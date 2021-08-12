# Copyright (c) 2021, Atrina Technologies Pvt Ltd and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.core.doctype.communication.email import make
# from frappe.core.doctype.communication.email import sendmail


class CustomerForm(Document):
	# pass
	def on_update(self):
		print("\n\n\nI am from customer form\n\n\n")
		# print("The self.name is \n\n",self.name)
		asm_rsm = [x for x in frappe.db.sql("""select shm.asm_user,shm.rsm_user from `tabCustomer Form` cf inner join `tabSales Hierarchy Mapping` shm on shm.asm_user = cf.owner where cf.name = '{}'""".format(self.name), as_list=1)]
		cma_list =[x for x in frappe.db.sql("""select u.name from `tabUser` u inner join `tabHas Role` hr on hr.parent = u.name where hr.role = 'Customer Master Approver'""", as_list=1)]
		print("The asm is ",asm_rsm[0][0])
		print("The rsm is ",asm_rsm[0][1])
		print("The cma is ",cma_list[0][0])
	


		if self.workflow_state == 'Pending for RSM Approval':
			msg="""Hello {},<br>
			Pending RSM Approval for customer {}<br>
			Thankyou""".format(asm_rsm[0][1],self.customer_name)
			frappe.sendmail(subject="Pending for RSM Approval", content=msg, recipients = '{}'.format(asm_rsm[0][1]),sender="Notification@hectorbeverages.com")
			print("\n email sent \n")

		if self.workflow_state == 'Resent for RSM Approval &nbsp;':
			msg="""Hello {},<br>
			Resent for RSM Approval for customer {}<br>
			Thankyou""".format(asm_rsm[0][1],self.customer_name)
			frappe.sendmail(subject="Resent for RSM Approval", content=msg, recipients = '{}'.format(asm_rsm[0][1]),sender="Notification@hectorbeverages.com")
			print("\n email sent \n")
		
		if self.workflow_state == 'Pending for Master Team Approval':
			msg="""Hello {},<br>
			Pending for Master Team Approval for customer {}<br>
			Thankyou""".format(cma_list[0][0],self.customer_name)
			frappe.sendmail(subject="Pending for Master Team Approval", content=msg, recipients = '{}'.format(cma_list[0][0]), sender="Notification@hectorbeverages.com")
			print("\n email sent \n")
		
		if self.workflow_state == 'Resent for Master Team Approval &nbsp;':
			msg="""Hello {},<br>
			Resent for Master Team Approval for customer {}<br>
			Thankyou""".format(cma_list[0][0],self.customer_name)
			frappe.sendmail(subject="Resent for Master Team Approval", content=msg, recipients = '{}'.format(cma_list[0][0]), sender="Notification@hectorbeverages.com")
			print("\n email sent \n")

		if self.workflow_state == 'Requested for More Details by RSM':
			msg="""Hello {},<br>
			Requested for More Details by RSM {} for customer {}<br>
			Thankyou""".format(asm_rsm[0][0],asm_rsm[0][1],self.customer_name)
			frappe.sendmail(subject="Requested for More Details by RSM", content=msg, recipients = '{}'.format(asm_rsm[0][0]), sender="Notification@hectorbeverages.com")
			print("\n email sent \n")

		if self.workflow_state == 'Requested for More Details by Master Team':
			msg="""Hello {},<br>
			Requested for More Details by Master Team {} for customer {}<br>
			Thankyou""".format(asm_rsm[0][0],cma_list[0][0],self.customer_name)
			frappe.sendmail(subject="Requested for More Details by Master Team", content=msg, recipients = '{}'.format(asm_rsm[0][0]), sender="Notification@hectorbeverages.com")
			print("\n email sent \n")

		if self.workflow_state == 'Rejected by RSM':
			msg="""Hello {},<br>
			Customer {} Rejected by RSM {}<br>
			Thankyou""".format(asm_rsm[0][0],self.customer_name,asm_rsm[0][1])
			frappe.sendmail(subject="Rejected by RSM", content=msg, recipients = '{}'.format(asm_rsm[0][0]), sender="Notification@hectorbeverages.com")
			print("\n email sent \n")
		
		if self.workflow_state == 'TOT Rejected by Customer &nbsp;':
			msg="""Hello,<br>
			TOT Rejected by Customer {}<br>
			Thankyou""".format(self.customer_name)
			frappe.sendmail(subject="TOT Rejected by Customer", content=msg, recipients = '{},{},{}'.format(asm_rsm[0][0], asm_rsm[0][1], cma_list[0][0]), sender="Notification@hectorbeverages.com")
			print("\n email sent \n")
		