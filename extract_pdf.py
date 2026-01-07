from pdfminer.high_level import extract_text

def extract_text_from_pdf(pdf_path):
    try:
        text = extract_text(pdf_path)
        return text
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    pdf_path = r"d:\NEST 2.0\NEST 2.0 Detailed Problem Statements.pdf"
    text = extract_text_from_pdf(pdf_path)
    if text:
        # Split text into manageable chunks or just print it all if it's not too huge for the terminal
        # Actually, let's write it to a UTF-8 file and read it in chunks.
        with open(r"d:\NEST 2.0\full_text.txt", "w", encoding="utf-8") as f:
            f.write(text)
        print("Text extracted and saved to full_text.txt")
    else:
        print("No text extracted.")
