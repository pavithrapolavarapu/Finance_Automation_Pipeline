def categorize_invoice(data):

    categories = {
        "Office Expenses": [
            "stationery", "office", "chair", "desk", "printer", "paper", "pen"
        ],

        "IT Equipment": [
            "laptop", "computer", "desktop", "monitor", "WirelessMouse", "keyboard","BluetoothHeadphones",
            "mouse", "hard disk", "ssd", "ram", "router"
        ],

        "Tools & Software": [
            "software", "tool", "subscription", "license", "saas"
        ],

        "Travel & Petrol": [
            "petrol", "flight", "hotel", "cab", "taxi", "uber", "ola"
        ],

        "Utilities": [
            "electricity", "water", "internet", "utility", "wifi"
        ]
    }

    assigned = "Other"
    print("data",data.get("line_items"))
    # Loop through line items
    for item in data.get("line_items", []):
        description = item.get("description", "").lower()

        for category, keywords in categories.items():
            for word in keywords:
                if word in description:
                    assigned = category
                    break

            if assigned != "Other":
                break

        if assigned != "Other":
            break

    data["category"] = assigned
    return data


def validate_invoice(data):

    issues = []

    if not data.get("vendor_name"):
        issues.append("Missing vendor name")

    if not data.get("invoice_number"):
        issues.append("Missing invoice number")

    if not data.get("total_amount"):
        issues.append("Missing total amount")

    line_items = data.get("line_items", [])

    items_total = 0

    for item in line_items:

        try:
            items_total += float(item.get("item_total",0))
        except:
            pass

    try:
        invoice_total = float(data.get("total_amount",0))
    except:
        invoice_total = 0

    if abs(items_total - invoice_total) > 5:

        issues.append(
            f"Line items total {items_total} != invoice total {invoice_total}"
        )

    if issues:

        print("\n⚠ Invoice Validation Issues:")

        for i in issues:
            print("-", i)

    else:

        print("\n✅ Invoice validation passed")

    return issues