import frappe
from frappe.model.document import Document

class ShopCashFlow(Document):
    def on_cancel(self):
        if self.iscancelled:
            self.cancel_transaction()

    def cancel_transaction(self):
        frappe.db.set_value(
            'Shop CashFlow',
            {'transaction_type': self.transaction_type},  
            {'iscancelled': 1}  
        )
