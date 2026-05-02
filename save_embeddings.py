import json
import torch

from metadata_loader import load_metadata_from_neon, table_to_text
from embeddings import embedding_model


tables_cache = load_metadata_from_neon()


table_texts_cache = [
    table_to_text(t)
    for t in tables_cache
]
table_embeddings_cache = embedding_model.encode(
    table_texts_cache,
    convert_to_tensor=True
)


torch.save(
    table_embeddings_cache,
    "table_embeddings.pt"
)
with open("tables_cache.json", "w", encoding="utf-8") as f:
    json.dump(tables_cache, f, ensure_ascii=False, indent=2)


print("Saved embeddings")