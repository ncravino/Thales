#!/usr/bin/env python3
import os
import chromadb
import re 

book_path = "./books/"
db_path = "./chromadb/"

if not os.path.exists(db_path):
    os.mkdir(db_path)

client = chromadb.PersistentClient(db_path)

collection = client.get_or_create_collection("stoics")

for book in os.listdir(book_path):
    
    book_name = os.path.splitext(book)[0]
    
    with open(book_path+book) as book_file:
        content = re.sub(r"\s+", ' ', book_file.read())
        collection.upsert(
            documents=[content],
            ids=[book_name])

