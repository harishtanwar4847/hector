import frappe
totFilePath = "/assets/hector/files/Hector Beverages-General Terms and Conditions for Partners-.pdf"

def execute():
    doc = frappe.get_doc("Hector Settings")
    doc.tot_attachment = totFilePath
    doc.insert()
    frappe.db.commit()
