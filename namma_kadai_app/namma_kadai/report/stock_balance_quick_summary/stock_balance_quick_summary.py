import frappe

def execute(filters=None):
    columns = [
        {
            "fieldname": "shop_name", 
            "fieldtype": "Data",
            "label": "Shop Name", 
            "width": 150
        },
        {
            "fieldname": "item_name", 
            "fieldtype": "Data", 
            "label": "Item Name", 
            "width": 150
        },
        {
            "fieldname": "in_qty", 
            "fieldtype": "Int", 
            "label": "In Qty", 
            "width": 100
        },
        {
            "fieldname": "out_qty", 
            "fieldtype": "Int", 
            "label": "Out Qty", 
            "width": 100
        },
        {
            "fieldname": "balance", 
            "fieldtype": "Int", 
            "label": "Balance", 
            "width": 100
        }
    ]
    
    data = get_transactions(filters)
    
    return columns, data

def get_transactions(filters):
    transactions_data = []
    shop_name = filters.get("shop_name")
    item_name = filters.get("item_name")  

    filter_conditions = {}
    
    if shop_name:
        filter_conditions["shop_name"] = shop_name
    if item_name:
        filter_conditions["item_name"] = item_name

    transactions = frappe.get_list("Transaction", filters=filter_conditions, fields=["item_name", "quantity", "status"])

    item_qty = {}

    for transaction in transactions:
        item_name = transaction['item_name']
        quantity = transaction['quantity']

        if item_name not in item_qty:
            item_qty[item_name] = {"in_qty": 0, "out_qty": 0}

        if quantity > 0:
            item_qty[item_name]["in_qty"] += quantity  
        elif quantity < 0:
            item_qty[item_name]["out_qty"] += abs(quantity)  

    for item_name, qty in item_qty.items():
        transactions_data.append({
            "item_name": item_name,
            "in_qty": qty["in_qty"],  
            "out_qty": qty["out_qty"],  
            "shop_name": shop_name, 
            "balance": qty["in_qty"] - qty["out_qty"]  
        })
        
    return transactions_data
