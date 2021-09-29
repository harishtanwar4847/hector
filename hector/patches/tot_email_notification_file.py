import frappe
totFilePath =  "/assets/hector/files/Hector%20Beverages-General%20Terms%20and%20Conditions%20for%20Partners-.pdf"

def execute():
    doc = frappe.get_doc("Hector Settings")
    doc.tot_attachment = totFilePath
    doc.insert()
    frappe.db.commit()
