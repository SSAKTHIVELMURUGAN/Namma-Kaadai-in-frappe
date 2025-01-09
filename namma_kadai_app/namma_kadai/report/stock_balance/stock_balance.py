import frappe
from frappe.utils import flt, getdate

def execute(filters=None):
    filters = filters or {}

    columns = [
        {
            "label": "Date", 
            "fieldname": "date", 
            "fieldtype": "Date", 
            "width": 150
        },
        {
            "fieldname": "shop_name", 
            "fieldtype": "Data",
            "label": "Shop Name", 
            "width": 150
        },
        {
            "label": "Item Code", 
            "fieldname": "item_code", 
            "fieldtype": "Data", 
            "width": 150
        },
        {
            "label": "In Quantity(Purchase)", 
            "fieldname": "in_qty", 
            "fieldtype": "Float", 
            "width": 120
        },
        {
            "label": "Out Quantity(Sale)", 
            "fieldname": "out_qty", 
            "fieldtype": "Float", 
            "width": 120
        },
        {
            "label": "Balance", 
            "fieldname": "balance", 
            "fieldtype": "Currency", 
            "width": 120
        },
        {
            "label": "Voucher Name", 
            "fieldname": "voucher_name", 
            "fieldtype": "Data", 
            "width": 180
        },
    ]
    
    data = get_stock_balance(filters)
    
    return columns, data

def get_stock_balance(filters):
    stock_balance = []
    date_filter = filters.get("date")
    shop_name_filter = filters.get("shop_name")
    item_name_filter = filters.get("item_name")

    # purchase and sale transactions from transaction
    # get_all will always store the data in list contains multi-dict [{},{},{}]
    transaction_details = frappe.get_all(
        "Transaction",
        filters={
            "is_cancel": 0, 
            "status": ["in", ["Purchase", "Sale"]]
        },
        fields=["shop_name", "item_name", "quantity", "rate", "total", "id", "date", "status"]
    )

    for transaction in transaction_details:
        # Apply filters
        if shop_name_filter and transaction.get('shop_name') != shop_name_filter:
            continue
        if item_name_filter and transaction.get('item_name') != item_name_filter:
            continue
        if date_filter:
            # Convert both date strings to datetime.date for accurate comparison
            transaction_date = getdate(transaction.get('date'))
            filter_date = getdate(date_filter)
            if transaction_date != filter_date:
                continue

        # Process Purchase transactions
        if transaction.get('status') == "Purchase":
            stock_balance.append({
                "shop_name": transaction["shop_name"],
                "item_code": transaction["item_name"],
                "in_qty": transaction["quantity"],
                "out_qty": 0,
                "balance": transaction["total"],  
                "voucher_name": transaction["id"],
                "date": transaction["date"]
            })

        # Process Sale transactions
        elif transaction.get('status') == "Sale":
            stock_balance.append({
                "shop_name": transaction["shop_name"],
                "item_code": transaction["item_name"],
                "in_qty": 0,
                "out_qty": -transaction["quantity"],  
                "balance": transaction["total"], 
                "voucher_name": transaction["id"],
                "date": transaction["date"]
            })

    return stock_balance