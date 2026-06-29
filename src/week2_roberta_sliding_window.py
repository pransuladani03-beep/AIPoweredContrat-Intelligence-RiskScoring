from transformers import AutoTokenizer
import os

tokenizer = AutoTokenizer.from_pretrained("roberta-base")

# Grab a long contract from your specific folder
txt_folder = "./data/full_contract_txt 2/full_contract_txt"
sample_file = os.listdir(txt_folder)[0]
with open(os.path.join(txt_folder, sample_file), "r", encoding="utf-8", errors="ignore") as f:
    contract_text = f.read()

question = "What are the termination for convenience terms?"

print(f"Tokenizing {sample_file} using Sliding Window...")

# Apply Sliding Window so long text is safely broken into chunks
chunks = tokenizer(
    [question],
    [contract_text],
    max_length=512,          # Max tokens per chunk
    stride=128,              # Overlap chunks by 128 words so clauses don't get broken
    truncation="only_second",
    return_overflowing_tokens=True,
    padding="max_length"
)

print(f"\nSuccess! Your massive contract was safely split into {len(chunks['input_ids'])} AI-readable chunks.")
print("Now your RoBERTa model won't run out of memory!")
