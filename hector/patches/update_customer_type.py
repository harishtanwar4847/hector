from __future__ import unicode_literals
import frappe

def execute():
    frappe.db.sql("""UPDATE `tabPrimary Customer Form` set customer_type = 'Direct Distributor' where customer_type = 'Direct Party'""")
    frappe.db.sql("""UPDATE `tabPrimary Customer Form` set asm_user = owner""")
    frappe.db.commit()