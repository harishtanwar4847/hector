import frappe

def execute():
    server_type = frappe.get_site_config().server_type
    if server_type in ('Dev','UAT'):
        frappe.db.sql("""UPDATE `tabNotification` set sender = 'Notifications' where sender = 'Notificati'""")
        frappe.db.commit()