import frappe
from datetime import datetime

def daysDiffrence(documentDate):
    from datetime import datetime
    try:
        # todayDateStr = datetime.strptime(frappe.utils.today(), "%Y-%m-%d")
        todayDateStr = datetime.strptime(frappe.utils.now(), "%Y-%m-%d %H:%M:%S.%f")
        # documentDateStr = datetime.strftime(documentDate, '%Y-%m-%d %H:%M:%S.%f')
        # documentDateStr = datetime.strptime(documentDate, '%Y-%m-%d')
        documentDateStr = datetime.strptime(documentDate, '%Y-%m-%d %H:%M:%S.%f')
        return int((todayDateStr - documentDateStr).days)
    except :
        return 0


def quality_issue_daily():
    qualityIssueList = frappe.db.get_list('Quality Issue', as_list = True)
    for qualityIssue in qualityIssueList :
        issue = frappe.get_doc('Quality Issue',qualityIssue[0])
        complaintTeamEmail = issue.owner
        complaintTeamName = frappe.get_doc('User', complaintTeamEmail).full_name
        physicalVerificationTeamEmail = issue.physicalremote_verification_executive_email
        physicalVerificationTeamName = frappe.get_doc('User',physicalVerificationTeamEmail).full_name
        financeTeamEmail = [x[0] for x in frappe.db.sql("""select u.name from `tabUser` u inner join `tabHas Role` hr on hr.parent = u.name where hr.role = 'Finance Team'""", as_list=1)]
        financeTeamEmail.remove('Administrator')
        qualityHeadEmail = [x[0] for x in frappe.db.sql("""select u.name from `tabUser` u inner join `tabHas Role` hr on hr.parent = u.name where hr.role = 'Quality Head'""", as_list=1)]
        qualityHeadEmail.remove('Administrator')
        emailMessage = """This is to inform you that there has been a ticket pending with you for 3 days. Kindly resolve the issue as soon as possible. Below is the Details of the Ticket<br>
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
                    <tr>
						<td>ASM:</td>
						<td>{}</td>
					</tr>
                    <tr>
						<td>RSM:</td>
						<td>{}</td>
					</tr>
				</tbody>
			</table><br>""".format(issue.name, issue.customer_name, issue.customer_code, issue.customer_location, issue.customer_phone_number, issue.type_of_issue, issue.invoice_number, issue.asm_full_name, issue.rsm_full_name)


        if (issue.workflow_state == 'Pending for Physical Verification Officer Approval' and daysDiffrence(issue.pending_physical_verification_time) >= 3):
            salutation = "Hello " + physicalVerificationTeamName + ",<br><br>"
            message2 = """<table border="1" cellspacing="0" cellpadding="5" align="">
                <tr><th>SKU Code</th><th>SKU Name</th><th>Quantity</th><th>Mgf Date</th><th>Batch Details</th></tr>
                """
            for skuRow in issue.sku_details:
                message2 += "<tr><td>"+skuRow.sku_code + "</td><td>"+skuRow.sku_name + "</td><td>" + skuRow.quantity_in_pieces + "</td><td>" + str(skuRow.mgf_date) + "</td><td>" + skuRow.batch_details + "</td><tr>"
            message2 += "</table><br>"
            message3 = """<br><br><br>
            Regards,<br>
            Hector Beverages"""
            msg= salutation + emailMessage + message2 + message3
            frappe.sendmail(subject="Quality Complaint: Ticket Pending since 3 Days", content=msg, recipients = '{}'.format(physicalVerificationTeamEmail),sender="Notification@hectorbeverages.com")
            print("\n email sent \n")

        if (issue.workflow_state == 'Resent for Physical Verification Officer Approval' and daysDiffrence(issue.resent_physical_verification_time) >= 3):
            salutation = "Hello " + physicalVerificationTeamName + ",<br><br>"
            message2 = """<table border="1" cellspacing="0" cellpadding="5" align="">
				<tr><th>SKU Code</th><th>SKU Name</th><th>Quantity</th><th>Mgf Date</th><th>Batch Details</th></tr>
				"""
            for skuRow in issue.sku_details:
                message2 += "<tr><td>"+skuRow.sku_code + "</td><td>"+skuRow.sku_name + "</td><td>" + skuRow.quantity_in_pieces + "</td><td>" + str(skuRow.mgf_date) + "</td><td>" + skuRow.batch_details + "</td><tr>"
            message2 += "</table><br>"
            message3 = """<br><br><br>
            Regards,<br>
            Hector Beverages"""
            msg= salutation + emailMessage + message2 + message3
            frappe.sendmail(subject="Quality Complaint: Ticket Pending since 3 Days", content=msg, recipients = '{}'.format(physicalVerificationTeamEmail),sender="Notification@hectorbeverages.com")
            print("\n email sent \n")

        if (issue.workflow_state == 'Pending for Finance Team Approval' and daysDiffrence(issue.pending_finance_team_time) >= 3):
            for i in range(len(financeTeamEmail)):
                salutation = "Hello " + frappe.get_doc('User', financeTeamEmail[i]).full_name + ",<br><br>"
                message2 = """<table border="1" cellspacing="0" cellpadding="5" align="">
				<tr><th>SKU Code</th><th>SKU Name</th><th>Quantity</th><th>Mgf Date</th><th>Batch Details</th></tr>
				"""
                for skuRow in issue.sku_details:
                    message2 += "<tr><td>"+skuRow.sku_code + "</td><td>"+skuRow.sku_name + "</td><td>" + skuRow.quantity_in_pieces + "</td><td>" + str(skuRow.mgf_date) + "</td><td>" + skuRow.batch_details + "</td><tr>"
                message2 += "</table><br>"
                message3 = """<br><br><br>
                Regards,<br>
                Hector Beverages"""
                msg= salutation + emailMessage + message2 + message3
                frappe.sendmail(subject="Quality Complaint: Ticket Pending since 3 Days", content=msg, recipients = '{}'.format(financeTeamEmail[i]),sender="Notification@hectorbeverages.com")
                print("\n email sent \n")

        if (issue.workflow_state == 'Resent for Finance Team Approval' and daysDiffrence(issue.resent_finance_team_time) >= 3):
            for i in range(len(financeTeamEmail)):
                salutation = "Hello " + frappe.get_doc('User', financeTeamEmail[i]).full_name + ",<br><br>"
                message2 = """<table border="1" cellspacing="0" cellpadding="5" align="">
				<tr><th>SKU Code</th><th>SKU Name</th><th>Quantity</th><th>Mgf Date</th><th>Batch Details</th></tr>
				"""
                for skuRow in issue.sku_details:
                    message2 += "<tr><td>"+skuRow.sku_code + "</td><td>"+skuRow.sku_name + "</td><td>" + skuRow.quantity_in_pieces + "</td><td>" + str(skuRow.mgf_date) + "</td><td>" + skuRow.batch_details + "</td><tr>"
                message2 += "</table><br>"
                message3 = """<br><br><br>
                Regards,<br>
                Hector Beverages"""
                msg= salutation + emailMessage + message2 + message3
                frappe.sendmail(subject="Quality Complaint: Ticket Pending since 3 Days", content=msg, recipients = '{}'.format(financeTeamEmail[i]),sender="Notification@hectorbeverages.com")
                print("\n email sent \n")

        if (issue.workflow_state == 'Pending for Quality Head Approval' and daysDiffrence(issue.pending_quality_head_time) >= 3):
            for i in range(len(qualityHeadEmail)):
                salutation = "Hello " + frappe.get_doc('User', qualityHeadEmail[i]).full_name + ",<br><br>"
                message2 = """<table border="1" cellspacing="0" cellpadding="5" align="">
				<tr><th>SKU Code</th><th>SKU Name</th><th>Quantity</th><th>Mgf Date</th><th>Batch Details</th></tr>
				"""
                for skuRow in issue.sku_details:
                    message2 += "<tr><td>"+skuRow.sku_code + "</td><td>"+skuRow.sku_name + "</td><td>" + skuRow.quantity_in_pieces + "</td><td>" + str(skuRow.mgf_date) + "</td><td>" + skuRow.batch_details + "</td><tr>"
                message2 += "</table><br>"
                message3 = """<br><br><br>
                Regards,<br>
                Hector Beverages"""
                msg= salutation + emailMessage + message2 + message3
                frappe.sendmail(subject="Quality Complaint: Ticket Pending since 3 Days", content=msg, recipients = '{}'.format(qualityHeadEmail[i]),sender="Notification@hectorbeverages.com")
                print("\n email sent \n")

        if (issue.workflow_state == 'Resent for Quality Head Approval' and daysDiffrence(issue.resent_quality_head_time) >= 3):
            for i in range(len(qualityHeadEmail)):
                salutation = "Hello " + frappe.get_doc('User', qualityHeadEmail[i]).full_name + ",<br><br>"
                message2 = """<table border="1" cellspacing="0" cellpadding="5" align="">
				<tr><th>SKU Code</th><th>SKU Name</th><th>Quantity</th><th>Mgf Date</th><th>Batch Details</th></tr>
				"""
                for skuRow in issue.sku_details:
                    message2 += "<tr><td>"+skuRow.sku_code + "</td><td>"+skuRow.sku_name + "</td><td>" + skuRow.quantity_in_pieces + "</td><td>" + str(skuRow.mgf_date) + "</td><td>" + skuRow.batch_details + "</td><tr>"
                message2 += "</table><br>"
                message3 = """<br><br><br>
                Regards,<br>
                Hector Beverages"""
                msg= salutation + emailMessage + message2 + message3
                frappe.sendmail(subject="Quality Complaint: Ticket Pending since 3 Days", content=msg, recipients = '{}'.format(qualityHeadEmail[i]),sender="Notification@hectorbeverages.com")
                print("\n email sent \n")

        if (issue.workflow_state == 'Requested for More Details by Physical Verification Officer' and daysDiffrence(issue.request_details_physical_verification_time) >= 3):
            salutation = "Hello " + complaintTeamName + ",<br><br>"
            message2 = """<table border="1" cellspacing="0" cellpadding="5" align="">
				<tr><th>SKU Code</th><th>SKU Name</th><th>Quantity</th><th>Mgf Date</th><th>Batch Details</th></tr>
				"""
            for skuRow in issue.sku_details:
                message2 += "<tr><td>"+skuRow.sku_code + "</td><td>"+skuRow.sku_name + "</td><td>" + skuRow.quantity_in_pieces + "</td><td>" + str(skuRow.mgf_date) + "</td><td>" + skuRow.batch_details + "</td><tr>"
            message2 += "</table><br>"
            message3 = """<br><br><br>
            Regards,<br>
            Hector Beverages"""
            msg= salutation + emailMessage + message2 + message3
            frappe.sendmail(subject="Quality Complaint: Ticket Pending since 3 Days", content=msg, recipients = '{}'.format(complaintTeamEmail),sender="Notification@hectorbeverages.com")
            print("\n email sent \n")

        if (issue.workflow_state == 'Requested for More Details by Finance Team' and daysDiffrence(issue.request_details_finance_team_time) >= 3):
            salutation = "Hello " + physicalVerificationTeamName + ",<br><br>"
            message2 = """<table border="1" cellspacing="0" cellpadding="5" align="">
				<tr><th>SKU Code</th><th>SKU Name</th><th>Quantity</th><th>Mgf Date</th><th>Batch Details</th></tr>
				"""
            for skuRow in issue.sku_details:
                message2 += "<tr><td>"+skuRow.sku_code + "</td><td>"+skuRow.sku_name + "</td><td>" + skuRow.quantity_in_pieces + "</td><td>" + str(skuRow.mgf_date) + "</td><td>" + skuRow.batch_details + "</td><tr>"
            message2 += "</table><br>"
            message3 = """<br><br><br>
            Regards,<br>
            Hector Beverages"""
            msg= salutation + emailMessage + message2 + message3
            frappe.sendmail(subject="Quality Complaint: Ticket Pending since 3 Days", content=msg, recipients = '{}'.format(physicalVerificationTeamEmail),sender="Notification@hectorbeverages.com")
            print("\n email sent \n")

        if (issue.workflow_state == 'Requested for More Details by Quality Head' and daysDiffrence(issue.request_details_quality_head_time) >= 3):
            salutation = "Hello " + physicalVerificationTeamName + ",<br><br>"
            message2 = """<table border="1" cellspacing="0" cellpadding="5" align="">
				<tr><th>SKU Code</th><th>SKU Name</th><th>Quantity</th><th>Mgf Date</th><th>Batch Details</th></tr>
				"""
            for skuRow in issue.sku_details:
                message2 += "<tr><td>"+skuRow.sku_code + "</td><td>"+skuRow.sku_name + "</td><td>" + skuRow.quantity_in_pieces + "</td><td>" + str(skuRow.mgf_date) + "</td><td>" + skuRow.batch_details + "</td><tr>"
            message2 += "</table><br>"
            message3 = """<br><br><br>
            Regards,<br>
            Hector Beverages"""
            msg= salutation + emailMessage + message2 + message3
            frappe.sendmail(subject="Quality Complaint: Ticket Pending since 3 Days", content=msg, recipients = '{}'.format(physicalVerificationTeamEmail),sender="Notification@hectorbeverages.com")
            print("\n email sent \n")

        if (issue.workflow_state == 'Pending for RCA Details' and daysDiffrence(issue.pending_rca_details_time) >= 3):
            salutation = "Hello " + physicalVerificationTeamName + ",<br><br>"
            message2 = """<table border="1" cellspacing="0" cellpadding="5" align="">
				<tr><th>SKU Code</th><th>SKU Name</th><th>Quantity</th><th>Mgf Date</th><th>Batch Details</th></tr>
				"""
            for skuRow in issue.sku_details:
                message2 += "<tr><td>"+skuRow.sku_code + "</td><td>"+skuRow.sku_name + "</td><td>" + skuRow.quantity_in_pieces + "</td><td>" + str(skuRow.mgf_date) + "</td><td>" + skuRow.batch_details + "</td><tr>"
            message2 += "</table><br>"
            message3 = """<br><br><br>
            Regards,<br>
            Hector Beverages"""
            msg= salutation + emailMessage + message2 + message3
            frappe.sendmail(subject="Quality Complaint: Ticket Pending since 3 Days", content=msg, recipients = '{}'.format(physicalVerificationTeamEmail),sender="Notification@hectorbeverages.com")
            print("\n email sent \n")


def transit_issue_daily():
    transitIssueList = frappe.db.get_list('Transit Issue', as_list = True)
    for transitIssue in transitIssueList :
        issue = frappe.get_doc('Transit Issue',transitIssue[0])
        complaintTeamEmail = issue.owner
        complaintTeamName = frappe.get_doc('User', complaintTeamEmail).full_name
        supplyTeamEmail = [x[0] for x in frappe.db.sql("""select u.name from `tabUser` u inner join `tabHas Role` hr on hr.parent = u.name where hr.role = 'Supply Team'""", as_list=1)]
        supplyTeamEmail.remove('Administrator')
        financeTeamEmail = [x[0] for x in frappe.db.sql("""select u.name from `tabUser` u inner join `tabHas Role` hr on hr.parent = u.name where hr.role = 'Finance Team'""", as_list=1)]
        financeTeamEmail.remove('Administrator')
        emailMessage = """This is to inform you that there has been a ticket pending with you for 3 days. Kindly resolve the issue as soon as possible. Below is the Details of the Ticket<br>
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
						<td>ASM:</td>
						<td>{}</td>
					</tr>
                    <tr>
						<td>RSM:</td>
						<td>{}</td>
					</tr>
				</tbody>
			</table><br>
			Kindly login to apps.myhector.com for the approval process.<br><br><br>
			Regards,<br>
			Hector Beverages""".format(issue.name, issue.customer_name, issue.customer_code, issue.customer_location, issue.customer_phone_number, issue.type_of_issue, issue.asm_full_name, issue.rsm_full_name)

        if (issue.workflow_state == 'Pending for Supply Team Approval' and daysDiffrence(issue.pending_supply_team_time) >= 3):
            for i in range(len(supplyTeamEmail)):
                salutation = "Hello " + frappe.get_doc('User', supplyTeamEmail[i]).full_name + ",<br><br>"
                message2 = """<table border="1" cellspacing="0" cellpadding="5" align="">
			<tr><th>SKU Code</th><th>SKU Name</th><th>Damaged /Missing Quantity</th><th>Invoice Number</th><th>Batch Details</th></tr>
			"""
                for skuRow in issue.sku_details:
                    message2 += "<tr><td>"+skuRow.sku_code + "</td><td>"+skuRow.sku_name + "</td><td>" + skuRow.damaged_missing_quantity + "</td><td>" + skuRow.invoice_number + "</td><td>" + skuRow.batch_details + "</td><tr>"
                message2 += "</table><br>"
                message3 = """<br><br><br>
                Regards,<br>
                Hector Beverages"""
                msg= salutation + emailMessage + message2 + message3
                frappe.sendmail(subject="Transit Complaint: Ticket Pending since 3 Days", content=msg, recipients = '{}'.format(supplyTeamEmail[i]) ,sender="Notification@hectorbeverages.com")
                print("\n email sent \n")


        if (issue.workflow_state == 'Resent for Supply Team Approval' and daysDiffrence(issue.resent_supply_team_time) >= 3):
            for i in range(len(supplyTeamEmail)):
                salutation = "Hello " + frappe.get_doc('User', supplyTeamEmail[i]).full_name + ",<br><br>"
                message2 = """<table border="1" cellspacing="0" cellpadding="5" align="">
			<tr><th>SKU Code</th><th>SKU Name</th><th>Damaged /Missing Quantity</th><th>Invoice Number</th><th>Batch Details</th></tr>
			"""
                for skuRow in issue.sku_details:
                    message2 += "<tr><td>"+skuRow.sku_code + "</td><td>"+skuRow.sku_name + "</td><td>" + skuRow.damaged_missing_quantity + "</td><td>" + skuRow.invoice_number + "</td><td>" + skuRow.batch_details + "</td><tr>"
                message2 += "</table><br>"
                message3 = """<br><br><br>
                Regards,<br>
                Hector Beverages"""
                msg= salutation + emailMessage + message2 + message3
                frappe.sendmail(subject="Transit Complaint: Ticket Pending since 3 Days", content=msg, recipients = '{}'.format(supplyTeamEmail[i]) ,sender="Notification@hectorbeverages.com")
                print("\n email sent \n")

        if (issue.workflow_state == 'Pending for Finance Team Approval' and daysDiffrence(issue.pending_finance_team_time) >= 3):
            for i in range(len(financeTeamEmail)):
                salutation = "Hello " + frappe.get_doc('User', financeTeamEmail[i]).full_name + ",<br><br>"
                message2 = """<table border="1" cellspacing="0" cellpadding="5" align="">
			<tr><th>SKU Code</th><th>SKU Name</th><th>Damaged /Missing Quantity</th><th>Invoice Number</th><th>Batch Details</th></tr>
			"""
                for skuRow in issue.sku_details:
                    message2 += "<tr><td>"+skuRow.sku_code + "</td><td>"+skuRow.sku_name + "</td><td>" + skuRow.damaged_missing_quantity + "</td><td>" + skuRow.invoice_number + "</td><td>" + skuRow.batch_details + "</td><tr>"
                message2 += "</table><br>"
                message3 = """<br><br><br>
                Regards,<br>
                Hector Beverages"""
                msg= salutation + emailMessage + message2 + message3
                frappe.sendmail(subject="Transit Complaint: Ticket Pending since 3 Days", content=msg, recipients = '{}'.format(financeTeamEmail[i]) ,sender="Notification@hectorbeverages.com")
                print("\n email sent \n")


        if (issue.workflow_state == 'Resent for Finance Team Approval' and daysDiffrence(issue.resent_finance_team_time) >= 3):
            for i in range(len(financeTeamEmail)):
                salutation = "Hello " + frappe.get_doc('User', financeTeamEmail[i]).full_name + ",<br><br>"
                message2 = """<table border="1" cellspacing="0" cellpadding="5" align="">
			<tr><th>SKU Code</th><th>SKU Name</th><th>Damaged /Missing Quantity</th><th>Invoice Number</th><th>Batch Details</th></tr>
			"""
                for skuRow in issue.sku_details:
                    message2 += "<tr><td>"+skuRow.sku_code + "</td><td>"+skuRow.sku_name + "</td><td>" + skuRow.damaged_missing_quantity + "</td><td>" + skuRow.invoice_number + "</td><td>" + skuRow.batch_details + "</td><tr>"
                message2 += "</table><br>"
                message3 = """<br><br><br>
                Regards,<br>
                Hector Beverages"""
                msg= salutation + emailMessage + message2 + message3
                frappe.sendmail(subject="Transit Complaint: Ticket Pending since 3 Days", content=msg, recipients = '{}'.format(financeTeamEmail[i]) ,sender="Notification@hectorbeverages.com")
                print("\n email sent \n")


        if (issue.workflow_state == 'Requested for More Details by Supply Team' and daysDiffrence(issue.request_details_supply_team_time) >= 3):
            salutation = "Hello " + complaintTeamName + ",<br><br>"
            message2 = """<table border="1" cellspacing="0" cellpadding="5" align="">
			<tr><th>SKU Code</th><th>SKU Name</th><th>Damaged /Missing Quantity</th><th>Invoice Number</th><th>Batch Details</th></tr>
			"""
            for skuRow in issue.sku_details:
                message2 += "<tr><td>"+skuRow.sku_code + "</td><td>"+skuRow.sku_name + "</td><td>" + skuRow.damaged_missing_quantity + "</td><td>" + skuRow.invoice_number + "</td><td>" + skuRow.batch_details + "</td><tr>"
            message2 += "</table><br>"
            message3 = """<br><br><br>
            Regards,<br>
            Hector Beverages"""
            msg= salutation + emailMessage + message2 + message3
            frappe.sendmail(subject="Transit Complaint: Ticket Pending since 3 Days", content=msg, recipients = '{}'.format(complaintTeamEmail),sender="Notification@hectorbeverages.com")
            print("\n email sent \n")

        if (issue.workflow_state == 'Requested for More Details by Finance Team' and daysDiffrence(issue.request_details_finance_team_time) >= 3):
            for i in range(len(supplyTeamEmail)):
                salutation = "Hello " + frappe.get_doc('User', supplyTeamEmail[i]).full_name + ",<br><br>"
                message2 = """<table border="1" cellspacing="0" cellpadding="5" align="">
			<tr><th>SKU Code</th><th>SKU Name</th><th>Damaged /Missing Quantity</th><th>Invoice Number</th><th>Batch Details</th></tr>
			"""
                for skuRow in issue.sku_details:
                    message2 += "<tr><td>"+skuRow.sku_code + "</td><td>"+skuRow.sku_name + "</td><td>" + skuRow.damaged_missing_quantity + "</td><td>" + skuRow.invoice_number + "</td><td>" + skuRow.batch_details + "</td><tr>"
                message2 += "</table><br>"
                message3 = """<br><br><br>
                Regards,<br>
                Hector Beverages"""
                msg= salutation + emailMessage + message2 + message3
                frappe.sendmail(subject="Transit Complaint: Ticket Pending since 3 Days", content=msg, recipients = '{}'.format(supplyTeamEmail[i]) ,sender="Notification@hectorbeverages.com")
                print("\n email sent \n")
