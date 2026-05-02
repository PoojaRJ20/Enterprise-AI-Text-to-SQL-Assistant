from pipeline import run_pipeline

while True:
    question = input("\nAsk Question: ")

    if question.lower() == "exit":
        break

    run_pipeline(question)