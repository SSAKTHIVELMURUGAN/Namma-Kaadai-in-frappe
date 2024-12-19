import frappe
from frappe.model.document import Document

class Transaction(Document):
    def on_cancel(self):
        if self.is_cancel:
            self.cancel_transaction()

    def cancel_transaction(self):
        frappe.db.set_value(
            'Transaction',
            {'id': self.id},  
            {'is_cancel': 1}  
        )
