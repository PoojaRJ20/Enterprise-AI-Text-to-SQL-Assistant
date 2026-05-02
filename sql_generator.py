import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

MODEL_NAME = "Qwen/Qwen2.5-Coder-1.5B-Instruct"


tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

llm = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float16,
    device_map="auto"
)

llm.eval()
def build_schema_text(selected_columns):
    grouped = {}

    for item in selected_columns:
        table_name = item["table_name"]

        if table_name not in grouped:
            grouped[table_name] = []

        grouped[table_name].append(item)

    schema_text = ""

    for table_name, cols in grouped.items():
        schema_text += f"\nTable: {table_name}\nColumns:\n"

        for item in cols:
            col = item["column_name"]
            info = item["column_info"]
            aliases = ", ".join(info.get("aliases", []))
            desc = info.get("description", "")

            schema_text += f"- {col}\n"
            schema_text += f"  Aliases: {aliases}\n"
            schema_text += f"  Description: {desc}\n"

        schema_text += "\n"

    return schema_text
def build_prompt(question, schema_text):
    return f"""
You are a PostgreSQL SQL generator.

STRICT RULES:
- ONLY use ONE table
- DO NOT use JOIN
- DO NOT use subqueries
- ONLY use columns from schema
- ALWAYS use ORDER BY + LIMIT 1

Schema:
{schema_text}

Question:
{question}

SQL:
"""
def generate_sql(prompt):
    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=2048
    ).to(llm.device)

    input_len = inputs["input_ids"].shape[1]

    with torch.no_grad():
        outputs = llm.generate(
            **inputs,
            max_new_tokens=150,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id
        )
    generated_tokens = outputs[0][input_len:]

    result = tokenizer.decode(
        generated_tokens,
        skip_special_tokens=True
    ).strip()

    result = result.replace("```sql", "").replace("```", "").strip()

    if ";" in result:
        result = result.split(";")[0].strip() + ";"

    return result    