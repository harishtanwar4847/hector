from __future__ import unicode_literals
import frappe

def execute():
    frappe.db.sql("""UPDATE `tabQuality Issue` set manufacturing_plant = 'HBPL@Manesar' where manufacturing_plant = 'Manesar'""")
    frappe.db.sql("""UPDATE `tabQuality Issue` set manufacturing_plant = 'HBPL@Mysore' where manufacturing_plant = 'Mysore'""")
    frappe.db.sql("""UPDATE `tabQuality Issue` set manufacturing_plant = 'PAITHAN@ Aurangabad' where manufacturing_plant = 'Paithan'""")
    frappe.db.sql("""UPDATE `tabQuality Issue` set manufacturing_plant = 'VSA FOODS @ Dindigul' where manufacturing_plant = 'VSA'""")
    frappe.db.sql("""UPDATE `tabQuality Issue` set manufacturing_plant = 'KOVAI @ Coimbatore' where manufacturing_plant = 'Kowai'""")
    frappe.db.sql("""UPDATE `tabQuality Issue` set manufacturing_plant = 'SDDPL@Baramati' where manufacturing_plant = 'Baramati'""")
    frappe.db.sql("""UPDATE `tabQuality Issue` set manufacturing_plant = 'SDDPL@ Fazilka' where manufacturing_plant = 'Fazilika'""")
    frappe.db.sql("""UPDATE `tabQuality Issue` set manufacturing_plant = 'VINAYAK BEVERAGES@ Hyderabad' where manufacturing_plant = 'Vinyak'""")
    frappe.db.sql("""UPDATE `tabQuality Issue` set manufacturing_plant = 'BD FOOD@ Varanasi' where manufacturing_plant = 'BD Foods'""")
    frappe.db.sql("""UPDATE `tabQuality Issue` set manufacturing_plant = 'HFL @Mysore' where manufacturing_plant = 'ATC'""")

    frappe.db.commit()
