import frappe
from frappe import _
from frappe.utils.data import today, date_diff, get_datetime_str
import json

def successful_login(login_manager):
    """
    on login verify if site is not expired
    """
    expiry = frappe.db.get_single_value('Limiting Doc','site_expiry_date')
    email = frappe.db.get_single_value('Limiting Doc', 'support_email')
    contact = frappe.db.get_single_value('Limiting Doc',"support_contact")
    print(expiry)

    diff = date_diff(expiry,today())
    if login_manager.user != 'Administrator' and diff < 0:
            frappe.throw(_('You site is suspended. Please contact PowerSoft <br> Email: {0} <br>Phone: {1}").format(email,phone), frappe.AuthenticationErro'))

    def user_limit(self,method):
          no_user = frappe.db.get_single_value("Limiting Doc",'no_of_users')
          print(no_user)
    
    