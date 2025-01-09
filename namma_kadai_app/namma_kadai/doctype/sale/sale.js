//     // Copyright (c) 2024, Sakthi and contributors
//    // For license information, please see license.txt

    frappe.ui.form.on("Sale", {
        refresh(frm) {

            frm.add_custom_button(__("Data Export for Sale"), function () {
                let fields_meta_data = {}
                //get metadata
                meta_data = frappe.get_meta(frm.doc.doctype)
                //for parent
                fields_meta_data[`${frm.doc.doctype}_parent`] = get_sale_fields(meta_data);
                // for child table                
                fields_meta_data[`${frm.doc.name}_child`] = get_child_table_fields(meta_data);
                
                // for passing  parameter for dialog box
                show_dialog_data_export(fields_meta_data,frm);
                
                
            })
        },
    });

function get_sale_fields(meta_data){
    sale_field_list = []
    for(let key in meta_data.fields){
        const field_key = meta_data.fields[key]
        if(!field_key.hidden && field_key.fieldtype != 'Table'){
            sale_field_list.push({
                label: field_key.label,
                fieldname: field_key.fieldname,
                fieldtype: 'Check',
            });
        }
    }
    return sale_field_list;
}


function get_child_table_fields(meta_data){
    
    let child_table = meta_data.fields.filter(field => field.fieldtype === 'Table');

    let child_fields_meta_data = [];
    for (let i = 0; i < child_table.length; i++) {

        let child = child_table[i];
        let child_table_fields = frappe.get_meta(child.options).fields
            .filter(field => !field.hidden)
            .map(field => ({
                label: field.label,
                fieldname: `${child.options}.${field.fieldname}`,
                fieldtype: 'Check'  
            }));        
        child_fields_meta_data = child_fields_meta_data.concat(child_table_fields);
    }
    return child_fields_meta_data;
}

function show_dialog_data_export(fields_meta_data,frm) {
    // fields_meta_data into single array
    let fields = [];
    for (let key in fields_meta_data) {
        fields = fields.concat(fields_meta_data[key]);
    }

    let d = new frappe.ui.Dialog({
        title: 'Export Data',
        fields: fields, // pass as array
        size: 'large',
        primary_action_label: 'Submit',

        primary_action(values) {
            let selected_fields = [];

            for (let key in values) {
                if (values[key]) {
                    selected_fields.push(key);
                }
            }

            frappe.call({
                method: "namma_kadai_app.namma_kadai.doctype.sale.sale.data_export",
                args: {
                    selected_fields: selected_fields,
                    docname : frm.doc.name
                },
                callback: function (response) {
                    
                    const file_path = response.message;

                    if (file_path) {
                        show_download_mail(file_path,frm)
                    } else {
                        // If there was an issue with the export
                        frappe.msgprint({
                            message: __("There was an issue exporting the data. Please try again."),
                            indicator: 'red'
                        });
                    }
                    d.hide();
                }
            });
        }

    });

    d.show();
}

function show_download_mail(file_path,frm){
    let d = new frappe.ui.Dialog({
        title : 'Export Sucessfully',
        fields : [],
        size : 'small',
        primary_action_label: null,

        secondary_action_label: __("Download"),
        secondary_action(){
            download_file(file_path);
            d.hide()
        },
    });

        const footer = d.footer;
        const sendMailButton = $(`<button class="btn btn-secondary btn-sm ml-2">${__("Send Mail")}</button>`)
        .appendTo(footer)
        .click(function () {
            check_email(frm, file_path);
            d.hide();
        });

    d.show();
}

function download_file(file_url) {
    if (!file_url) {
        frappe.msgprint({
            message: __("File path is invalid or not provided."),
            indicator: 'red'
        });
        return;
    }
    // Create the full download URL
    const absoluteUrl = window.location.origin + file_url;

    // Create a temporary link element
    const link = document.createElement('a');
    link.href = absoluteUrl;
    link.download = file_url.split('/').pop();  // Extract filename from URL
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    frappe.msgprint({
        message: __("File downloaded successfully."),
        indicator: 'green'
    });
}


function check_email(frm,file_path){
    if  (frm.doc.customer_mail_id === undefined){
        let d = new frappe.ui.Dialog({
            title: 'Enter Customer Mail ID',
            fields: [
                {
                    label: 'Mail ID',
                    fieldname: 'new_customer_mail_id',
                    fieldtype: 'Data',
                    reqd:1
                },
            ],
            size: 'small', 
            primary_action_label: 'Send Mail',
            primary_action(values) {
                send_mail(frm, file_path, values.new_customer_mail_id)
                console.log(values.new_customer_mail_id);
                
                d.hide();
            }
        });
        
        d.show();
        
    }
    else{
        send_mail(frm, file_path,frm.doc.customer_mail_id)
    }
}


function send_mail(frm, file_path,recipients) {

    frappe.call({
        method: "namma_kadai_app.namma_kadai.doctype.sale.sale.send_email",
        args: {
            sender: 'sakthiteamkc@gmail.com',
            recipients: recipients,
            subject: `${frm.doc.docname}`,
            file_url: file_path,
        },
        callback: function(response) {
            if (response && response.message === "success") {
                frappe.msgprint({
                    title: "Success",
                    message: "Email sent successfully.",
                    indicator: "green",
                });
            }
            else if(response && response.message === "Email error") {
                frappe.msgprint({
                    title: "Error",
                    message: "Email ID is not valid",
                    indicator: "red",
                });
            }
            else {
                frappe.msgprint({
                    title: "Error",
                    message: "Failed to send the email. Please try again.",
                    indicator: "red",
                });
            }
        }
    });
}
