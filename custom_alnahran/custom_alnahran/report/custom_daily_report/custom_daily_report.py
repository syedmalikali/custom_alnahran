# Copyright (c) 2013, C.R.I.O and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

def execute(filters=None):
	columns, data = [], []
	if filters:
		columns = get_column()
		data = get_data(filters)
	return columns, data

def get_column():
	columns = [
		{
		"label": "Voucher Type",
		"fieldname": "inward_voucher_type",
		"fieldtype": "Data",
		"width": 150
	},
		{
		"label": "Voucher No",
		"fieldname": "voucher_no",
		"fieldtype": "Dynamic Link",
		"options": "inward_voucher_type",
		"width": 200
	},
	# {
	# 	"fieldname": "branch",
	# 	"label":"Branch",
	# 	"fieldtype": "Link",
	# 	"options": "Branch",
	# 	"width": 150
	# },
	# {
	# 	"label": "Payment Mode",
	# 	"fieldname": "in_payment_mode",
	# 	"fieldtype": "Data",
	# 	"width": 150
	# },
	{
		"label": "Inward",
		"fieldname": "in_amount",
		"fieldtype": "Currency",
		"width": 160
	},
	{
		"label": "Outward",
		"fieldname": "ex_amount",
		"fieldtype": "Currency",
		"width": 160
	},
	# {
	# 	"label": "Remarks",
	# 	"fieldname": "in_remarks",
	# 	"fieldtype": "Data",
	# 	"width": 200
	# },
	# {
	# 	"label": "Party Type",
	# 	"fieldname": "party_type",
	# 	"fieldtype": "Data",
	# 	"width": 100
	# },
		{
		"label": "Party",
		"fieldname": "party",
		"fieldtype": "Dynamic Link",
		"options": "party_type",
		"width": 200
	},
	]
	return columns

def get_data(filters):
	data =[]
	si_cash_type = frappe.db.sql("""select %s as inward_voucher_type, si.name as voucher_no, si.custom_branch as branch,
					sip.amount as in_amount, si.remarks as in_remarks,
					sip.mode_of_payment as in_payment_mode, si.customer as party, %s as party_type
					from `tabSales Invoice` si join `tabSales Invoice Payment` sip
					on sip.parent = si.name
					where (sip.mode_of_payment = "AMAL CASH" or sip.mode_of_payment = "DAMMAM CASH" or sip.mode_of_payment = "KHAMIS CASH" or sip.mode_of_payment = "LIFETIME NAJ CASH" or sip.mode_of_payment = "LIFETIME-1 CASH" or sip.mode_of_payment = "LIFETIME-2 CASH" or sip.mode_of_payment = "VANSALE-1 CASH" or sip.mode_of_payment = "VANSALE-2 CASH") and si.posting_date 
					between %s and %s and si.docstatus = 1 and (si.status = 'Paid' or si.status = 'Credit Note Issued') """,
					('Sales Invoice','Customer', filters['cf_date'],filters['cf_date']),  as_dict = True)
	
	pi_cash_type = frappe.db.sql("""select %s as inward_voucher_type, pi.name as voucher_no, pi.custom_branch as branch,
					pi.paid_amount as ex_amount,
					pi.mode_of_payment as in_payment_mode, pi.supplier as party, %s as party_type
					from `tabPurchase Invoice` pi 
					where (pi.mode_of_payment = "AMAL CASH" or pi.mode_of_payment = "DAMMAM CASH" or pi.mode_of_payment = "KHAMIS CASH" or pi.mode_of_payment = "LIFETIME NAJ CASH" or pi.mode_of_payment = "LIFETIME-1 CASH" or pi.mode_of_payment = "LIFETIME-2 CASH" or pi.mode_of_payment = "VANSALE-1 CASH" or pi.mode_of_payment = "VANSALE-2 CASH") and pi.posting_date 
					between %s and %s and pi.docstatus = 1 and (pi.status = 'Paid' or pi.status = 'Debit Note Issued') """,
					('Purchase Invoice','Supplier', filters['cf_date'],filters['cf_date']),  as_dict = True)

	return_si = frappe.db.sql("""select %s as inward_voucher_type, si.name as voucher_no, si.custom_branch as branch,
					si.paid_amount as in_amount, si.remarks as in_remarks,
					sip.mode_of_payment as in_payment_mode, si.customer as party, %s as party_type
					from `tabSales Invoice` si join `tabSales Invoice Payment` sip
					on sip.parent = si.name
					where (sip.mode_of_payment = "AMAL CASH" or sip.mode_of_payment = "DAMMAM CASH" or sip.mode_of_payment = "KHAMIS CASH" or sip.mode_of_payment = "LIFETIME NAJ CASH" or sip.mode_of_payment = "LIFETIME-1 CASH" or sip.mode_of_payment = "LIFETIME-2 CASH" or sip.mode_of_payment = "VANSALE-1 CASH" or sip.mode_of_payment = "VANSALE-2 CASH") and si.posting_date 
					between %s and %s and si.docstatus = 1 and si.is_return = 1 and si.status = 'Return'""",
					('Sales Invoice','Customer',filters['cf_date'],filters['cf_date']),  as_dict = True)
	
	return_pi = frappe.db.sql("""select %s as inward_voucher_type, pi.name as voucher_no, pi.custom_branch as branch,
					pi.paid_amount as in_amount,
					pi.mode_of_payment as in_payment_mode, pi.supplier as party, %s as party_type
					from `tabPurchase Invoice` pi
					where (pi.mode_of_payment = "AMAL CASH" or pi.mode_of_payment = "DAMMAM CASH" or pi.mode_of_payment = "KHAMIS CASH" or pi.mode_of_payment = "LIFETIME NAJ CASH" or pi.mode_of_payment = "LIFETIME-1 CASH" or pi.mode_of_payment = "LIFETIME-2 CASH" or pi.mode_of_payment = "VANSALE-1 CASH" or pi.mode_of_payment = "VANSALE-2 CASH") and pi.posting_date 
					between %s and %s and pi.docstatus = 1 and pi.is_return = 1 and pi.status = 'Return'""",
					('Purchase Invoice','Supplier',filters['cf_date'],filters['cf_date']),  as_dict = True)

	pe_list_rc = frappe.db.sql('''select %s as inward_voucher_type, pe.name as voucher_no, pe.custom_branch as branch,
					pe.paid_amount as in_amount, pe.remarks as in_remarks,
					pe.mode_of_payment as in_payment_mode, pe.party_type, pe.party
					from `tabPayment Entry` pe 
					where pe.payment_type = "Receive" and (pe.mode_of_payment = "AMAL CASH" or pe.mode_of_payment = "DAMMAM CASH" or pe.mode_of_payment = "KHAMIS CASH" or pe.mode_of_payment = "LIFETIME NAJ CASH" or pe.mode_of_payment = "LIFETIME-1 CASH" or pe.mode_of_payment = "LIFETIME-2 CASH" or pe.mode_of_payment = "VANSALE-1 CASH" or pe.mode_of_payment = "VANSALE-2 CASH") and pe.posting_date 
					between %s and %s and pe.docstatus = 1''',
					('Payment Entry',filters['cf_date'],filters['cf_date']),  as_dict = True)

	cust_pe_list_pay = frappe.db.sql('''select %s as inward_voucher_type, pe.name as voucher_no, pe.custom_branch as branch,
					pe.paid_amount as ex_amount, pe.remarks as in_remarks,
					pe.mode_of_payment as in_payment_mode, pe.party_type, pe.party
					from `tabPayment Entry` pe 
					where pe.payment_type = "Pay" and pe.party_type = 'Customer' and (pe.mode_of_payment = "AMAL CASH" or pe.mode_of_payment = "DAMMAM CASH" or pe.mode_of_payment = "KHAMIS CASH" or pe.mode_of_payment = "LIFETIME NAJ CASH" or pe.mode_of_payment = "LIFETIME-1 CASH" or pe.mode_of_payment = "LIFETIME-2 CASH" or pe.mode_of_payment = "VANSALE-1 CASH" or pe.mode_of_payment = "VANSALE-2 CASH") and pe.posting_date  
					between %s and %s and pe.docstatus = 1''',
					('Payment Entry',filters['cf_date'],filters['cf_date']),  as_dict = True)
	
	common_pe_list_pay = frappe.db.sql('''select %s as inward_voucher_type, pe.name as voucher_no, pe.custom_branch as branch,
					pe.paid_amount as ex_amount, pe.remarks as in_remarks,
					pe.mode_of_payment as in_payment_mode, pe.party_type, pe.party
					from `tabPayment Entry` pe 
					where pe.payment_type = "Pay" and (pe.party_type = 'Supplier' or pe.party_type = 'Employee') and (pe.mode_of_payment = "AMAL CASH" or pe.mode_of_payment = "DAMMAM CASH" or pe.mode_of_payment = "KHAMIS CASH" or pe.mode_of_payment = "LIFETIME NAJ CASH" or pe.mode_of_payment = "LIFETIME-1 CASH" or pe.mode_of_payment = "LIFETIME-2 CASH" or pe.mode_of_payment = "VANSALE-1 CASH" or pe.mode_of_payment = "VANSALE-2 CASH") and pe.posting_date  
					between %s and %s and pe.docstatus = 1''',
					('Payment Entry',filters['cf_date'],filters['cf_date']),  as_dict = True)
	
	je_list = []
	journal_entries = frappe.get_list('Journal Entry',{'voucher_type':'Journal Entry','docstatus':1,
						"posting_date": ["between", (filters['cf_date'],filters['cf_date'])],})
	
	cash_account = frappe.db.get_single_value('ALNahran Settings', 'cash_account')
	for je in journal_entries:
		doc = frappe.get_doc('Journal Entry',je['name'])
		for row in doc.accounts:
			if row.account == cash_account:
				if row.debit_in_account_currency:
					je_list.append({
						'inward_voucher_type': 'Journal Entry',
						'voucher_no' : doc.name,
						'in_amount' : row.debit_in_account_currency,
						'in_remarks' : doc.remark,
						'in_payment_mode' : 'Cash'
					})
				if row.credit_in_account_currency:
					je_list.append({
						'inward_voucher_type': 'Journal Entry',
						'voucher_no' : doc.name,
						'ex_amount' : row.credit_in_account_currency,
						'in_remarks' : doc.remark,
						'in_payment_mode' : 'Cash'
					})			

	# je_list = frappe.db.sql('''select  %s as inward_voucher_type, je.name as voucher_no, 
	# 			je.total_debit as in_amount, je.remark as in_remarks, 'Cash' as in_payment_mode
	# 			from `tabJournal Entry` je
	# 			where je.voucher_type = 'Cash Entry' and je.posting_date  between %s and %s 
	# 			and je.docstatus = 1''',
	# 			('Journal Entry',filters['cf_date'],filters['cf_date']),  as_dict = True)
	# je_list = frappe.db.sql(f"""

	# 		select 
	# 		'Journal Entry' as inward_voucher_type, 
	# 		je.name as voucher_no, 
	# 		jea.debit_in_account_currency as in_amount,
	# 		jea.credit_in_account_currency as ex_amount,
	# 		je.remark as in_remarks,
	# 		jea.account as acc,
	# 		'Cash' as in_payment_mode 
	# 		from 
	# 		`tabJournal Entry` je 
	# 		left join `tabJournal Entry Account` jea on je.name = jea.parent and jea.account  LIKE "%Cash In Hand%"
	# 		where 
	# 		je.voucher_type = 'Cash Entry' 
	# 		and je.posting_date between '{filters['cf_date']}'
	# 		and '{filters['cf_date']}' 
	# 		and je.docstatus = 1
	# 		group by je.name
	
	# 				""",  as_dict = True)
	data = si_cash_type +pi_cash_type+ return_si +return_pi+ pe_list_rc  + je_list + cust_pe_list_pay + common_pe_list_pay
	final_result = []
	for i in data:
		if filters.get('custom_branch'):
			if i.get('branch') and i.get('branch') != filters.get('custom_branch'):
				continue
				
		if not 'in_amount' in i:
			i['in_amount'] = 0
		if not 'ex_amount' in i:
			i['ex_amount'] = 0
		if 'in_amount' in i and i['in_amount'] and i['in_amount']<0 :
			i['ex_amount'] = abs(i['in_amount'])
			i['in_amount']= 0

		if i['ex_amount'] < 0 and i['in_payment_mode']!='Cash':
			i['ex_amount']=i['in_amount']
		
		if i['inward_voucher_type'] == 'Journal Entry':
			jea_list = frappe.db.get_list('Journal Entry Account', {'parent': i['voucher_no']},['party_type', 'party'], ignore_permissions=True)
			for row in jea_list:
				if row['party_type']:
					i['party_type'] = row['party_type']
				if row['party']:
					i['party'] = row['party']
		final_result.append(i)
	

	data = final_result
	totals = calculate_amount(data,filters)
	data += totals

	return data


def calculate_amount(entries,filters):
	# je_list_total = frappe.db.sql(f"""

    #     select 
    #       'Journal Entry' as inward_voucher_type, 
    #       je.name as voucher_no,
    #       sum(jea.debit_in_account_currency) as ex_amount,
    #       sum(jea.credit_in_account_currency) as in_amount,
    #       je.remark as in_remarks,
    #       jea.account as acc,
    #       'Cash' as in_payment_mode 
    #     from 
    #       `tabJournal Entry` je 
    #      left join `tabJournal Entry Account` jea on je.name = jea.parent and jea.account  LIKE "%Cash In Hand%"
    #     where 
    #       je.voucher_type = 'Cash Entry' 
    #       and je.posting_date between '2022-11-14'
    #       and '2022-11-14' 
    #       and je.docstatus = 1
    #             """,  as_dict = True)

	# jet = 0
	# if je_list_total[0]['ex_amount'] != 0:
	# 	jet= je_list_total[0]['ex_amount']

#  -  jet

	total = 0
	final_data  = []
	cl = abs(sum([entry['in_amount'] if 'in_amount' in entry and entry['in_payment_mode'] == 'Cash'  else 0 for entry in entries]) - sum([entry['ex_amount'] if 'ex_amount' in entry and entry['in_payment_mode'] == 'Cash'  else 0 for entry in entries]))
	total_in_amt = sum([entry['in_amount'] if 'in_amount' in entry else 0 for entry in entries])
	total_sales = sum([entry['in_amount'] if 'in_amount' in entry and entry['inward_voucher_type']!='Journal Entry' else 0 for entry in entries])
	total_ex_amt = sum([entry['ex_amount'] if 'ex_amount' in entry else 0 for entry in entries])
	opening = filters['cf_opening_balance'] if 'cf_opening_balance' in filters else 0
	total = opening + total_in_amt
	final_data += [{'in_amount':total_in_amt, 'ex_amount': total_ex_amt}, {'in_payment_mode':frappe.bold('Opening'), 'in_amount':opening}, {'in_payment_mode':frappe.bold('Total'), 'in_amount': total, 'ex_amount': total_ex_amt},
	{'in_payment_mode':frappe.bold('Less Expenses'), 'in_amount': -total_ex_amt},
	{'in_payment_mode':frappe.bold('Closing Cash'), 'in_amount': total-total_ex_amt}
	]

	# is_denomination_exist = frappe.db.get_value('Cash Denomination', {'date': filters['cf_date'], 'docstatus': 1})
	# if is_denomination_exist:
	# 	closing_cash = frappe.db.get_value('Cash Denomination', is_denomination_exist, 'total_amount')
	# 	denomination_list = frappe.get_list('Cash Denominations Details', {'parent': is_denomination_exist}, ['denomination','count','total'], ignore_permissions=True)
	# 	ordered_list = [['2000', 0, 0], ['500', 0, 0], ['200', 0, 0], ['100', 0, 0], ['50', 0, 0], ['20', 0, 0], ['10', 0, 0]]
	# 	for row in denomination_list[::-1]:
	# 		for row1 in ordered_list:
	# 			if row.get('denomination') == row1[0]:
	# 				row1[1] = row.get('count') if row.count else 0
	# 				row1[2] = row.get('total') if row.total else 0
	# 	if closing_cash:
	# 		final_data += [{'in_payment_mode':frappe.bold('Difference'), 'in_amount': (total-total_ex_amt) - (closing_cash)}]
	# 	final_data += [{'voucher_no':'', 'in_payment_mode':'', 'in_amount':''}]
	# 	for row in ordered_list:
	# 		final_data += [{'voucher_no':frappe.bold(row[0]), 'in_payment_mode':row[1], 'in_amount':row[2]}]

	# 	final_data += [{'voucher_no':'', 'in_payment_mode':'', 'in_amount':closing_cash}]
	# 	if closing_cash:
	# 		if frappe.db.exists('Daily Summary Balance',{'date':filters['cf_date']}):
	# 			frappe.db.set_value('Daily Summary Balance',{'date':filters['cf_date']},'amount',closing_cash)
	# 		else:
	# 			frappe.get_doc({'doctype':'Daily Summary Balance', 'date':filters['cf_date'],'amount':closing_cash}).insert()
	# 		final_data += [
	# 		{'inward_voucher_type':frappe.bold('**Closing Cash**'), 'voucher_no': frappe.bold(closing_cash)},
	# 		{'inward_voucher_type':frappe.bold('**Total Sales** '), 'voucher_no': frappe.bold(total_sales)}]
	
	frappe.db.commit()
	
	return final_data