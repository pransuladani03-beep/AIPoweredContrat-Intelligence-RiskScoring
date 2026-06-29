from pdf2image import convert_from_path
import pytesseract
import os

pdf_folder = "./data/full_contract_pdf/full_contract_pdf"

def extract_text_from_pdf(pdf_path):
    print(f"Starting OCR on: {pdf_path}")
    
    # Convert PDF to images (300 DPI is best for legal text clarity)
    images = convert_from_path(pdf_path, dpi=300)
    full_text = ""
    
    for page_num, image in enumerate(images):
        print(f"Processing Page {page_num + 1}...")
        text = pytesseract.image_to_string(image)
        full_text += f"\n--- PAGE {page_num + 1} ---\n" + text
        
    return full_text

if __name__ == "__main__":
    # Grab the very first PDF inside your actual folder, recursively
    test_pdf = None
    for root, dirs, files in os.walk(pdf_folder):
        for f in files:
            if f.endswith(".pdf"):
                test_pdf = os.path.join(root, f)
                break
        if test_pdf:
            break
            
    if test_pdf:
        extracted_content = extract_text_from_pdf(test_pdf)
        print("\n--- OCR COMPLETE ---")
        print(extracted_content[:500])
    else:
        print("No PDFs found inside ./data/full_contract_pdf!")
