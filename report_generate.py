import sqlite3
import pandas as pd
import os

def generate_excel_report():
    # Connect to SQLite database
    conn = sqlite3.connect("finance.db")
    invoices = pd.read_sql("SELECT * FROM invoices", conn)
    line_items = pd.read_sql("SELECT * FROM line_items", conn)
    conn.close()

    # Create reports folder
    os.makedirs("reports", exist_ok=True)
    file = "reports/finance_report.xlsx"

    # Initialize Excel writer
    writer = pd.ExcelWriter(file, engine="xlsxwriter")

    # Sheet 1 – Invoices
    invoices.to_excel(writer, sheet_name="Invoices", index=False)

    # Sheet 2 – Line Items
    line_items.to_excel(writer, sheet_name="Line_Items", index=False)

    # Sheet 3 – Summary by Product
    summary = line_items.groupby("description")["item_total"].sum().reset_index()
    summary.to_excel(writer, sheet_name="Summary", index=False)

    # Sheet 4 – Vendor Summary
    vendor_summary = invoices.groupby("vendor_name")["total_amount"].sum().reset_index()
    vendor_summary.to_excel(writer, sheet_name="Vendor_Summary", index=False)

    # Sheet 5 – Category Summary
    if 'category' in invoices.columns:
        category_summary = invoices.groupby("category")["total_amount"].sum().reset_index()
        category_summary.to_excel(writer, sheet_name="Category_Summary", index=False)

    # Access workbook object for charts
    workbook = writer.book

    # Pie chart for Summary by Product
    worksheet_summary = writer.sheets["Summary"]
    chart_summary = workbook.add_chart({"type": "pie"})
    max_row_summary = len(summary) + 1
    chart_summary.add_series({
        "name": "Expenses by Product",
        "categories": f"=Summary!A2:A{max_row_summary}",
        "values": f"=Summary!B2:B{max_row_summary}"
    })
    worksheet_summary.insert_chart("D2", chart_summary)

    # Pie chart for Category Summary
    if 'category' in invoices.columns:
        worksheet_cat = writer.sheets["Category_Summary"]
        chart_cat = workbook.add_chart({"type": "pie"})
        max_row_cat = len(category_summary) + 1
        chart_cat.add_series({
            "name": "Expenses by Category",
            "categories": f"=Category_Summary!A2:A{max_row_cat}",
            "values": f"=Category_Summary!B2:B{max_row_cat}"
        })
        worksheet_cat.insert_chart("D2", chart_cat)

    # Save and close Excel file
    writer.close()
    print("Excel report generated:", file)