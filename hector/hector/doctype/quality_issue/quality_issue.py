# Copyright (c) 2021, Atrina Technologies Pvt Ltd and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime

class QualityIssue(Document):
	def before_save(self):
		skuDetails = self.sku_details
		currentDate = frappe.utils.today()
		date_format = "%Y-%m-%d"
		for i in range(len(skuDetails)):
			todayDate = datetime.strptime(currentDate, date_format)
			documentDate = frappe.utils.get_datetime(skuDetails[i].mgf_date).strftime(date_format)
			documentDateStr = datetime.strptime(documentDate, date_format)
			daysDiffrence = (todayDate - documentDateStr).days

			#for selecting dates from past
			if int(daysDiffrence) <= 0 :
				frappe.throw("Please select correct manufacturing date")

	def on_update(self):
		rsmEmail = self.rsm_name
		asmEmail = self.asm_name
		requestorSalesTeam = self.email_address_of_requestor_from_sales_team
		complaintTeamEmail = self.owner
		complaintTeamName = frappe.get_doc('User', complaintTeamEmail).full_name
		physicalVerificationTeamEmail = self.physicalremote_verification_executive_email
		physicalVerificationTeamName = frappe.get_doc('User',physicalVerificationTeamEmail).full_name
		financeTeamEmail = [x for x in frappe.db.sql("""select u.name from `tabUser` u inner join `tabHas Role` hr on hr.parent = u.name where hr.role = 'Finance Team'""", as_list=1)]
		financeTeamEmail.remove(['Administrator'])
		financeTeamEmail = financeTeamEmail[0][0]
		financeTeamName = [x for x in frappe.db.sql("""select u.full_name from `tabUser` u inner join `tabHas Role` hr on hr.parent = u.name where hr.role = 'Finance Team'""", as_list=1)]
		financeTeamName.remove(['Administrator'])
		financeTeamName = financeTeamName[0][0]
		qualityHeadEmail = [x for x in frappe.db.sql("""select u.name from `tabUser` u inner join `tabHas Role` hr on hr.parent = u.name where hr.role = 'Quality Head'""", as_list=1)]
		qualityHeadEmail.remove(['Administrator'])
		qualityHeadEmail = qualityHeadEmail[0][0]
		qualityHeadName = [x for x in frappe.db.sql("""select u.full_name from `tabUser` u inner join `tabHas Role` hr on hr.parent = u.name where hr.role = 'Quality Head'""", as_list=1)]
		qualityHeadName.remove(['Administrator'])
		qualityHeadName = qualityHeadName[0][0]


		if self.workflow_state == 'Pending for Physical Verification Officer Approval':
			#For sendng email to sales team of customer complaint registered
			msg="""Hello {},<br><br>
				Your Complaint has been registered.<br><br>
				Kindly login to apps.myhector.com for the approval process.<br><br><br>
				Regards,<br>
				Hector Beverages""".format(self.customer_name)
			frappe.sendmail(subject="Customer Complaints: Complaint Registered", content=msg,recipients = '{}'.format(requestorSalesTeam), cc = '{},{}'.format(rsmEmail, asmEmail),expose_recipients="header", sender="Notification@hectorbeverages.com")
			print("\n email sent \n")
			#For sending approval email to Physical Verification Officer
			msg="""Hello {},<br><br>
			You have received a request for quality complaint from {} for the customer {}.<br><br>
			Kindly login to apps.myhector.com for the approval process.<br><br><br>
			Regards,<br>
			Hector Beverages""".format(physicalVerificationTeamName, complaintTeamName, self.customer_name)
			frappe.sendmail(subject="Customer Complaints: Pending for Quality Team Approval", content=msg, recipients = '{}'.format(physicalVerificationTeamEmail),sender="Notification@hectorbeverages.com")
			print("\n email sent \n")

		if self.workflow_state == 'Resent for Physical Verification Officer Approval':
			msg="""Hello {},<br><br>
			You have received a request for complaint team approval from {} for the customer {}.<br><br>
			Kindly login to apps.myhector.com for the approval process.<br><br><br>
			Regards,<br>
			Hector Beverages""".format(physicalVerificationTeamName, complaintTeamName, self.customer_name)
			frappe.sendmail(subject="Customer Complaints: Resent for Phyical Verification Officer Approval", content=msg, recipients = '{}'.format(physicalVerificationTeamEmail),sender="Notification@hectorbeverages.com")
			print("\n email sent \n")

		if self.workflow_state == 'Rejected by Physical Verification Officer':
			msg="""Hello {},<br><br>
			You have received a request is rejected by {} for the customer {}.<br><br>
			Kindly login to apps.myhector.com for the approval process.<br><br><br>
			Regards,<br>
			Hector Beverages""".format(complaintTeamName, physicalVerificationTeamName, self.customer_name)
			frappe.sendmail(subject="Customer Complaints: Rejected by Physical Verification Officer", content=msg, recipients = '{}'.format(complaintTeamEmail),sender="Notification@hectorbeverages.com")
			print("\n email sent \n")

		if self.workflow_state == 'Requested for More Details by Physical Verification Officer':
			msg="""Hello {},<br><br>
			You have received a request for more details from {} for the customer {}.<br><br>
			Kindly login to apps.myhector.com for the approval process.<br><br><br>
			Regards,<br>
			Hector Beverages""".format(complaintTeamName, physicalVerificationTeamName, self.customer_name)
			frappe.sendmail(subject="Customer Complaints: Requested for More Details by Physical Verification Officer", content=msg, recipients = '{}'.format(complaintTeamEmail),sender="Notification@hectorbeverages.com")
			print("\n email sent \n")

		if self.workflow_state == 'Requested for More Details by Finance Team':
			msg="""Hello {},<br><br>
			You have received a request for more details from {} for the customer {}.<br><br>
			Kindly login to apps.myhector.com for the approval process.<br><br><br>
			Regards,<br>
			Hector Beverages""".format(complaintTeamName, financeTeamName, self.customer_name)
			frappe.sendmail(subject="Customer Complaints: Requested for More Details by Finance Team", content=msg, recipients = '{}'.format(complaintTeamEmail),sender="Notification@hectorbeverages.com")
			print("\n email sent \n")

		if self.workflow_state == 'Rejected by Finance Team':
			msg="""Hello Team,<br><br>
			Your request for quality team approval is rejected by {} for the customer {}.<br><br>
			Kindly login to apps.myhector.com for the approval process.<br><br><br>
			Regards,<br>
			Hector Beverages""".format(financeTeamName, self.customer_name)
			frappe.sendmail(subject="Customer Complaints: Rejected by Finance Team", content=msg, recipients = '{},{}'.format(complaintTeamEmail, physicalVerificationTeamEmail),sender="Notification@hectorbeverages.com")
			print("\n email sent \n")

		if self.workflow_state == 'Pending for Finance Team Approval':
			msg="""Hello {},<br><br>
			You have received a request for finance team approval from {} for the customer {}.<br><br>
			Kindly login to apps.myhector.com for the approval process.<br><br><br>
			Regards,<br>
			Hector Beverages""".format(financeTeamName, physicalVerificationTeamName, self.customer_name)
			frappe.sendmail(subject="Customer Complaints: Pending for Finance Team Approval", content=msg, recipients = '{}'.format(financeTeamEmail),sender="Notification@hectorbeverages.com")
			print("\n email sent \n")

		if self.workflow_state == 'Resent for Finance Team Approval':
			msg="""Hello {},<br><br>
			You have received a request for finance team approval from {} for the customer {}.<br><br>
			Kindly login to apps.myhector.com for the approval process.<br><br><br>
			Regards,<br>
			Hector Beverages""".format(financeTeamName, complaintTeamName, self.customer_name)
			frappe.sendmail(subject="Customer Complaints: Resent for Finance Team Approval", content=msg, recipients = '{}'.format(financeTeamEmail),sender="Notification@hectorbeverages.com")
			print("\n email sent \n")

		if self.workflow_state == 'RCA Approved':
			msg="""Hello Team,<br><br>
			You have received a request for quality team approval for the customer {} is approved.<br><br>
			Kindly login to apps.myhector.com for the approval process.<br><br><br>
			Regards,<br>
			Hector Beverages""".format(self.customer_name)
			frappe.sendmail(subject="Customer Complaints: RCA Approved", content=msg, recipients = '{},{},{}'.format(complaintTeamEmail, physicalVerificationTeamEmail, financeTeamEmail),sender="Notification@hectorbeverages.com")
			print("\n email sent \n")

		if self.workflow_state == 'Pending for RCA Details' :
			doc = frappe.get_doc('Quality Issue',self.name)
			skuDetails = self.sku_details
			currentDate = frappe.utils.today()
			date_format = "%Y-%m-%d"
			closeIssue = 0
			for i in range(len(skuDetails)):
				todayDate = datetime.strptime(currentDate, date_format)
				documentDate = frappe.utils.get_datetime(skuDetails[i].mgf_date).strftime(date_format)
				documentDateStr = datetime.strptime(documentDate, date_format)
				daysDiffrence = (todayDate - documentDateStr).days

				#for Quantity less than 100 pouches
				if int(skuDetails[i].quantity_in_pieces) < 100 :
					closeIssue = 1
					# self.close_issue = 1
					frappe.db.set_value('Quality Issue', self.name, 'close_issue', 1)


				#for diffrence between 2 dates greater than 3 months
				if int(daysDiffrence) > 90 :
					closeIssue = 1
					# self.close_issue = 1
					frappe.db.set_value('Quality Issue', self.name, 'close_issue', 1)


			# self.save()
			# frappe.db.commit()
			if closeIssue :
				# frappe.msgprint('for Quantity less than 100 pouches')
				frappe.db.set_value('Quality Issue', self.name, 'workflow_state', 'Issue Closed')
				msg="""Hello Team,<br><br>
				You have received a request for quality team approval for the customer {} is closed.<br><br>
				Kindly login to apps.myhector.com for the approval process.<br><br><br>
				Regards,<br>
				Hector Beverages""".format(self.customer_name)
				frappe.sendmail(subject="Customer Complaints: Issue Closed", content=msg, recipients = '{},{},{}'.format(complaintTeamEmail,physicalVerificationTeamEmail,financeTeamEmail),sender="Notification@hectorbeverages.com")
				print("\n email sent \n")
				self.reload()
				# frappe.db.commit()

			else :
				msg="""Hello {},<br><br>
				You have received a request for quality team approval for the customer {}.<br><br>
				Kindly login to apps.myhector.com for the approval process.<br><br><br>
				Regards,<br>
				Hector Beverages""".format(physicalVerificationTeamName, self.customer_name)
				frappe.sendmail(subject="Customer Complaints: Pending for RCA Details", content=msg, recipients = '{}'.format(physicalVerificationTeamEmail),sender="Notification@hectorbeverages.com")
				print("\n email sent \n")

			#For sendng email to sales team of credit note raised process
			msg="""Hello Team,<br><br>
				Credit Note raised for the customer {}.<br><br>
				Kindly login to apps.myhector.com for the approval process.<br><br><br>
				Regards,<br>
				Hector Beverages""".format(self.customer_name)
			frappe.sendmail(subject="Customer Complaints: Credit Note Raised", content=msg, cc = '{},{}'.format(rsmEmail, asmEmail), recipients = '{}'.format(requestorSalesTeam), expose_recipients="header", sender="Notification@hectorbeverages.com")
			print("\n email sent \n")


		if self.workflow_state == 'Pending for Quality Head Approval':
			doc = frappe.get_doc('Quality Issue',self.name)
			skuDetails = self.sku_details
			closeIssue = 0
			for i in range(len(skuDetails)):
				#for Quantity less than 500 pouches
				if int(skuDetails[i].quantity_in_pieces) < 500 :
					# frappe.throw('for Quantity less than 500 pouches')
					closeIssue = 1
					frappe.db.set_value('Quality Issue', self.name, 'close_issue', 1)
					# frappe.db.commit()


			if closeIssue :
				frappe.db.set_value('Quality Issue', self.name, 'workflow_state', 'Issue Closed')
				msg="""Hello Team,<br><br>
				You have received a request for quality team approval for the customer {} is closed.<br><br>
				Kindly login to apps.myhector.com for the approval process.<br><br><br>
				Regards,<br>
				Hector Beverages""".format(self.customer_name)
				frappe.sendmail(subject="Customer Complaints: Issue Closed", content=msg, recipients = '{},{},{}'.format(complaintTeamEmail, physicalVerificationTeamEmail, financeTeamEmail),sender="Notification@hectorbeverages.com")
				print("\n email sent \n")
				self.reload()

			else :
				msg="""Hello {},<br><br>
				You have received a request for quality team approval from {} for the customer {}.<br><br>
				Kindly login to apps.myhector.com for the approval process.<br><br><br>
				Regards,<br>
				Hector Beverages""".format(qualityHeadName, physicalVerificationTeamName, self.customer_name)
				frappe.sendmail(subject="Customer Complaints: Pending for Quality Head Approval", content=msg, recipients = '{}'.format(qualityHeadEmail),sender="Notification@hectorbeverages.com")
				print("\n email sent \n")


