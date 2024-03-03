import PyPDF2, os, re, csv, sys

pdfDirectoryName = "pdfs"
csv_filename = "temp_transactions.csv"

def get_script_directory():
    """Return the directory containing the script."""
    if getattr(sys, 'frozen', False):  # PyInstaller bundle
        return os.path.dirname(os.path.dirname(sys.executable))
    return os.path.dirname(os.path.abspath(__file__))


def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for  page in reader.pages:
            text += page.extract_text()
    return text

# get_pdf_transactions_from_dir can accept a directory and will go through all statement documents.
def get_pdf_transactions_from_dir(directory):
    transactions = []
    script_dir = get_script_directory()
    pdfs_dir = os.path.join(script_dir, directory)

    if os.path.exists(pdfs_dir) and os.path.isdir(pdfs_dir):
        for filename in os.listdir(pdfs_dir):
                if filename.endswith(".pdf"):
                    pdf_path = os.path.join(pdfs_dir, filename)
                    # Get text for each .pdf file
                    text = extract_text_from_pdf(pdf_path)
                    transactions += get_line_transactions_from_text(text)
        pass
    else:
        raise FileNotFoundError(f"Directory not found: {pdfs_dir}")

    return transactions        
   

def get_line_transactions_from_text(text):
    transactions = []
    pattern = r"([A-Z]{3}\s\d{2})\s([A-Z]{3}\s\d{2})\s(.+)\n(.+?)(-?\$\d+\.\d{2})$"
    for match in re.finditer(pattern, text, re.MULTILINE):
        transaction_date = f"{match.group(2)}"
        description = match.group(3).strip()
        amount = match.group(5)
        transactions.append({"date": transaction_date, "description": description, "amount": amount})
    return transactions

def write_to_file(csv_filename, transactions):
    with open(csv_filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['date', 'description', 'amount'])
        writer.writeheader()
        writer.writerows(transactions)


if __name__ == "__main__":
    transactions = get_pdf_transactions_from_dir(pdfDirectoryName)
    write_to_file(csv_filename, transactions)
