# Copyright (c) 2021, Atrina Technologies Pvt Ltd and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.core.doctype.communication.email import make
# from frappe.core.doctype.communication.email import sendmail


class CustomerForm(Document):
	# pass
	def on_update(self):
		try:
			print("\n\n\nI am from customer form\n\n\n")
			# print("The self.name is \n\n",self.name)
			asm_rsm = [x for x in frappe.db.sql("""select shm.asm_user,shm.rsm_user from `tabCustomer Form` cf inner join `tabSales Hierarchy Mapping` shm on shm.asm_user = cf.owner where cf.name = '{}'""".format(self.name), as_list=1)]
			asm_rsm_name = [x for x in frappe.db.sql("""select shm.asm_name,shm.rsm_name from `tabCustomer Form` cf inner join `tabSales Hierarchy Mapping` shm on shm.asm_user = cf.owner where cf.name = '{}'""".format(self.name), as_list=1)]
			cma_list =[x[0] for x in frappe.db.sql("""select u.name from `tabUser` u inner join `tabHas Role` hr on hr.parent = u.name where hr.role = 'Customer Master Approver'""", as_list=1)]
			cma_name =[x[0] for x in frappe.db.sql("""select u.full_name from `tabUser` u inner join `tabHas Role` hr on hr.parent = u.name where hr.role = 'Customer Master Approver'""", as_list=1)]
			print("The asm is ",asm_rsm[0][0])
			print("The rsm is ",asm_rsm[0][1])
			print("The cma is ",cma_list)



			if self.workflow_state == 'Pending for RSM Approval':
				msg="""Hello {},<br><br>
				You have received a request for customer creation approval from {} for the customer {}.<br><br>
				Kindly login to apps.myhector.com for the approval process.<br><br><br>
				Regards,<br>
				Hector Beverages""".format(asm_rsm_name[0][1],asm_rsm_name[0][0],self.customer_name)
				frappe.sendmail(subject="Customer Creation: Pending for RSM Approval", content=msg, recipients = '{}'.format(asm_rsm[0][1]),sender="Notification@hectorbeverages.com")
				print("\n email sent \n")

			if self.workflow_state == 'Resent for RSM Approval &nbsp;':
				msg="""Hello {},<br><br>
				You have received a request for customer creation approval from {} for the customer {}.<br><br>
				Kindly login to apps.myhector.com for the approval process.<br><br><br>
				Regards,<br>
				Hector Beverages""".format(asm_rsm_name[0][1],asm_rsm_name[0][0],self.customer_name)
				frappe.sendmail(subject="Customer Creation: Resent for RSM Approval", content=msg, recipients = '{}'.format(asm_rsm[0][1]),sender="Notification@hectorbeverages.com")
				print("\n email sent \n")

			if self.workflow_state == 'Pending for Master Team Approval':
				for i in range(len(cma_list)):
					msg="""Hello {},<br><br>
					You have received a request for customer creation from {} for the customer {}.<br><br>
					Kindly login to apps.myhector.com for the approval process.<br><br><br>
					Regards,<br>
					Hector Beverages""".format(frappe.get_doc('User', cma_list[i]).full_name,asm_rsm_name[0][1],self.customer_name)
					frappe.sendmail(subject="Customer Creation: Pending for Master Data Team Approval", content=msg, recipients = '{}'.format(cma_list[i]), sender="Notification@hectorbeverages.com")
					print("\n email sent \n")

			if self.workflow_state == 'Resent for Master Team Approval &nbsp;':
				for i in range(len(cma_list)):
					msg="""Hello {},<br><br>
					You have received a request for customer creation from {} for the customer {}.<br><br>
					Kindly login to apps.myhector.com for the approval process.<br><br><br>
					Regards,<br>
					Hector Beverages""".format(frappe.get_doc('User', cma_list[i]).full_name,asm_rsm_name[0][1],self.customer_name)
					frappe.sendmail(subject="Customer Creation: Resent for Master Data Team Approval", content=msg, recipients = '{}'.format(cma_list[i]), sender="Notification@hectorbeverages.com")
					print("\n email sent \n")

			if self.workflow_state == 'Requested for More Details by RSM':
				msg="""Hello {},<br><br>
				You have received a request for more information in customer creation from {} for the customer {}.<br><br>
				Kindly login to apps.myhector.com for the approval process.<br><br><br>
				Regards,<br>
				Hector Beverages""".format(asm_rsm_name[0][0],asm_rsm_name[0][1],self.customer_name)
				frappe.sendmail(subject="Customer Creation: Requested for More Details by RSM", content=msg, recipients = '{}'.format(asm_rsm[0][0]), sender="Notification@hectorbeverages.com")
				print("\n email sent \n")

			if self.workflow_state == 'Requested for More Details by Master Team':
				msg="""Hello {},<br><br>
				You have received a request for more information in customer creation from {} for the customer {}.<br><br>
				Kindly login to apps.myhector.com for the approval process.<br><br><br>
				Regards,<br>
				Hector Beverages""".format(asm_rsm_name[0][0],cma_name[0][0],self.customer_name)
				frappe.sendmail(subject="Customer Creation: Requested for More Details by Master Data Team", content=msg, recipients = '{}'.format(asm_rsm[0][0]), sender="Notification@hectorbeverages.com")
				print("\n email sent \n")

			if self.workflow_state == 'Rejected by RSM':
				msg="""Hello {},<br><br>
				Your request for customer creation for customer {} has been rejected by {}.<br><br>
				Kindly check reason for rejection in website apps.myhector.com<br><br><br>
				Regards,<br>
				Hector Beverages""".format(asm_rsm_name[0][0],self.customer_name,asm_rsm_name[0][1])
				frappe.sendmail(subject="Customer Creation Rejected : {}".format(self.customer_name), content=msg, recipients = '{}'.format(asm_rsm[0][0]), sender="Notification@hectorbeverages.com")
				print("\n email sent \n")

			if self.workflow_state == 'TOT Rejected by Customer &nbsp;':
				msg="""Hello Team,<br><br>
				Your request for customer creation has been rejected.<br><br>
				Kindly check reason for rejection in website apps.myhector.com<br><br><br>
				Regards,<br>
				Hector Beverages"""
				frappe.sendmail(subject="Customer Creation Rejected : {}".format(self.customer_name), content=msg, recipients = [asm_rsm[0][0]] + [asm_rsm[0][1]] + cma_list, sender="Notification@hectorbeverages.com")
				print("\n email sent \n")

			if self.workflow_state == 'Customer Approved':
				msg="""Hello Team,<br><br>
				Your request for customer creation has been approved. And New Customer Code is {} for {}.<br><br>
				Link- apps.myhector.com<br><br><br>
				Regards,<br>
				Hector Beverages""".format(self.customer_id,self.customer_name)
				frappe.sendmail(subject="Customer Creation Completed : {} : {}".format(self.customer_id,self.customer_name), content=msg, recipients = '{},{}'.format(asm_rsm[0][0], asm_rsm[0][1]), sender="Notification@hectorbeverages.com")
				print("\n email sent \n")
		except:
			frappe.throw("Please add ASM in Sales Hierarchy Mapping")
