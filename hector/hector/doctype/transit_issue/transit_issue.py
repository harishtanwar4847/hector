# Copyright (c) 2021, Atrina Technologies Pvt Ltd and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class TransitIssue(Document):
	def on_update(self):
		rsmEmail = self.rsm_name
		asmEmail = self.asm_name
		requestorSalesTeam = self.email_address_of_requestor_from_sales_team
		complaintTeamEmail = self.owner
		complaintTeamName = frappe.get_doc('User', complaintTeamEmail).full_name
		supplyTeamEmail = [x[0] for x in frappe.db.sql("""select u.name from `tabUser` u inner join `tabHas Role` hr on hr.parent = u.name where hr.role = 'Supply Team'""", as_list=1)]
		supplyTeamEmail.remove('Administrator')
		financeTeamEmail = [x for x in frappe.db.sql("""select u.name from `tabUser` u inner join `tabHas Role` hr on hr.parent = u.name where hr.role = 'Finance Team'""", as_list=1)]
		financeTeamEmail.remove(['Administrator'])
		financeTeamEmail = financeTeamEmail[0][0]
		financeTeamName = [x for x in frappe.db.sql("""select u.full_name from `tabUser` u inner join `tabHas Role` hr on hr.parent = u.name where hr.role = 'Finance Team'""", as_list=1)]
		financeTeamName.remove(['Administrator'])
		financeTeamName = financeTeamName[0][0]
		emailMessage = """You have been requested to review the following:<br>
			<table border="1" cellspacing="0" cellpadding="5" align="">
				<tbody>
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
				</tbody>
			</table><br>
			Kindly login to apps.myhector.com for the approval process.<br><br><br>
			Regards,<br>
			Hector Beverages""".format(self.customer_name, self.customer_code, self.customer_location, self.customer_phone_number, self.type_of_issue)


		if self.workflow_state == 'Pending for Supply Team Approval' :
			#For sendng email to sales team of customer complaint registered
			msg=emailMessage
			frappe.sendmail(subject="Transit Issue registered: {}: {}".format(self.customer_code, self.customer_name), content=msg,recipients = '{}'.format(requestorSalesTeam), cc = '{},{}'.format(rsmEmail, asmEmail),expose_recipients="header", sender="Notification@hectorbeverages.com")
			print("\n email sent \n")
			#For sending approval email to Supply Team
			msg=emailMessage
			frappe.sendmail(subject="Transit Issue Pending for Supply Team Approval: {}: {}".format(self.customer_code, self.customer_name), content=msg, recipients = supplyTeamEmail,sender="Notification@hectorbeverages.com")
			print("\n email sent \n")

		if self.workflow_state == 'Resent for Supply Team Approval' :
			msg=emailMessage
			frappe.sendmail(subject="Transit Issue Resent for Supply Team Approval: {}: {}".format(self.customer_code, self.customer_name), content=msg, recipients = supplyTeamEmail,sender="Notification@hectorbeverages.com")
			print("\n email sent \n")

		if self.workflow_state == 'Rejected by Supply Team' :
			msg="""Below Transit Issue have been Rejected:<br>
			<table border="1" cellspacing="0" cellpadding="5" align="">
				<tbody>
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
				</tbody>
			</table><br>
			Comment: {}<br><br>
			Kindly login to apps.myhector.com for the approval process.<br><br><br>
			Regards,<br>
			Hector Beverages""".format(self.customer_name, self.customer_code, self.customer_location, self.customer_phone_number, self.type_of_issue, self.reason_of_rejection)
			frappe.sendmail(subject="Transit Issue Rejected: {}: {}".format(self.customer_code, self.customer_name), content=msg, recipients = '{}'.format(complaintTeamEmail),sender="Notification@hectorbeverages.com")
			print("\n email sent \n")
			#For sendng email to sales team and customer of Issue rejected process
			msg="""Below Transit Issue have been Rejected:<br>
			<table border="1" cellspacing="0" cellpadding="5" align="">
				<tbody>
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
				</tbody>
			</table><br>
			Comment: {}<br><br>
			Kindly login to apps.myhector.com for the approval process.<br><br><br>
			Regards,<br>
			Hector Beverages""".format(self.customer_name, self.customer_code, self.customer_location, self.customer_phone_number, self.type_of_issue, self.reason_of_rejection)
			frappe.sendmail(subject="Transit Issue Rejected: {}: {}".format(self.customer_code, self.customer_name), content=msg, cc = '{},{}'.format(rsmEmail, asmEmail), recipients = '{}'.format(requestorSalesTeam), expose_recipients="header", sender="Notification@hectorbeverages.com")
			print("\n email sent \n")


		if self.workflow_state == 'Requested for More Details by Supply Team':
			msg=emailMessage
			frappe.sendmail(subject="Transit Issue requesting for more details: {}: {}".format(self.customer_code, self.customer_name), content=msg, recipients = '{}'.format(complaintTeamEmail),sender="Notification@hectorbeverages.com")
			print("\n email sent \n")

		if self.workflow_state == 'Requested for More Details by Finance Team':
			msg=emailMessage
			frappe.sendmail(subject="Transit Issue requesting for more details: {}: {}".format(self.customer_code, self.customer_name), content=msg, recipients = supplyTeamEmail,sender="Notification@hectorbeverages.com")
			print("\n email sent \n")

		if self.workflow_state == 'Rejected by Finance Team':
			msg="""Below Transit Issue have been Rejected:<br>
			<table border="1" cellspacing="0" cellpadding="5" align="">
				<tbody>
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
				</tbody>
			</table><br>
			Comment: {}<br><br>
			Kindly login to apps.myhector.com for the approval process.<br><br><br>
			Regards,<br>
			Hector Beverages""".format(self.customer_name, self.customer_code, self.customer_location, self.customer_phone_number, self.type_of_issue, self.reason_of_rejection)
			frappe.sendmail(subject="Transit Issue Rejected: {}: {}".format(self.customer_code, self.customer_name), content=msg, recipients = [complaintTeamEmail] + supplyTeamEmail, sender="Notification@hectorbeverages.com")
			print("\n email sent \n")
			#For sendng email to sales team and customer of Issue rejected process
			msg="""Below Transit Issue have been Rejected:<br>
			<table border="1" cellspacing="0" cellpadding="5" align="">
				<tbody>
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
				</tbody>
			</table><br>
			Comment: {}<br><br>
			Kindly login to apps.myhector.com for the approval process.<br><br><br>
			Regards,<br>
			Hector Beverages""".format(self.customer_name, self.customer_code, self.customer_location, self.customer_phone_number, self.type_of_issue, self.reason_of_rejection)
			frappe.sendmail(subject="Transit Issue Rejected: {}: {}".format(self.customer_code, self.customer_name), content=msg, cc = '{},{}'.format(rsmEmail, asmEmail), recipients = '{}'.format(requestorSalesTeam), expose_recipients="header", sender="Notification@hectorbeverages.com")
			print("\n email sent \n")


		if self.workflow_state == 'Pending for Finance Team Approval':
			msg=emailMessage
			frappe.sendmail(subject="Transit Issue Pending for Finance Team Approval: {}: {}".format(self.customer_code, self.customer_name), content=msg, recipients = '{}'.format(financeTeamEmail),sender="Notification@hectorbeverages.com")
			print("\n email sent \n")

		if self.workflow_state == 'Resent for Finance Team Approval':
			msg=emailMessage
			frappe.sendmail(subject="Transit Issue Resent for Finance Team Approval: {}: {}".format(self.customer_code, self.customer_name), content=msg, recipients = '{}'.format(financeTeamEmail),sender="Notification@hectorbeverages.com")
			print("\n email sent \n")

		if self.workflow_state == 'Issue Closed':
			msg=emailMessage
			frappe.sendmail(subject="Transit Issue Completed: {}: {}".format(self.customer_code, self.customer_name), content=msg, recipients = [complaintTeamEmail] + supplyTeamEmail, sender="Notification@hectorbeverages.com")
			print("\n email sent \n")

			#For sendng email to sales team of credit note raised process
			msg=emailMessage
			frappe.sendmail(subject="Transit Issue Completed: {}: {}".format(self.customer_code, self.customer_name), content=msg, cc = '{},{}'.format(rsmEmail, asmEmail), recipients = '{}'.format(requestorSalesTeam), expose_recipients="header", sender="Notification@hectorbeverages.com")
			print("\n email sent \n")

