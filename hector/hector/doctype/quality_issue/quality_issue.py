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
			try :
				int(skuDetails[i].quantity_in_pieces)
			except :
				frappe.throw("Quantity (in pieces) must be a Number")



	def on_update(self):
		rsmEmail = self.rsm_name
		asmEmail = self.asm_name
		requestorSalesTeam = self.email_address_of_requestor_from_sales_team
		complaintTeamEmail = self.owner
		complaintTeamName = frappe.get_doc('User', complaintTeamEmail).full_name
		physicalVerificationTeamEmail = self.physicalremote_verification_executive_email
		physicalVerificationTeamName = frappe.get_doc('User',physicalVerificationTeamEmail).full_name
		financeTeamEmail = [x[0] for x in frappe.db.sql("""select u.name from `tabUser` u inner join `tabHas Role` hr on hr.parent = u.name where hr.role = 'Finance Team'""", as_list=1)]
		financeTeamEmail.remove('Administrator')
		financeTeamName = [x[0] for x in frappe.db.sql("""select u.full_name from `tabUser` u inner join `tabHas Role` hr on hr.parent = u.name where hr.role = 'Finance Team'""", as_list=1)]
		financeTeamName.remove('Administrator')
		qualityHeadEmail = [x[0] for x in frappe.db.sql("""select u.name from `tabUser` u inner join `tabHas Role` hr on hr.parent = u.name where hr.role = 'Quality Head'""", as_list=1)]
		qualityHeadEmail.remove('Administrator')
		qualityHeadName = [x[0] for x in frappe.db.sql("""select u.full_name from `tabUser` u inner join `tabHas Role` hr on hr.parent = u.name where hr.role = 'Quality Head'""", as_list=1)]
		qualityHeadName.remove('Administrator')
		emailMessage = """You have been requested to review the following:<br>
			<table border="1" cellspacing="0" cellpadding="5" align="">
				<tbody>
					<tr>
						<td>Ticket No:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Customer Name:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Customer Code:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Customer Location:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Customer Phone Number:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Type of Issue:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Invoice Number:</td>
						<td>{}</td>
					</tr>
				</tbody>
			</table><br>
			Kindly login to apps.myhector.com for the approval process.<br><br><br>
			Regards,<br>
			Hector Beverages""".format(self.name, self.customer_name, self.customer_code, self.customer_location, self.customer_phone_number, self.type_of_issue, self.invoice_number)

		if self.workflow_state == 'Pending for Physical Verification Officer Approval':
			frappe.db.set_value('Quality Issue', self.name, 'pending_physical_verification_time', frappe.utils.now())
			#For sending approval email to Physical Verification Officer
			msg=emailMessage
			frappe.sendmail(subject="Quality Issue for your review: {}: {}".format(self.customer_code, self.customer_name), content=msg, recipients = '{}'.format(physicalVerificationTeamEmail),sender="Notification@hectorbeverages.com")
			print("\n email sent \n")
			#For sendng email to sales team of customer complaint registered
			message1 = """Below Quality Issue have been Registered:<br>
			<table border="1" cellspacing="0" cellpadding="5" align="">
				<tbody>
					<tr>
						<td>Ticket No:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Customer Name:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Customer Code:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Customer Location:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Customer Phone Number:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Type of Issue:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Invoice Number:</td>
						<td>{}</td>
					</tr>
				</tbody>
			</table><br>""".format(self.name, self.customer_name, self.customer_code, self.customer_location, self.customer_phone_number, self.type_of_issue, self.invoice_number)
			message2 = """<table border="1" cellspacing="0" cellpadding="5" align="">
				<tr><th>SKU Code</th><th>SKU Name</th><th>Quantity</th><th>Mgf Date</th><th>Batch Details</th></tr>
				"""
			for skuRow in self.sku_details:
				message2 += "<tr><td>"+skuRow.sku_code + "</td><td>"+skuRow.sku_name + "</td><td>" + skuRow.quantity_in_pieces + "</td><td>" + str(skuRow.mgf_date) + "</td><td>" + skuRow.batch_details + "</td><tr>"
			message2 += "</table><br>"
			message3 = """<br><br><br>
			Regards,<br>
			Hector Beverages"""
			messageFinal = message1 + message2 + message3
			frappe.sendmail(subject="Quality Issue registered: {}: {}".format(self.customer_code, self.customer_name), content=messageFinal, recipients = '{}'.format(requestorSalesTeam), cc = '{},{}'.format(rsmEmail, asmEmail),expose_recipients="header", sender="Notification@hectorbeverages.com")
			print("\n email sent \n")


		if self.workflow_state == 'Resent for Physical Verification Officer Approval':
			frappe.db.set_value('Quality Issue', self.name, 'resent_physical_verification_time', frappe.utils.now())
			msg=emailMessage
			frappe.sendmail(subject="Quality Issue for your review: {}: {}".format(self.customer_code, self.customer_name), content=msg, recipients = '{}'.format(physicalVerificationTeamEmail),sender="Notification@hectorbeverages.com")
			print("\n email sent \n")

		if self.workflow_state == 'Rejected by Physical Verification Officer':
			msg="""Below Quality Issue have been Rejected:<br>
			<table border="1" cellspacing="0" cellpadding="5" align="">
				<tbody>
					<tr>
						<td>Ticket No:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Customer Name:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Customer Code:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Customer Location:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Customer Phone Number:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Type of Issue:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Invoice Number:</td>
						<td>{}</td>
					</tr>
				</tbody>
			</table><br>
			Comment: {}<br><br>
			Kindly login to apps.myhector.com for the approval process.<br><br><br>
			Regards,<br>
			Hector Beverages""".format(self.name, self.customer_name, self.customer_code, self.customer_location, self.customer_phone_number, self.type_of_issue, self.invoice_number, self.reason_of_rejection)
			frappe.sendmail(subject="Quality Issue Rejected: {}: {}".format(self.customer_code, self.customer_name), content=msg, recipients = '{}'.format(complaintTeamEmail),sender="Notification@hectorbeverages.com")
			print("\n email sent \n")
			#For sendng email to sales team and customer of Issue rejected process
			sku = self.sku_details
			message1 = """Below Quality Issue have been Rejected:<br>
			<table border="1" cellspacing="0" cellpadding="5" align="">
				<tbody>
					<tr>
						<td>Ticket No:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Customer Name:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Customer Code:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Customer Location:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Customer Phone Number:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Type of Issue:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Invoice Number:</td>
						<td>{}</td>
					</tr>
				</tbody>
			</table><br>""".format(self.name, self.customer_name, self.customer_code, self.customer_location, self.customer_phone_number, self.type_of_issue, self.invoice_number)
			message2 = """<table border="1" cellspacing="0" cellpadding="5" align="">
			<tr><th>SKU Code</th><th>SKU Name</th><th>Quantity</th><th>Mgf Date</th><th>Batch Details</th></tr>
			"""
			for skuRow in self.sku_details:
				message2 += "<tr><td>"+skuRow.sku_code + "</td><td>"+skuRow.sku_name + "</td><td>" + skuRow.quantity_in_pieces + "</td><td>" + str(skuRow.mgf_date) + "</td><td>" + skuRow.batch_details + "</td><tr>"
			message2 += "</table><br>"
			message3 = """Comment: {}<br><br><br>
			Regards,<br>
			Hector Beverages""".format(self.reason_of_rejection)
			messageFinal = message1 + message2 + message3
			frappe.sendmail(subject="Quality Issue Rejected: {}: {}".format(self.customer_code, self.customer_name), content=messageFinal, cc = '{},{}'.format(rsmEmail, asmEmail), recipients = '{}'.format(requestorSalesTeam), expose_recipients="header", sender="Notification@hectorbeverages.com")
			print("\n email sent \n")

		if self.workflow_state == 'Requested for More Details by Physical Verification Officer':
			frappe.db.set_value('Quality Issue', self.name, 'request_details_physical_verification_time', frappe.utils.now())
			msg=emailMessage
			frappe.sendmail(subject="Quality Issue requesting for more details: {}: {}".format(self.customer_code, self.customer_name), content=msg, recipients = '{}'.format(complaintTeamEmail),sender="Notification@hectorbeverages.com")
			print("\n email sent \n")

		if self.workflow_state == 'Requested for More Details by Finance Team':
			frappe.db.set_value('Quality Issue', self.name, 'request_details_finance_team_time', frappe.utils.now())
			msg=emailMessage
			frappe.sendmail(subject="Quality Issue requesting for more details: {}: {}".format(self.customer_code, self.customer_name), content=msg, recipients = '{}'.format(complaintTeamEmail),sender="Notification@hectorbeverages.com")
			print("\n email sent \n")

		if self.workflow_state == 'Rejected by Finance Team':
			msg="""Below Quality Issue have been Rejected:<br>
			<table border="1" cellspacing="0" cellpadding="5" align="">
				<tbody>
					<tr>
						<td>Ticket No:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Customer Name:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Customer Code:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Customer Location:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Customer Phone Number:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Type of Issue:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Invoice Number:</td>
						<td>{}</td>
					</tr>
				</tbody>
			</table><br>
			Comment: {}<br><br>
			Kindly login to apps.myhector.com for the approval process.<br><br><br>
			Regards,<br>
			Hector Beverages""".format(self.name, self.customer_name, self.customer_code, self.customer_location, self.customer_phone_number, self.type_of_issue, self.invoice_number, self.reason_of_rejection)
			frappe.sendmail(subject="Quality Issue Rejected: {}: {}".format(self.customer_code, self.customer_name), content=msg, recipients = '{},{}'.format(complaintTeamEmail, physicalVerificationTeamEmail),sender="Notification@hectorbeverages.com")
			print("\n email sent \n")

			#For sendng email to sales team and customer of Issue rejected process
			message1 = """Below Quality Issue have been Rejected:<br>
			<table border="1" cellspacing="0" cellpadding="5" align="">
				<tbody>
					<tr>
						<td>Ticket No:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Customer Name:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Customer Code:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Customer Location:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Customer Phone Number:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Type of Issue:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Invoice Number:</td>
						<td>{}</td>
					</tr>
				</tbody>
			</table><br>""".format(self.name, self.customer_name, self.customer_code, self.customer_location, self.customer_phone_number, self.type_of_issue, self.invoice_number)
			message2 = """<table border="1" cellspacing="0" cellpadding="5" align="">
			<tr><th>SKU Code</th><th>SKU Name</th><th>Quantity</th><th>Mgf Date</th><th>Batch Details</th></tr>
			"""
			for skuRow in self.sku_details:
				message2 += "<tr><td>"+skuRow.sku_code + "</td><td>"+skuRow.sku_name + "</td><td>" + skuRow.quantity_in_pieces + "</td><td>" + str(skuRow.mgf_date) + "</td><td>" + skuRow.batch_details + "</td><tr>"
			message2 += "</table><br>"
			message3 = """Comment: {}<br><br><br>
			Regards,<br>
			Hector Beverages""".format(self.reason_of_rejection)
			messageFinal = message1 + message2 + message3
			frappe.sendmail(subject="Quality Issue Rejected: {}: {}".format(self.customer_code, self.customer_name), content=messageFinal, cc = '{},{}'.format(rsmEmail, asmEmail), recipients = '{}'.format(requestorSalesTeam), expose_recipients="header", sender="Notification@hectorbeverages.com")
			print("\n email sent \n")

		if self.workflow_state == 'Pending for Finance Team Approval':
			frappe.db.set_value('Quality Issue', self.name, 'pending_finance_team_time', frappe.utils.now())
			msg=emailMessage
			frappe.sendmail(subject="Quality Issue for your review: {}: {}".format(self.customer_code, self.customer_name), content=msg, recipients = financeTeamEmail,sender="Notification@hectorbeverages.com")
			print("\n email sent \n")

		if self.workflow_state == 'Resent for Finance Team Approval':
			frappe.db.set_value('Quality Issue', self.name, 'resent_finance_team_time', frappe.utils.now())
			msg=emailMessage
			frappe.sendmail(subject="Quality Issue for your review: {}: {}".format(self.customer_code, self.customer_name), content=msg, recipients = financeTeamEmail,sender="Notification@hectorbeverages.com")
			print("\n email sent \n")

		if self.workflow_state == 'RCA Approved':
			msg=emailMessage
			frappe.sendmail(subject="Quality Issue Completed: {}: {}".format(self.customer_code, self.customer_name), content=msg, recipients = [complaintTeamEmail] + [physicalVerificationTeamEmail] + financeTeamEmail,sender="Notification@hectorbeverages.com")
			print("\n email sent \n")

			message1 = """Below Quality Issue have been Closed:<br>
			<table border="1" cellspacing="0" cellpadding="5" align="">
				<tbody>
					<tr>
						<td>Ticket No:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Customer Name:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Customer Code:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Customer Location:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Customer Phone Number:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Type of Issue:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Invoice Number:</td>
						<td>{}</td>
					</tr>
				</tbody>
				</table><br>""".format(self.name, self.customer_name, self.customer_code, self.customer_location, self.customer_phone_number, self.type_of_issue, self.invoice_number)
			message2 = """<table border="1" cellspacing="0" cellpadding="5" align="">
			<tr><th>SKU Code</th><th>SKU Name</th><th>Quantity</th><th>Mgf Date</th><th>Batch Details</th></tr>
			"""
			for skuRow in self.sku_details:
				message2 += "<tr><td>"+skuRow.sku_code + "</td><td>"+skuRow.sku_name + "</td><td>" + skuRow.quantity_in_pieces + "</td><td>" + str(skuRow.mgf_date) + "</td><td>" + skuRow.batch_details + "</td><tr>"
			message2 += "</table><br>"
			message3 = """
				Credit Details: {}
				<br><br><br>
				Regards,<br>
				Hector Beverages""".format(self.credit_details)
			messageFinal = message1 + message2 + message3
			frappe.sendmail(subject="Quality Issue Completed: {}: {}".format(self.customer_code, self.customer_name), content=messageFinal, cc = '{},{}'.format(rsmEmail, asmEmail), recipients = '{}'.format(requestorSalesTeam), expose_recipients="header",sender="Notification@hectorbeverages.com")
			print("\n email sent \n")

		if self.workflow_state == 'Pending for RCA Details' :
			doc = frappe.get_doc('Quality Issue',self.name)
			skuDetails = self.sku_details
			currentDate = frappe.utils.today()
			date_format = "%Y-%m-%d"
			closeIssue = 1
			for i in range(len(skuDetails)):
				todayDate = datetime.strptime(currentDate, date_format)
				documentDate = frappe.utils.get_datetime(skuDetails[i].mgf_date).strftime(date_format)
				documentDateStr = datetime.strptime(documentDate, date_format)
				daysDiffrence = (todayDate - documentDateStr).days

				#for Quantity less than 100 pouches and for diffrence between 2 dates greater than 3 months
				if ((int(skuDetails[i].quantity_in_pieces) > 100) and (int(daysDiffrence) < 91)) :
					closeIssue = 0
					# self.close_issue = 0
					frappe.db.set_value('Quality Issue', self.name, 'close_issue', 0)

			print("the close_issue value is ",closeIssue)

			# self.save()
			# frappe.db.commit()
			if closeIssue :
				# frappe.msgprint('for Quantity less than 100 pouches')
				frappe.db.set_value('Quality Issue', self.name, 'workflow_state', 'Issue Closed')
				msg=emailMessage
				frappe.sendmail(subject="Quality Issue Completed: {}: {}".format(self.customer_code, self.customer_name), content=msg, recipients = [complaintTeamEmail] + [physicalVerificationTeamEmail] + financeTeamEmail,sender="Notification@hectorbeverages.com")
				print("\n email sent \n")
				self.reload()
				# frappe.db.commit()

				#For sendng email to sales team of credit note raised process
				message1 = """Below Quality Issue have been Closed:<br>
			<table border="1" cellspacing="0" cellpadding="5" align="">
				<tbody>
					<tr>
						<td>Ticket No:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Customer Name:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Customer Code:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Customer Location:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Customer Phone Number:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Type of Issue:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Invoice Number:</td>
						<td>{}</td>
					</tr>
				</tbody>
				</table><br>""".format(self.name, self.customer_name, self.customer_code, self.customer_location, self.customer_phone_number, self.type_of_issue, self.invoice_number)
				message2 = """<table border="1" cellspacing="0" cellpadding="5" align="">
				<tr><th>SKU Code</th><th>SKU Name</th><th>Quantity</th><th>Mgf Date</th><th>Batch Details</th></tr>
				"""
				for skuRow in self.sku_details:
					message2 += "<tr><td>"+skuRow.sku_code + "</td><td>"+skuRow.sku_name + "</td><td>" + skuRow.quantity_in_pieces + "</td><td>" + str(skuRow.mgf_date) + "</td><td>" + skuRow.batch_details + "</td><tr>"
				message2 += "</table><br>"
				message3 = """
				Credit Details: {}
				<br><br><br>
				Regards,<br>
				Hector Beverages""".format(self.credit_details)
				messageFinal = message1 + message2 + message3
				frappe.sendmail(subject="Quality Issue Completed: {}: {}".format(self.customer_code, self.customer_name), content=messageFinal, cc = '{},{}'.format(rsmEmail, asmEmail), recipients = '{}'.format(requestorSalesTeam), expose_recipients="header", sender="Notification@hectorbeverages.com")
				print("\n email sent \n")

			else :
				frappe.db.set_value('Quality Issue', self.name, 'pending_rca_details_time', frappe.utils.now())
				msg=emailMessage
				frappe.sendmail(subject="Quality Issue Pending for RCA: {}: {}".format(self.customer_code, self.customer_name), content=msg, recipients = '{}'.format(physicalVerificationTeamEmail),sender="Notification@hectorbeverages.com")
				print("\n email sent \n")


		if self.workflow_state == 'Pending for Quality Head Approval':
			doc = frappe.get_doc('Quality Issue',self.name)
			skuDetails = self.sku_details
			currentDate = frappe.utils.today()
			date_format = "%Y-%m-%d"

			skuDetails = self.sku_details
			closeIssue = 1
			for i in range(len(skuDetails)):
				todayDate = datetime.strptime(currentDate, date_format)
				documentDate = frappe.utils.get_datetime(skuDetails[i].mgf_date).strftime(date_format)
				documentDateStr = datetime.strptime(documentDate, date_format)
				daysDiffrence = (todayDate - documentDateStr).days

				#for Quantity less than 500 pouches
				if (int(skuDetails[i].quantity_in_pieces) >= 500 and (int(daysDiffrence) < 91)):
					# frappe.throw('for Quantity less than 500 pouches')
					closeIssue = 0
					frappe.db.set_value('Quality Issue', self.name, 'close_issue', 0)
					# frappe.db.commit()


			if closeIssue :
				frappe.db.set_value('Quality Issue', self.name, 'workflow_state', 'Issue Closed')
				msg=emailMessage
				frappe.sendmail(subject="Quality Issue Completed: {}: {}".format(self.customer_code, self.customer_name), content=msg, recipients = [complaintTeamEmail] + [physicalVerificationTeamEmail] + financeTeamEmail,sender="Notification@hectorbeverages.com")
				print("\n email sent \n")
				self.reload()

				#For sendng email to sales team of credit note raised process
				message1 = """Below Quality Issue have been Closed:<br>
			<table border="1" cellspacing="0" cellpadding="5" align="">
				<tbody>
					<tr>
						<td>Ticket No:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Customer Name:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Customer Code:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Customer Location:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Customer Phone Number:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Type of Issue:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Invoice Number:</td>
						<td>{}</td>
					</tr>
				</tbody>
				</table><br>""".format(self.name, self.customer_name, self.customer_code, self.customer_location, self.customer_phone_number, self.type_of_issue, self.invoice_number)
				message2 = """<table border="1" cellspacing="0" cellpadding="5" align="">
				<tr><th>SKU Code</th><th>SKU Name</th><th>Quantity</th><th>Mgf Date</th><th>Batch Details</th></tr>
				"""
				for skuRow in self.sku_details:
					message2 += "<tr><td>"+skuRow.sku_code + "</td><td>"+skuRow.sku_name + "</td><td>" + skuRow.quantity_in_pieces + "</td><td>" + str(skuRow.mgf_date) + "</td><td>" + skuRow.batch_details + "</td><tr>"
				message2 += "</table><br>"
				message3 = """
				Credit Details: {}
				<br><br><br>
				Regards,<br>
				Hector Beverages""".format(self.credit_details)
				messageFinal = message1 + message2 + message3
				frappe.sendmail(subject="Quality Issue Completed: {}: {}".format(self.customer_code, self.customer_name), content=messageFinal, cc = '{},{}'.format(rsmEmail, asmEmail), recipients = '{}'.format(requestorSalesTeam), expose_recipients="header", sender="Notification@hectorbeverages.com")
				print("\n email sent \n")

			else :
				frappe.db.set_value('Quality Issue', self.name, 'pending_quality_head_time', frappe.utils.now())
				msg=emailMessage
				frappe.sendmail(subject="Quality Issue Pending for RCA Approval: {}: {}".format(self.customer_code, self.customer_name), content=msg, recipients = qualityHeadEmail,sender="Notification@hectorbeverages.com")
				print("\n email sent \n")


		if self.workflow_state == 'Resent for Quality Head Approval':
			frappe.db.set_value('Quality Issue', self.name, 'resent_quality_head_time', frappe.utils.now())
			msg=emailMessage
			frappe.sendmail(subject="Quality Issue Pending for RCA Approval: {}: {}".format(self.customer_code, self.customer_name), content=msg, recipients = qualityHeadEmail, sender="Notification@hectorbeverages.com")
			print("\n email sent \n")

		if self.workflow_state == 'Rejected by Quality Head':
			msg="""Below Quality Issue have been Rejected:<br>
			<table border="1" cellspacing="0" cellpadding="5" align="">
				<tbody>
					<tr>
						<td>Ticket No:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Customer Name:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Customer Code:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Customer Location:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Customer Phone Number:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Type of Issue:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Invoice Number:</td>
						<td>{}</td>
					</tr>
				</tbody>
			</table><br>
			Comment: {}<br><br>
			Kindly login to apps.myhector.com for the approval process.<br><br><br>
			Regards,<br>
			Hector Beverages""".format(self.name, self.customer_name, self.customer_code, self.customer_location, self.customer_phone_number, self.type_of_issue, self.invoice_number, self.reason_of_rejection)
			frappe.sendmail(subject="Quality Issue Rejected: {}: {}".format(self.customer_code, self.customer_name), content=msg, recipients = [complaintTeamEmail] + [physicalVerificationTeamEmail] + [financeTeamEmail],sender="Notification@hectorbeverages.com")
			print("\n email sent \n")

			#For sendng email to sales team and customer of Issue rejected process
			message1 = """Below Quality Issue have been Rejected:<br>
			<table border="1" cellspacing="0" cellpadding="5" align="">
				<tbody>
					<tr>
						<td>Ticket No:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Customer Name:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Customer Code:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Customer Location:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Customer Phone Number:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Type of Issue:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Invoice Number:</td>
						<td>{}</td>
					</tr>
				</tbody>
			</table><br>""".format(self.name, self.customer_name, self.customer_code, self.customer_location, self.customer_phone_number, self.type_of_issue, self.invoice_number)
			message2 = """<table border="1" cellspacing="0" cellpadding="5" align="">
			<tr><th>SKU Code</th><th>SKU Name</th><th>Quantity</th><th>Mgf Date</th><th>Batch Details</th></tr>
			"""
			for skuRow in self.sku_details:
				message2 += "<tr><td>"+skuRow.sku_code + "</td><td>"+skuRow.sku_name + "</td><td>" + skuRow.quantity_in_pieces + "</td><td>" + str(skuRow.mgf_date) + "</td><td>" + skuRow.batch_details + "</td><tr>"
			message2 += "</table><br>"
			message3 = """Comment: {}<br><br><br>
			Regards,<br>
			Hector Beverages""".format(self.reason_of_rejection)
			messageFinal = message1 + message2 + message3
			frappe.sendmail(subject="Quality Issue Rejected: {}: {}".format(self.customer_code, self.customer_name), content=messageFinal, cc = '{},{}'.format(rsmEmail, asmEmail), recipients = '{}'.format(requestorSalesTeam), expose_recipients="header", sender="Notification@hectorbeverages.com")
			print("\n email sent \n")

		if self.workflow_state == 'Requested for More Details by Quality Head':
			frappe.db.set_value('Quality Issue', self.name, 'request_details_quality_head_time', frappe.utils.now())
			msg=emailMessage
			frappe.sendmail(subject="Quality Issue requesting for more details: {}: {}".format(self.customer_code, self.customer_name), content=msg, recipients = '{}'.format(physicalVerificationTeamEmail),sender="Notification@hectorbeverages.com")
			print("\n email sent \n")
