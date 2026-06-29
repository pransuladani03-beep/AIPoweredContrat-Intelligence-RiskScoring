import spacy
from spacy.tokens import DocBin
import json

# Load spaCy's standard English pipeline
nlp = spacy.blank("en")
doc_bin = DocBin()

# We open your exact JSON file
json_path = "./data/CUAD_v1.json"

print(f"Loading {json_path} to build baseline training data...")
with open(json_path, "r", encoding="utf-8") as f:
    cuad_json = json.load(f)

# Grab just the first 5 contracts to train quickly without crashing your computer
for document in cuad_json["data"][:5]:
    for paragraph in document["paragraphs"]:
        text = paragraph["context"]
        doc = nlp.make_doc(text)
        ents = []
        
        # Look for the simple 'Parties' answers
        for qa in paragraph["qas"]:
            if qa["id"].endswith("__Parties") and qa["answers"]:
                ans = qa["answers"][0]
                start = ans["answer_start"]
                end = start + len(ans["text"])
                span = doc.char_span(start, end, label="PARTY")
                if span:
                    ents.append(span)
                    
        doc.ents = ents
        doc_bin.add(doc)

doc_bin.to_disk("./data/baseline.spacy")
print("\nSuccess! Saved baseline training data to ./data/baseline.spacy")
print("To train your model, run this command in your terminal:")
print("python -m spacy train config.cfg --output ./models/spacy_parties --paths.train ./data/baseline.spacy")
