#!/usr/bin/env python3
import chromadb
from transformers import pipeline
import logging
import sys
logging.basicConfig(stream=sys.stdout, level=logging.ERROR)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

model = "distilbert-base-cased-distilled-squad"
db_path = "./chromadb/"

client = chromadb.PersistentClient(db_path)

try:
    collection = client.get_collection("stoics")
except ValueError:
    print("Please run load_books to load the books into the database")
    exit(-1)

qa_pipe = pipeline("question-answering", model=model)

print("use quit to exit")
while True:
    try:
        question = input("> ")
    except EOFError:
        print("exiting...")
        exit(0)
    if question == "quit":
        print("exiting...")
        exit(0)
    context = collection.query(
        query_texts=[question],
        n_results=3
    )["documents"]
    if len(context) > 0:
        answer = qa_pipe(question=question, context=".".join([".".join(c) for c in context]))
        print(answer)
    else:
        print("No information found about that")