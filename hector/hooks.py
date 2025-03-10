# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "hector"
app_title = "Hector"
app_publisher = "Atrina Technologies Pvt Ltd"
app_description = "Hector"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "developers@atriina.com"
app_license = "MIT"
app_logo_url = "/assets/hector/images/logo_hector.png"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/hector/css/hector.css"
# app_include_js = "/assets/hector/js/hector.js"

# include js, css files in header of web template
# web_include_css = "/assets/hector/css/hector.css"
# web_include_js = "/assets/hector/js/hector.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {"Lead" : "public/js/lead.js"}
doctype_list_js = {"Lead" : "public/js/lead_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "hector.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "hector.install.before_install"
# after_install = "hector.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "hector.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
permission_query_conditions = {
    # "Customer": "hector.permissions.customer_query",
	"Primary Customer Form": "hector.permissions.primary_customer_form_query",
	"Secondary Customer Form": "hector.permissions.secondary_customer_form_query",
	"Quality Issue": "hector.permissions.quality_issue_query"
}
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }


email_brand_image = "/assets/hector/images/logo_hector.png"

website_context = {
	"favicon": 	"/assets/hector/images/logo_hector.png",
	"splash_image": "/assets/hector/images/logo_hector.png"
}

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
    "Lead": {
 	    "on_update": "hector.lead.on_update",
# 		"on_cancel": "method",
# 		"on_trash": "method"
    }
}

# Scheduled Tasks
# ---------------

scheduler_events = {
	# "all": [
	# 	"hector.tasks.all"
	# ],
	"daily": [
		"hector.tasks.quality_issue_daily",
		"hector.tasks.transit_issue_daily"
	],
	# "hourly": [
	# 	"hector.tasks.quality_issue_daily",
	# 	"hector.tasks.transit_issue_daily"
	# ],
	# "weekly": [
	# 	"hector.tasks.weekly"
	# ]
	# "monthly": [
	# 	"hector.tasks.monthly"
	# ]
}

# Testing
# -------

# before_tests = "hector.install.before_tests"

# Overriding Methods
# ------------------------------
#
override_whitelisted_methods = {
	"frappe.website.doctype.web_form.web_form.accept": "hector.web_form.accept"
}
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "hector.task.get_dashboard_data"
# }

