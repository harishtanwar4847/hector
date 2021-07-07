# Copyright (c) 2021, Atrina Technologies Pvt Ltd and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.core.doctype.communication.email import make
class CustomerForm(Document):
	def on_update(self):
		asm_rsm = [x[0] for x in frappe.db.sql("""select shm.asm_user,shm.rsm_user from `tabCustomer Form` cf inner join `tabSales Hierarchy Mapping` shm on shm.asm_user = cf.owner where cf.name = '{}'""".format(self.name), as_dict=0)]
		cma_list =[x[0] for x in frappe.db.sql("""select u.name from `tabUser` u inner join `tabHas Role` hr on hr.parent = u.name where hr.role = 'Customer Master Approver'""", as_dict=0)]

		if self.workflow_state == 'Pending for RSM Approval' or self.workflow_state == 'Resent for RSM Approval &nbsp;':
			msg="""Hello {},<br>
			Pending RSM Approval for customer {}.<br>
			Thankyou""".format(asm_rsm[0],self.customer_name)
			make(subject="Pending for RSM Approval", content=msg, recipients = '{},{},{}'.format(asm_rsm[0],asm_rsm[1],cma_list[0]), send_email=True, sender="Notification@hectorbeverages.com")

		if self.workflow_state == 'Resent for Master Team Approval &nbsp;':
			msg="""Hello {},<br>
			Resent for Master Team Approval for customer {}.<br>
			Thankyou""".format(cma_list[0],self.customer_name)
			make(subject="Pending for RSM Approval", content=msg, recipients = '{},{}'.format(asm_rsm[0],cma_list[0]), send_email=True, sender="Notification@hectorbeverages.com")

		if self.workflow_state == 'Requested for More Details by RSM':
			msg="""Hello {},<br>
			Requested for More Details by RSM {} for customer {}.<br>
			Thankyou""".format(asm_rsm[0],asm_rsm[1],self.customer_name)
			make(subject="Pending for RSM Approval", content=msg, recipients = '{},{},{}'.format(asm_rsm[0],asm_rsm[1],cma_list[0]), send_email=True, sender="Notification@hectorbeverages.com")
		
		if self.workflow_state == 'Requested for More Details by Master Team':
			msg="""Hello {},<br>
			Requested for More Details by Master Team {} for customer {}.<br>
			Thankyou""".format(asm_rsm[0],cma_list[0],self.customer_name)
			make(subject="Pending for RSM Approval", content=msg, recipients = '{},{},{}'.format(asm_rsm[0],asm_rsm[1],cma_list[0],self.modified_by), send_email=True, sender="Notification@hectorbeverages.com")
		
