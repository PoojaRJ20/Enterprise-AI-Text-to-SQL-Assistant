import torch
from sentence_transformers import SentenceTransformer, util

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


def normalize_question(question):
    q = question.lower()

    intent_map = {
        "last seen": "last_comm",
        "last ping": "last_comm",
        "last online": "last_comm",
        "last contact": "last_comm",
        "last communication": "last_comm",
        "communicate": "last_comm",
        "communication": "last_comm",
        "latest communication": "last_comm",
        "latest update": "last_comm",
        "last activity": "last_comm",
        "last active": "last_comm",
        "latest record": "last_comm",
    }

    for key, value in intent_map.items():
        if key in q:
            return question + " " + value

    return question
def select_top_tables(question, tables, table_embeddings_cache, top_k=3):
    question_embedding = embedding_model.encode(
        question,
        convert_to_tensor=True
    )

    scores = util.cos_sim(question_embedding, table_embeddings_cache)[0]

    top_results = scores.topk(k=min(top_k, len(tables)))

    selected = []

    for score, idx in zip(top_results.values, top_results.indices):
        i = int(idx)

        selected.append({
            "table_name": tables[i]["table_name"],
            "score": float(score),
            "table": tables[i]
        "table": tables[i]
        })

    return selected


def select_relevant_columns(question, selected_tables, top_k=10):
    question_lower = question.lower()

    alias_hits = []
    seen = set()

    for table_item in selected_tables:
        table = table_item["table"]
        table_name = table["table_name"] 
        for col_name, info in table.get("columns", {}).items():
            if info.get("secure"):
                continue

            aliases = info.get("aliases", []) or []

            for alias in aliases:
                alias_lower = alias.lower().strip()

                if alias_lower and alias_lower in question_lower:
                    key = (table_name, col_name)

                    if key not in seen:
                        alias_hits.append({
                            "table_name": table_name,
                            "column_name": col_name,
                            "column_info": info,
                            "score": 1.0,
                            "source": "alias" 
                        })
                        seen.add(key)
    if alias_hits:
        print("\n🔥 Alias match used")
        return alias_hits[:top_k]

    print("\n⚡ Using embedding fallback")

    column_items = []
    column_texts = []

    for table_item in selected_tables:
        table = table_item["table"]
        table_name = table["table_name"]

        for col_name, info in table.get("columns", {}).items():
            if info.get("secure"):
                continue
            column_items.append({
                "table_name": table_name,
                "column_name": col_name,
                "column_info": info
            })

            text_data = f"""
            Table: {table_name}
            Column: {col_name}
            Aliases: {', '.join(info.get('aliases', []))}
            Description: {info.get('description', '')}
            """

            column_texts.append(text_data)
    column_embeddings = embedding_model.encode(
        column_texts,
        convert_to_tensor=True
    )

    question_embedding = embedding_model.encode(
        question,
        convert_to_tensor=True
    ) 
    scores = util.cos_sim(question_embedding, column_embeddings)[0]

    top_results = scores.topk(k=min(top_k, len(column_items)))

    results = []

    for score, idx in zip(top_results.values, top_results.indices):
        item = column_items[int(idx)]

        results.append({
            **item,
            "score": float(score),
            "source": "embedding"
        })

    return results
    