import re
import sqlglot
from sqlalchemy import text
from db import engine


def validate_sql(sql):
    try:
        parsed = sqlglot.parse_one(sql, dialect="postgres")

        if parsed.key != "select":
            return False, "Only SELECT allowed"

        return True, "SQL validation passed"

    except Exception as e:
        return False, str(e)

def execute_sql(sql):
    with engine.connect() as conn:
        rows = conn.execute(text(sql)).mappings().all()

    return [dict(row) for row in rows]


def reject_bad_sql(sql):
    bad_patterns = [
        " join ",
        "case ",
        "exists ",
        " coalesce "
    ]
    sql_lower = f" {sql.lower()} "

    for pattern in bad_patterns:
        if pattern in sql_lower:
            return True

    return False