# sql_builder.py
from typing import List

from query_intent import QueryIntent, FilterIntent, SortIntent
from schema import SchemaConfig


def _quote_ident(name: str) -> str:
    """
    Very simple identifier quoting. This is reasonably safe/common for
    PostgreSQL-like dialects. You can later make this dialect-aware.
    """
    return f'"{name}"'


def _escape_literal(value: str) -> str:
    return value.replace("'", "''")


def _format_value(value: str) -> str:
    """
    Naive literal formatting: everything becomes a quoted string.
    Data engineers can adjust this or post-edit the SQL as needed.
    """
    return f"'{_escape_literal(value)}'"


def _build_where(filters: List[FilterIntent]) -> str:
    if not filters:
        return ""
    parts = []
    for f in filters:
        parts.append(f"{_quote_ident(f.field)} {f.operator} {_format_value(f.value)}")
    return "WHERE " + " AND ".join(parts)


def _build_order_by(sort: List[SortIntent]) -> str:
    if not sort:
        return ""
    parts = [f"{_quote_ident(s.field)} {s.direction.upper()}" for s in sort]
    return "ORDER BY " + ", ".join(parts)


def build_sql(intent: QueryIntent, schema: SchemaConfig) -> str:
    """
    Convert a QueryIntent into a SQL SELECT statement string using the
    configured schema to map entities → tables.
    """
    table_name = schema.get_table_for_entity(intent.entity)
    if not table_name:
        raise ValueError(f"No table configured for entity '{intent.entity}'")

    # SELECT clause
    if not intent.fields:
        select_expr = "*"
    else:
        select_expr = ", ".join(_quote_ident(f) for f in intent.fields)

    distinct_str = "DISTINCT " if intent.distinct else ""

    parts: List[str] = []
    parts.append(f"SELECT {distinct_str}{select_expr}")
    parts.append(f"FROM {_quote_ident(table_name)}")

    where_clause = _build_where(intent.filters)
    if where_clause:
        parts.append(where_clause)

    order_by_clause = _build_order_by(intent.sort)
    if order_by_clause:
        parts.append(order_by_clause)

    if intent.limit is not None:
        parts.append(f"LIMIT {intent.limit}")

    return "\n".join(parts) + ";"
