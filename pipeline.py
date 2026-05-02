from metadata_loader import load_metadata_from_neon, table_to_text
from embeddings import (
    normalize_question,
    select_top_tables,
    select_relevant_columns,
    embedding_model
)
from sql_generator import (
    build_schema_text,
    build_prompt,
    generate_sql
)
from sql_utils import (
    validate_sql,
    execute_sql,
    reject_bad_sql
)

import torch

# ---------- LOAD TABLES ----------

tables_cache = load_metadata_from_neon()


# ---------- PRECOMPUTE EMBEDDINGS ----------

table_texts_cache = [
    table_to_text(t)
    for t in tables_cache
]


table_embeddings_cache = embedding_model.encode(
    table_texts_cache,
    convert_to_tensor=True
)

# ---------- MAIN PIPELINE ----------

def run_pipeline(question):
    print("\n" + "=" * 50)
    print("User Question:")
    print(question)

    search_question = normalize_question(question)

    selected_tables = select_top_tables(
        search_question,
        tables_cache,
        table_embeddings_cache,
        top_k=3
    )

    print("\nTop Selected Tables:")
    for t in selected_tables:
        print(f"- {t['table_name']} | score: {t['score']:.4f}")

    selected_columns = select_relevant_columns(
        search_question,
        selected_tables,
        top_k=10
    )

    print("\nTop Selected Columns:")

    for c in selected_columns:
        print(
            f"- {c['table_name']}.{c['column_name']} "
            f"| score: {c.get('score', 0):.4f}"
        )
     schema_text = build_schema_text(selected_columns)

    prompt = build_prompt(question, schema_text)

    sql = generate_sql(prompt)

    print("\nGenerated SQL:")
    print(sql)

    is_valid, message = validate_sql(sql)

    if not is_valid:
        print(message)
        return
    try:
        result = execute_sql(sql)

        print("\nQuery Result:")
        print(result)

        return result

    except Exception as e:
        print(e)
