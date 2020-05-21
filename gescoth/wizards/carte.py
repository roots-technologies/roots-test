# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from datetime import *
from odoo.exceptions import ValidationError
import base64

class GescothCarte(models.TransientModel):
    _name = 'gescoth.carte'
    _description = 'Carte'

    classe_id = fields.Many2one(
        'gescoth.classe',
        string='Classe',
        required=True,
    )
    annee_scolaire_id = fields.Many2one(
        'gescoth.anneescolaire',
        string='Année scolaire',
        required=True,
        default=lambda self: int(self.env['ir.config_parameter'].sudo().get_param('gescoth.annee_scolaire_id')),
    )

    def imprimer_cate_scolaire(self):
        data = {}
        eleves = self.env['gescoth.eleve'].search([('classe','=',self.classe_id.id)])
        chef_id = self.env['ir.config_parameter'].sudo().get_param('gescoth.chef_etablissement')
        if int(chef_id) <= 0 or chef_id == None:
            raise ValidationError(_('Veuillez vérifier les parmatres du chef détablissement'))
        chef = self.env['gescoth.personnel'].search([('id','=', chef_id)])[0]
        liste_eleves = []
        for el in eleves:
            date =''
            if el.date_naissance:
                date = el.date_naissance.strftime('%d/%m/%Y')
            else:
                ''
            vals = {
                'nom_eleve' : el.nom_eleve,
                'photo' : el.photo,
                'date_naissance' : date,
                'lieu_naissance' : el.lieu_naissance,
                'sexe' : 'Masculin' if el.sexe == 'masculin' else 'Féminin',
                'nationalite' : el.nationalite,
                'classe' : el.classe.name,
                'statut' : el.statut,
                'Apt_sport' : el.Apt_sport,
                'anneescolaire':self.annee_scolaire_id.name,
                'chef_etablissement':chef.name,
            }
            liste_eleves.append(vals)
        data['Liste_eleve'] = liste_eleves
        data['entete'] = self.env['ir.config_parameter'].sudo().get_param('gescoth.entete')
        return self.env.ref('gescoth.carte_report_view').report_action(self, data=data)