# -*- coding: utf-8 -*-
# Copyright (c) 2021, Atrina Technologies Pvt Ltd and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
import random
from datetime import timedelta

class EmailOTPVerification(Document):
    def before_insert(self):
        self.otp = "".join((random.choice("0123456789") for i in range(4))) 
        self.expiry = frappe.utils.now_datetime() + timedelta(minutes=180)
