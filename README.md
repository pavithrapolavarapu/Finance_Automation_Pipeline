# Finance Automation System

# Project Description
  The Finance Automation System is a Python-based solution designed to streamline invoice management for businesses. It automates the entire workflow from email attachment retrieval to Excel reporting, including:
    Automatically downloading invoice attachments from your email inbox
    Extracting text from PDFs and images using OCR (Tesseract)
    Converting text into structured JSON invoice data using Google Gemini AI
    Validating invoice data for accuracy before storage
    Storing invoice and line item details in a SQLite database
    Generating detailed Excel reports with summaries and visual charts

  This system significantly reduces manual effort, minimizes errors, and provides a quick, structured overview of all invoices and vendor expenses.

# Features
- Automatic email attachment download
- OCR text extraction from PDFs and images
- AI-based JSON extraction for invoice details
- Validation of invoices before saving
- Database storage in SQLite
- Excel report generation with summaries and charts


# Project Architecture
  The Finance Automation System follows a modular pipeline architecture:

        +-------------------+
        |   Email Server    |
        |  (IMAP Inbox)     |
        +-------------------+
                  |
                  v
        +-------------------+
        |  Email Reader     |  --> Downloads attachments from emails
        +-------------------+
                  |
                  v
        +-------------------+
        | Document Reader   |  --> OCR text extraction (Tesseract)
        |                   |  --> AI JSON extraction (Google Gemini)
        +-------------------+
                  |
                  v
        +-------------------+
        | Invoice Validator |  --> Validates invoice totals, dates, and fields
        +-------------------+
                  |
                  v
        +-------------------+
        | Database Module   |  --> Stores invoices, line items, and taxes in SQLite
        +-------------------+
                  |
                  v
        +-------------------+
        | Report Generator  |  --> Generates Excel reports with summaries and charts
        +-------------------+

  Flow Description
     Email Reader: Connects to your email inbox, fetches invoices, and saves attachments locally.
     Document Reader: Processes PDFs/images using OCR, then AI extracts structured JSON.
     Invoice Validator: Checks data accuracy, including totals, taxes, and required fields.
     Database Module: Saves validated invoices into SQLite tables (invoices, line_items, tax). Prevents duplicates.
     Report Generator: Reads data from the database and generates Excel reports with multiple
     sheets, summaries, and charts.


# Setup and Libraries 
1. PYTHON VERSION
   Recommended: Python 3.14.2

2. Python Standard Libraries(No installation required):
   os – File and folder operations
   re – Regular expressions for parsing and cleaning text
   io – Byte stream handling for images
   datetime – Handling email and invoice dates
   email – Parsing emails
   imaplib – Connecting to IMAP email servers
   sqlite3 – SQLite database handling

3. Third-Party Libraries(Installation required):
          pip install pandas
          pip install numpy
          pip install opencv-python
          pip install pillow
          pip install pytesseract
          pip install PyMuPDF
          pip install xlsxwriter
          pip install google-genai

   pandas - Data manipulation, grouping, exporting Excel reports
   numpy - Image array handling for OpenCV
   opencv-python (cv2) - Image preprocessing: grayscale, blur, threshold
   Pillow (PIL)	- Open and convert images for OCR
   pytesseract - Python wrapper for Tesseract OCR engine
   PyMuPDF (fitz) -	Read PDFs as images for OCR
   xlsxwriter -	Create Excel files with multiple sheets and charts
   google-genai -Google Gemini AI for structured JSON extraction

4. External Executable
   Tesseract OCR – Required for OCR extraction.
   Download link: https://github.com/tesseract-ocr/tesseract

5. Local Project Modules
   These are Python files:
            email_reader.py – Downloads attachments from email inbox
            document_reader.py – OCR extraction and AI JSON extraction
            database.py – Save invoice JSON to SQLite database
            report_generate.py – Generate Excel reports
            invoice_validator.py – Validate invoice data before saving

# APIs and Services used
1. Google Gemini AI
   Purpose: Converts raw OCR text into structured JSON for invoices.
   Usage in project: document_reader.py → extract_json_from_text()

   Setup:
   Get an API key from Google Cloud.
   Store it in your config.py.
   Call the API in your code.

2. IMAP Email Server
   Purpose: Automatically fetch emails and download invoice attachments from your inbox.
   Usage in project: email_reader.py → read_emails()

   Setup:
   Enable IMAP access in your email account settings.
   Store email credentials in config.py.
   The script connects and downloads attachments automatically.

3. Tesseract OCR
   Purpose: Extract text from images or PDF invoices for further processing.
   Usage in project: document_reader.py → extract_text()

   Setup:
   Windows: Download and install from Tesseract OCR
   Set path in your Python code











