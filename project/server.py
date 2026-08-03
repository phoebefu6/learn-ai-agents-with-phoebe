"""daybreak-mcp - the running-project MCP server for learn-mcp-with-phoebe.

This is the server as it stands at the end of builder session b3:
three tools, two resources, one prompt, over daybreak.db (see seed_daybreak.py).

Run locally (stdio, sessions b2-b5):
    uv run mcp dev server.py        # opens the MCP Inspector
or wire it into a host via .mcp.json (session b4).

Session b6 switches the transport to Streamable HTTP:
    mcp.run(transport="streamable-http")

Requires: pip install "mcp[cli]"  (official Python SDK, spec 2025-11-25)
"""

import pathlib
import sqlite3

from mcp.server.fastmcp import FastMCP

DB_PATH = pathlib.Path(__file__).parent / "daybreak.db"

mcp = FastMCP("daybreak-mcp")


def _query(sql: str, params: tuple = ()) -> list[tuple]:
    con = sqlite3.connect(DB_PATH)
    try:
        return con.execute(sql, params).fetchall()
    finally:
        con.close()


# ---------- tools (model-controlled actions) ----------

@mcp.tool()
def query_sales(month: str) -> str:
    """Order count, refunds, and completed revenue for one month (YYYY-MM)."""
    rows = _query(
        """
        SELECT o.status, COUNT(DISTINCT o.order_id),
               COALESCE(SUM(oi.quantity * oi.unit_price), 0)
        FROM orders o
        JOIN order_items oi ON oi.order_id = o.order_id
        WHERE substr(o.order_date, 1, 7) = ?
        GROUP BY o.status
        """,
        (month,),
    )
    if not rows:
        return f"No orders found for {month}."
    by_status = {status: (n, rev) for status, n, rev in rows}
    total = sum(n for n, _ in by_status.values())
    completed_rev = by_status.get("completed", (0, 0.0))[1]
    refunded = by_status.get("refunded", (0, 0.0))[0]
    return (
        f"{month}: {total} orders ({refunded} refunded), "
        f"completed revenue ${completed_rev:.2f}."
    )


@mcp.tool()
def top_products(from_date: str = "2026-01-01", to_date: str = "2026-12-31") -> str:
    """Best-selling products by quantity for a date range (YYYY-MM-DD)."""
    rows = _query(
        """
        SELECT p.name, SUM(oi.quantity) AS qty
        FROM order_items oi
        JOIN orders o ON o.order_id = oi.order_id
        JOIN products p ON p.product_id = oi.product_id
        WHERE o.order_date BETWEEN ? AND ? AND o.status = 'completed'
        GROUP BY p.name
        ORDER BY qty DESC
        LIMIT 5
        """,
        (from_date, to_date),
    )
    if not rows:
        return "No completed sales in that range."
    lines = [f"{i + 1}. {name} - {qty} sold" for i, (name, qty) in enumerate(rows)]
    return "Top products " + from_date + " to " + to_date + ":\n" + "\n".join(lines)


@mcp.tool()
def subscription_status() -> str:
    """Active vs cancelled subscription counts, with monthly quantities."""
    rows = _query(
        """
        SELECT CASE WHEN cancel_date IS NULL THEN 'active' ELSE 'cancelled' END,
               COUNT(*), SUM(monthly_qty)
        FROM subscriptions
        GROUP BY 1
        """
    )
    parts = [f"{status}: {n} subs ({qty} bags/month)" for status, n, qty in rows]
    return "Subscriptions - " + "; ".join(parts)


# ---------- resources (app-controlled context) ----------

@mcp.resource("daybreak://catalog")
def catalog() -> str:
    """Daybreak product catalog with prices."""
    rows = _query("SELECT name, category, price, roast FROM products ORDER BY price DESC")
    lines = ["# Daybreak catalog"]
    for name, category, price, roast in rows:
        roast_note = f" ({roast})" if roast else ""
        lines.append(f"- {name} - {category} - ${price:.2f}{roast_note}")
    return "\n".join(lines)


@mcp.resource("daybreak://policy/refunds")
def refund_policy() -> str:
    """Refund and cancellation policy."""
    return (
        "# Daybreak refund + cancellation policy\n"
        "- Full refund within 14 days of any order, no questions asked.\n"
        "- Subscriptions cancel any time; the current month still ships.\n"
        "- Refunded orders keep their row in the orders table with status "
        "'refunded' - revenue reports must exclude them."
    )


# ---------- prompts (user-controlled templates) ----------

@mcp.prompt()
def monthly_report(month: str) -> str:
    """Standard monthly ops report for the founder."""
    return (
        f"Write the {month} ops report for Daybreak: orders and revenue vs the "
        f"previous month, refunds, subscription changes, and one concrete "
        f"action for next month. Use query_sales, top_products and "
        f"subscription_status for the numbers - do not estimate."
    )


if __name__ == "__main__":
    mcp.run()  # stdio transport - b6 switches this to streamable-http
