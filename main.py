from email_reader import read_emails
from document_reader import extract_text, extract_json_from_text_gemini_api
from database import save_to_db
from report_generate import generate_excel_report
from invoice_validator import validate_invoice,categorize_invoice


def main():

    print("\nFinance Automation Pipeline Started\n")
    #Returns a list of file paths for all attachments downloaded
    files = read_emails(limit=10)
    if not files:
        print("No attachments found")
        return
    #Prints how many files were downloaded
    print("Total downloaded files:", len(files))
    #Process each downloaded file and Prints the file name for tracking
    for file in files:
        print("\nProcessing:", file)
        #extract raw text from PDF/image
        text = extract_text(file)
        #returns structured JSON
        data = extract_json_from_text_gemini_api(text)
        #Checks if the JSON is valid or not 
        if data:
            validate_invoice(data)
            # assign category
            data = categorize_invoice(data)
            #Saves validated invoice JSON to SQLite database 
            save_to_db(data)
    #Generate Excel report
    generate_excel_report()
    #prints pipeline completed 
    print("\nPipeline Completed")

#Run pipeline if script is executed directly
if __name__ == "__main__":
    main()