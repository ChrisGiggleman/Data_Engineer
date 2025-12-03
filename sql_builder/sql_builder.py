# sql_builder.py
from typing import List

from query_intent import QueryIntent, FilterIntent, SortIntent
from schema import SchemaConfig


def _quote_ident(name: str) -> str:
    """
    Simple identifier quoting. Works for many SQL dialects (Postgres-style).
    """
    return f'"{name}"'


def _escape_literal(value: str) -> str:
    return value.replace("'", "''")


def _format_literal(value: str) -> str:
    """
    Naive literal formatting: everything becomes a quoted string.
    Data engineers can adjust this or post-edit the SQL as needed.
    """
    return f"'{_escape_literal(value)}'"


def _field_expr(field: str) -> str:
    """
    Build the SQL expression for a "field":
    - "__count__" => COUNT(*)
    - "expr:..."  => raw SQL expression after "expr:"
    - anything else => quoted identifier
    """
    if field == "__count__":
        return "COUNT(*)"
    if field.startswith("expr:"):
        return field[len("expr:") :]
    return _quote_ident(field)


def _build_condition(f: FilterIntent) -> str:
    """
    Build a single condition string from a FilterIntent.
    Supports:
      =, !=, >, <, >=, <=, LIKE,
      IN (list),
      BETWEEN (range).
    """
    op = f.operator.upper()
    expr = _field_expr(f.field)

    # BETWEEN
    if op == "BETWEEN":
        # value can be a tuple (start, end) or list of length 2
        if isinstance(f.value, (tuple, list)) and len(f.value) == 2:
            v1, v2 = f.value
            return (
                f"{expr} BETWEEN "
                f"{_format_literal(str(v1))} AND {_format_literal(str(v2))}"
            )
        else:
            # fallback: treat as raw text after BETWEEN
            return f"{expr} BETWEEN {str(f.value)}"

    # IN
    if op == "IN":
        # value can be list/tuple or comma-separated string
        if isinstance(f.value, (list, tuple)):
            items = ", ".join(_format_literal(str(v)) for v in f.value)
        else:
            parts = [p.strip() for p in str(f.value).split(",") if p.strip()]
            items = ", ".join(_format_literal(p) for p in parts)
        return f"{expr} IN ({items})"

    # Simple comparison operators and LIKE
    return f"{expr} {op} {_format_literal(str(f.value))}"


def _build_filter_clause(
    filters: List[FilterIntent],
    clause_name: str,
) -> str:
    """
    Build a WHERE or HAVING clause from a list of FilterIntent objects.
    Respects each filter's logical operator (AND/OR).
    clause_name: "WHERE" or "HAVING"
    """
    if not filters:
        return ""
    parts: List[str] = []

    for idx, f in enumerate(filters):
        cond = _build_condition(f)
        if idx == 0:
            parts.append(cond)
        else:
            parts.append(f"{f.logical} {cond}")

    return f"{clause_name} " + " ".join(parts)


def _build_group_by(group_by: List[str]) -> str:
    if not group_by:
        return ""
    cols = ", ".join(_quote_ident(c) for c in group_by)
    return f"GROUP BY {cols}"


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

    # WHERE
    where_clause = _build_filter_clause(intent.filters, "WHERE")
    if where_clause:
        parts.append(where_clause)

    # GROUP BY / HAVING
    group_by_clause = _build_group_by(intent.group_by)
    if group_by_clause:
        parts.append(group_by_clause)

    having_clause = _build_filter_clause(intent.having, "HAVING")
    if having_clause:
        parts.append(having_clause)

    # ORDER BY
    order_by_clause = _build_order_by(intent.sort)
    if order_by_clause:
        parts.append(order_by_clause)

    # LIMIT
    if intent.limit is not None:
        parts.append(f"LIMIT {intent.limit}")

    return "\n".join(parts) + ";"
