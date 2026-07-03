import chromadb
import os

# 1. Initialize local persistent database
db_path = "./data/chroma_storage"
client = chromadb.PersistentClient(path=db_path)

# 2. Create or open a collection (like an SQL table)
collection = client.get_or_create_collection(name="contract_knowledge_base")

txt_folder = "./data/full_contract_txt 2"
print("Scanning Kaggle contract repository for vector embedding...")

# 3. Read first 10 contracts and slice them into semantic paragraphs
doc_ids = []
documents = []
metadatas = []

for file_name in os.listdir(txt_folder)[:10]:
    if file_name.endswith(".txt"):
        file_path = os.path.join(txt_folder, file_name)
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
            
        # Basic chunking by paragraph breaks
        paragraphs = [p.strip() for p in text.split("\n\n") if len(p.strip()) > 50]
        
        for i, para in enumerate(paragraphs):
            doc_ids.append(f"{file_name}_para_{i}")
            documents.append(para)
            metadatas.append({"filename": file_name, "chunk_index": i})

# 4. Save to ChromaDB (Automatically handles tokenization & embedding models!)
print(f"Adding {len(documents)} document chunks into ChromaDB...")
collection.add(documents=documents, metadatas=metadatas, ids=doc_ids)

print("\n--- SUCCESS! VECTOR DATABASE POPULATED ---")
print(f"All vectors permanently saved inside: {db_path}")

# Test a Semantic Query
results = collection.query(query_texts=["What are the rules for contract termination?"], n_results=2)
print("\nTop 2 Semantic Matches Found:")
print(results["documents"])
