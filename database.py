import sqlite3
import re

#cleans the unwanted details or symbols in the numbers and gives correct value number 
def clean_number(value):

    try:
        #Removes all characters except digits (0-9) and the decimal point (.).
        return float(re.sub("[^0-9.]", "", str(value)))
    except:
        return 0

#saves to database
def save_to_db(data):
    #creates a sqlite database file as finance db
    conn = sqlite3.connect("finance.db")
    #cursor is used to execute the sql queries
    cursor = conn.cursor()

   
    # CREATING INVOICE TABLE 
    #this is a sql command to create a invoice table if doesnt exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS invoices(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        vendor_name TEXT,
        vendor_gstin TEXT,
        order_id TEXT,
        invoice_number TEXT,
        invoice_date TEXT,
        total_amount REAL,
        payment_status TEXT,
        category TEXT
    )
    """)

    # CREATING LINE ITEMS TABLE
    #this is a sql command to create a line items table if doesnt exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS line_items(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        invoice_id INTEGER,
        description TEXT,
        quantity INTEGER,
        unit_price REAL,
        item_total REAL
    )
    """)

    # CREATING TAX TABLE
    #this is a sql command to create a tax table if doesnt exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tax(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        invoice_id INTEGER,
        tax_name TEXT,
        rate TEXT,
        amount REAL
    )
    """)

   
    # QUERY to check for the DUPLICATE INVOICES 
   
    cursor.execute(
        "SELECT id FROM invoices WHERE invoice_number=?",
        (data.get("invoice_number"),)
    )

    if cursor.fetchone():
        print("Duplicate invoice detected")
        conn.close()
        return
    
    #Retrieves total_amount from the dictionary and converts it to a float using clean_number.
    total = clean_number(data.get("total_amount"))

    # INSERT INVOICE data into invoices table
    cursor.execute("""
    INSERT INTO invoices(
        vendor_name,
        vendor_gstin,
        order_id,
        invoice_number,
        invoice_date,
        total_amount,
        payment_status,
        category
    )
    VALUES (?,?,?,?,?,?,?,?)
    """, (
        data.get("vendor_name"),
        data.get("vendor_gstin"),
        data.get("order_id"),      
        data.get("invoice_number"),
        data.get("invoice_date"),
        total,
        data.get("payment_status"),
        data.get("category")
    ))

    invoice_id = cursor.lastrowid

  
    # INSERT LINE ITEMS line items
    #Inserts each line item linked to the invoice_id
    for item in data.get("line_items", []):

        cursor.execute("""
        INSERT INTO line_items(
            invoice_id,
            description,
            quantity,
            unit_price,
            item_total
        )
        VALUES (?,?,?,?,?)
        """, (
            invoice_id,
            item.get("description"),
            int(item.get("quantity", 0)),
            clean_number(item.get("unit_price")),
            clean_number(item.get("item_total"))
        ))
    
    # INSERT TAX BREAKDOWN to tax
    # Inserts each tax entry linked to the invoice.
    for tax in data.get("tax_breakdown", []):

        cursor.execute("""
        INSERT INTO tax(
            invoice_id,
            tax_name,
            rate,
            amount
        )
        VALUES (?,?,?,?)
        """, (
            invoice_id,
            tax.get("tax_name"),
            tax.get("rate"),
            clean_number(tax.get("amount"))
        ))

    conn.commit()
    conn.close()
    print("Invoice stored successfully")