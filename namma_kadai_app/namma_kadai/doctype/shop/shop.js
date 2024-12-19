// Copyright (c) 2024, Sakthi and contributors
// For license information, please see license.txt

frappe.ui.form.on("Shop", {
    refresh(frm) {
        frm.add_custom_button('Add Investment Amount', () => {
            frappe.new_doc('Investment', {
                'shop_name': frm.doc.name,  
                'investment': 0,           
                'date': frappe.datetime.now_date()  
            });
        });
    },
});
