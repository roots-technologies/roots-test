# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class ComptaPayeRule(models.Model):
	_inherit = 'hr.salary.rule'

	compte_debit_id = fields.Many2one(
	    'account.account',
	    string='Compte de débit',
	 )
	compte_credit_id = fields.Many2one(
	    'account.account',
	    string='Compte de crédit',
	)



class ComptaPayeRuleCategory(models.Model):
	_inherit = 'hr.salary.rule.category'

	compte_debit_id = fields.Many2one(
	    'account.account',
	    string='Compte de débit',
	 )
	compte_credit_id = fields.Many2one(
	    'account.account',
	    string='Compte de crédit',
	)