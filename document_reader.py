import fitz
import pytesseract
import cv2
import numpy as np
from PIL import Image
import io
import os
import re
import json
from google import genai
from config import GEMINI_API_KEY

# Sets the path to the Tesseract OCR executable on Windows
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


# Image preprocessing (main purpose to improve OCR accuracy)
def preprocess_image(img):
    #Converts image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Improve contrast and brightness
    gray = cv2.convertScaleAbs(gray, alpha=1.5, beta=30)
    # Reduce noise
    blur = cv2.GaussianBlur(gray, (3,3), 0)
    # Automatic thresholding for better OCR text recognition.
    thresh = cv2.threshold(
        blur, 0, 255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )[1]
    # processed image ready for OCR
    return thresh


# LINE ITEM DETECTION
def extract_line_items_from_text(text):
    # Splits OCR text into lines
    lines = text.split("\n")
    items = []
    #Matches description text,quantity,unit price with possible commas/decimal,item total at line end.
    pattern = re.compile(r"(.+?)\s+(\d+)\s+([\d,.]+)\s+([\d,.]+)$")
    for line in lines:
        match = pattern.search(line)
        if match:
            try:
                items.append({
                    "description": match.group(1).strip(),
                    "quantity": int(match.group(2)),
                    "unit_price": float(match.group(3).replace(",", "")),
                    "item_total": float(match.group(4).replace(",", ""))
                })
            except:
                pass
    return items


# OCR EXTRACTION
def extract_text(file_path):
    print("Reading:", file_path)
    #stores file extension
    ext = os.path.splitext(file_path)[1].lower()
    #store all extracted text
    full_text = ""
    # OCR configuration and Only consider allowed characters
    config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz.,:-()/ '
    if ext == ".pdf":
        doc = fitz.open(file_path)
        for page in doc:
            # Converts page to high-resolution image
            pix = page.get_pixmap(dpi=500)
            # Converts pixmap to bytes
            img_bytes = pix.tobytes("png")
            image = Image.open(io.BytesIO(img_bytes))
            # converts to numpy array
            img = np.array(image)
            #Preprocesses image for OCR
            processed = preprocess_image(img)
            text = pytesseract.image_to_string(processed, config=config)
            #Appends each page's text
            full_text += text + "\n"
    # Image handling
    elif ext in [".jpg", ".jpeg", ".png"]:
        #Reads image using OpenCV, preprocesses, extracts text
        img = cv2.imread(file_path)
        processed = preprocess_image(img)
        full_text = pytesseract.image_to_string(processed, config=config)

    # TEXT CLEAN
    # Fix numbers like 01559 → 1559
    full_text = re.sub(r'\b0+(\d)', r'\1', full_text)
    # Remove incorrect currency characters before numbers
    full_text = re.sub(r'[WM](?=\d)', '', full_text)
    # Remove duplicate lines
    full_text = "\n".join(dict.fromkeys(full_text.splitlines()))
    # Remove empty lines
    full_text = "\n".join([line for line in full_text.splitlines() if line.strip()])
    #print cleaned OCR text
    print("\nOCR TEXT:\n", full_text)
    return full_text



# GEMINI AI JSON EXTRACTION 

def extract_json_from_text_gemini_api(text):
    detected_items = extract_line_items_from_text(text)
    #Initializes Gemini AI client with your API key
    client = genai.Client(api_key=GEMINI_API_KEY)
    #prompt tells to AI to extract structured invoice data as JSON
    prompt = f"""
Extract structured invoice data.
Return ONLY valid JSON.

Fields:
vendor_name
vendor_gstin
order_id
invoice_number
invoice_date
due_date
total_amount
payment_status

Line Items:
description
quantity
unit_price
item_total

Tax Breakdown:
tax_name
rate
amount

Detected possible rows:
{detected_items}

Invoice text:
{text}
"""
    #Calls Gemini AI to generate structured JSON from the prompt
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    result = response.text
    # Remove markdown formatting
    clean = re.sub(r"```json|```", "", result).strip()
    #If parsing pass it returns JSON or parsing fails it returns NONE
    try:
        data = json.loads(clean)
        # Pretty-print the clean JSON
        print("Extracted JSON:")
        print(json.dumps(data, indent=4))
        return data
    except:
        print("JSON parsing failed")
        print(result)
        return None