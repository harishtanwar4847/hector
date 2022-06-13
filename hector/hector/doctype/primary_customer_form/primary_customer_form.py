# Copyright (c) 2021, Atrina Technologies Pvt Ltd and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.core.doctype.communication.email import make
# from frappe.core.doctype.communication.email import sendmail

class PrimaryCustomerForm(Document):
	# pass
	def on_update(self):
		try:
			print("\n\n\nI am from customer form\n\n\n")
			asm_rsm = [x for x in frappe.db.sql("""select shm.asm_user,shm.rsm_user from `tabPrimary Customer Form` cf inner join `tabSales Hierarchy Mapping` shm on shm.asm_user = cf.asm_user where cf.name = '{}'""".format(self.name), as_list=1)]
			asm_rsm_name = [x for x in frappe.db.sql("""select shm.asm_name,shm.rsm_name from `tabPrimary Customer Form` cf inner join `tabSales Hierarchy Mapping` shm on shm.asm_user = cf.asm_user where cf.name = '{}'""".format(self.name), as_list=1)]
			nsm_user = [x for x in frappe.db.sql("""select shm.nsm_user from `tabPrimary Customer Form` cf inner join `tabSales Hierarchy Mapping` shm on shm.asm_user = cf.asm_user where cf.name = '{}'""".format(self.name), as_list=1)]
			nsm_name = [x for x in frappe.db.sql("""select shm.nsm_name from `tabPrimary Customer Form` cf inner join `tabSales Hierarchy Mapping` shm on shm.asm_user = cf.asm_user where cf.name = '{}'""".format(self.name), as_list=1)]
			pcma_list =[x[0] for x in frappe.db.sql("""select u.name from `tabUser` u inner join `tabHas Role` hr on hr.parent = u.name where hr.role = 'Primary Customer Master Approver'""", as_list=1)]
			pcma_name =[x[0] for x in frappe.db.sql("""select u.full_name from `tabUser` u inner join `tabHas Role` hr on hr.parent = u.name where hr.role = 'Primary Customer Master Approver'""", as_list=1)]
			
			print("The asm is ",asm_rsm[0][0])
			print("The rsm is ",asm_rsm[0][1])
			print("The pcma is ",pcma_list)
				
			if self.workflow_state == 'Pending for NSM Approval':
				msg="""Hello {},<br><br>
				You have received a request for Primary customer creation approval from {} for the customer {}.<br><br>
				Kindly login to apps.myhector.com for the approval process.<br><br><br>
				Regards,<br>
				Hector Beverages""".format(nsm_name[0][0],asm_rsm_name[0][0],self.customer_name)
				frappe.sendmail(subject="Customer Creation: Pending for NSM Approval", content=msg, recipients = '{}'.format(nsm_user[0][0]),sender="Notification@hectorbeverages.com")
				print("\n email sent \n")

			if self.workflow_state == 'Pending For Primary Customer Additional Details':
				msg="""Hello {},<br><br>
				You have received a request to fill Primary Customer Additional Details for the customer {}.<br><br>
				Kindly login to apps.myhector.com for the approval process.<br><br><br>
				Regards,<br>
				Hector Beverages""".format(asm_rsm_name[0][0],self.customer_name)
				frappe.sendmail(subject="Customer Creation: Pending For Primary Customer Additional Details", content=msg, recipients = '{}'.format(asm_rsm[0][0]), sender="Notification@hectorbeverages.com")
				print("\n email sent \n")

			if self.workflow_state == 'Resent for NSM Approval':
				msg="""Hello {},<br><br>
				You have received a request for Primary customer creation approval from {} for the customer {}.<br><br>
				Kindly login to apps.myhector.com for the approval process.<br><br><br>
				Regards,<br>
				Hector Beverages""".format(nsm_name[0][0],asm_rsm_name[0][0],self.customer_name)
				frappe.sendmail(subject="Customer Creation: Resent for NSM Approval", content=msg, recipients = '{}'.format(nsm_user[0][0]),sender="Notification@hectorbeverages.com")
				print("\n email sent \n")

			if self.workflow_state == 'Pending with Primary Master Processing':
				for i in range(len(pcma_list)):
					msg="""Hello {},<br><br>
					You have received a request for Primary customer creation from {} for the customer {}.<br><br>
					Kindly login to apps.myhector.com for the approval process.<br><br><br>
					Regards,<br>
					Hector Beverages""".format(frappe.get_doc('User', pcma_list[i]).full_name,nsm_name[0][0],self.customer_name)
					frappe.sendmail(subject="Customer Creation: Pending with Primary Master Processing", content=msg, recipients = '{}'.format(pcma_list[i]), sender="Notification@hectorbeverages.com")
					print("\n email sent \n")

			if self.workflow_state == 'Resent for Primary Master Processing':
				for i in range(len(pcma_list)):
					msg="""Hello {},<br><br>
					You have received a request for Primary customer creation from {} for the customer {}.<br><br>
					Kindly login to apps.myhector.com for the approval process.<br><br><br>
					Regards,<br>
					Hector Beverages""".format(frappe.get_doc('User', pcma_list[i]).full_name,nsm_name[0][0],self.customer_name)
					frappe.sendmail(subject="Customer Creation: Resent for Primary Master Processing", content=msg, recipients = '{}'.format(pcma_list[i]), sender="Notification@hectorbeverages.com")
					print("\n email sent \n")

			if self.workflow_state == 'Requested for More Details by NSM':
				msg="""Hello {},<br><br>
				You have received a request for more information in Primary customer creation from {} for the customer {}.<br><br>
				Kindly login to apps.myhector.com for the approval process.<br><br><br>
				Regards,<br>
				Hector Beverages""".format(asm_rsm_name[0][0],nsm_name[0][0],self.customer_name)
				frappe.sendmail(subject="Customer Creation: Requested for More Details by NSM", content=msg, recipients = '{}'.format(asm_rsm[0][0]), sender="Notification@hectorbeverages.com")
				print("\n email sent \n")

			if self.workflow_state == 'Requested for More Details by Primary Master Team':
				msg="""Hello {},<br><br>
				You have received a request for more information in Primary customer creation from {} for the customer {}.<br><br>
				Kindly login to apps.myhector.com for the approval process.<br><br><br>
				Regards,<br>
				Hector Beverages""".format(asm_rsm_name[0][0],pcma_name[0],self.customer_name)
				frappe.sendmail(subject="Customer Creation: Requested for More Details by Primary Master Data Team", content=msg, recipients = '{}'.format(asm_rsm[0][0]), sender="Notification@hectorbeverages.com")
				print("\n email sent \n")

			if self.workflow_state == 'Rejected by ASM':
				msg="""Hello,<br><br>
				Your request for Primary customer creation for customer {} has been rejected by {}.<br><br>
				Kindly check reason for rejection in website apps.myhector.com<br><br><br>
				Regards,<br>
				Hector Beverages""".format(self.customer_name,asm_rsm_name[0][0])
				frappe.sendmail(subject="Customer Creation Rejected : {}".format(self.customer_name), content=msg, recipients = '{}'.format(self.owner), sender="Notification@hectorbeverages.com")
				print("\n email sent \n")

			if self.workflow_state == 'Rejected by NSM':
				msg="""Hello,<br><br>
				Your request for Primary customer creation for customer {} has been rejected by {}.<br><br>
				Kindly check reason for rejection in website apps.myhector.com<br><br><br>
				Regards,<br>
				Hector Beverages""".format(self.customer_name,asm_rsm_name[0][1])
				frappe.sendmail(subject="Customer Creation Rejected : {}".format(self.customer_name), content=msg, recipients = '{}'.format(self.owner), sender="Notification@hectorbeverages.com")
				print("\n email sent \n")

			if self.workflow_state == 'Rejected by NSM':
				msg="""Hello {},<br><br>
				Your request for Primary customer creation for customer {} has been rejected by {}.<br><br>
				Kindly check reason for rejection in website apps.myhector.com<br><br><br>
				Regards,<br>
				Hector Beverages""".format(asm_rsm_name[0][0],self.customer_name,nsm_name[0][0])
				frappe.sendmail(subject="Customer Creation Rejected : {}".format(self.customer_name), content=msg, recipients = '{}'.format(asm_rsm[0][0]), sender="Notification@hectorbeverages.com")
				print("\n email sent \n")

			if self.workflow_state == 'TOT Rejected by Customer':
				msg="""Hello Team,<br><br>
				Your request for Primary customer creation has been rejected.<br><br>
				Kindly check reason for rejection in website apps.myhector.com<br><br><br>
				Regards,<br>
				Hector Beverages"""
				frappe.sendmail(subject="Customer Creation Rejected : {}".format(self.customer_name), content=msg, recipients = [asm_rsm[0][0]] + [nsm_user[0][0]] + pcma_list, sender="Notification@hectorbeverages.com")
				print("\n email sent \n")

			if self.workflow_state == 'Primary Customer Approved':
				msg="""Hello Team,<br><br>
				Your request for Primary customer creation has been approved. And New Customer Code is {} for {}.<br><br>
				Link- apps.myhector.com<br><br><br>
				Regards,<br>
				Hector Beverages""".format(self.customer_id,self.customer_name)
				frappe.sendmail(subject="Customer Creation Completed : {} : {}".format(self.customer_id,self.customer_name), content=msg, recipients = '{},{}'.format(asm_rsm[0][0], nsm_user[0][0]), sender="Notification@hectorbeverages.com")
				print("\n email sent \n")

		except:
			frappe.throw("Please add ASM in Sales Hierarchy Mapping")