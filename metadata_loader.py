from db import engine


def load_metadata_from_neon():
    with engine.connect() as conn:
        rows = conn.execute(text("""
            SELECT
                table_name,
                table_description,
                column_name,
                aliases,
                description,
                secure,
                indexed,
                sentence_template,
                validation_rules
            FROM hes_meta.metadata_columns
            ORDER BY table_name, column_name
        """)).mappings().all()
    tables = {}

    for row in rows:
        table_name = row["table_name"]

        if table_name not in tables:
            tables[table_name] = {
                "table_name": table_name,
                "table_description": row["table_description"] or "",
                "columns": {}
            }

        tables[table_name]["columns"][row["column_name"]] = {
            "aliases": row["aliases"] or [],
            "description": row["description"] or "",
            "secure": row["secure"] or False,
            "indexed": row["indexed"] or False,
            "sentence_template": row["sentence_template"] or "",
            "validation_rules": row["validation_rules"] or []
        }    


    return list(tables.values())


def table_to_text(table):
    txt = f"""
    Table: {table['table_name']}
    Description: {table.get('table_description', '')}
    """

    for col_name, info in table.get("columns", {}).items():
        aliases = ", ".join(info.get("aliases", []))
        desc = info.get("description", "")
        txt += f"\nColumn: {col_name}. Aliases: {aliases}. Description: {desc}"

    return txt