# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from ast import literal_eval

class GescothSettings(models.TransientModel):
	_inherit = 'res.config.settings'

	chef_etablissement = fields.Many2one(
	    'gescoth.personnel',
	    string="Chef d'établissement",
	) 
	annee_scolaire_id = fields.Many2one(
	    'gescoth.anneescolaire',
	    string='Année scolaire',
	)
	ville = fields.Char(
	    string='Fait à',
	)
	head_image_path = fields.Char(
	    string='Entete de page',
	)
	entete = fields.Binary(
	    string='Entete de page',
	    attachment=True,
	)
	cle_activation  = fields.Char(
	    string='Clé d\'activation',
	)

	@api.model
	def set_values(self):
		res = super(GescothSettings, self).set_values()
		self.env['ir.config_parameter'].set_param('gescoth.chef_etablissement', self.chef_etablissement.id)	
		self.env['ir.config_parameter'].set_param('gescoth.annee_scolaire_id', self.annee_scolaire_id.id)	
		self.env['ir.config_parameter'].set_param('gescoth.ville', self.ville)	
		self.env['ir.config_parameter'].set_param('gescoth.entete', self.entete)
		self.env['ir.config_parameter'].set_param('gescoth.activate', self.cle_activation)
		return res

	@api.model
	def get_values(self):
		res = super(GescothSettings, self).get_values()
		ICPSudo = self.env['ir.config_parameter'].sudo()
		_chef_etablissement = int(ICPSudo.get_param('gescoth.chef_etablissement'))
		_annee_scolaire_id = int(ICPSudo.get_param('gescoth.annee_scolaire_id'))
		_ville = ICPSudo.get_param('gescoth.ville')
		_entete = ICPSudo.get_param('gescoth.entete')
		_cle_activation = ICPSudo.get_param('gescoth.cle_activation')
		res.update(
			chef_etablissement = _chef_etablissement,
			annee_scolaire_id = _annee_scolaire_id,
			ville = _ville,
			entete = _entete,
			cle_activation = _cle_activation,
		)
		return res