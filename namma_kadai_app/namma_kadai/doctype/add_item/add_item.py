# Copyright (c) 2024, Sakthi and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class AddItem(Document):
	def validate(self):
		self.quantity = self.quantity
		self.rate = self.rate
		self.amount = self.quantity * self.rate
