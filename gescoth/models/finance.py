        # -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import *
import datetime

class GescothPayementEleve(models.Model):
    _name = 'gescoth.paiement.eleve'
    _description = 'Gestion des paiement des élèves'
    _inherit = ['mail.thread','mail.activity.mixin']
    _rec_name = 'numer_recu'

    numer_recu = fields.Char(
        string="N° de reçu", 
        readonly=True, 
        required=True, 
        copy=False, 
        default='Nouveau',
        track_visibility='always',
    )

    eleve_id = fields.Many2one(
    	'gescoth.eleve',
    	string='Elève',
    	required=True,
    )
    date_paiement = fields.Date(
        string='Date de paiement',
        required=True,
        default=datetime.date.today(),
        track_visibility='always',
    )

    montant = fields.Float(
        string='Montant du paiement',
        required=True,
        track_visibility='onchange',
    )
    classe_id = fields.Many2one(
        'gescoth.classe',
        string='Classe',
        store=True,
        required=True,
        track_visibility='always',
    )
    recu_manuel = fields.Char(string="N° du recu manuel")
    annee_scolaire_id = fields.Many2one(
        'gescoth.anneescolaire',
        string='Année scolaire',
        required=True,
        default=lambda self: int(self.env['ir.config_parameter'].sudo().get_param('gescoth.annee_scolaire_id')),
    )
    responsable_id = fields.Many2one(
        'res.users',
        string='Responsable',
        default=lambda self: self.env.user.id,
        readonly=True,
    )
    state = fields.Selection([
        ('draft','Brouillon'),
        ('confirmed','Confirmé'),
        ('cancel','Annulé'),
    ], default='draft', readonly=True, track_visibility='onchange',)

    def confirmer_paiement(self):
        for rec in self:
            rec.state = 'confirmed'

    def annuler_payement(self):
        for rec in self:
            rec.state = 'cancel'

    def mettre_en_brouillon(self):
        for rec in self:
            rec.state = 'draft'

    @api.multi
    def unlink(self):
        if self.state in ['confirmed','cancel']:
            raise ValidationError(_('Les paiements en status confirmé ou annulé ne peuvent pas être supprimer'))
        return super(GescothPayementEleve, self).unlink()


    def envoyer_carte_eleve(self):
        template_id= self.env.ref('gescoth.eleve_paiement_template').id
        template = self.env['mail.template'].browse(template_id)
        template.send_mail(self.id, force_send=True)

    @api.onchange('eleve_id')
    def _onchange_eleve_id(self):
        for rec in self:
            rec.classe_id = rec.eleve_id.classe.id

    @api.model
    def create(self, vals):
        if vals.get('numer_recu', 'Nouveau') == 'Nouveau':
            vals['numer_recu'] = self.env['ir.sequence'].next_by_code(
                'gescoth.paiement.eleve') or 'Nouveau'
        result = super(GescothPayementEleve, self).create(vals)
        return result

class GescothTranche(models.Model):
    _name = 'gescoth.tranche'
    _description = 'Tranche'
    _rec_name = "eleve_id"

    eleve_id = fields.Many2one(
        'gescoth.eleve',
        string='Elève',
        required=True,
    )
    date = fields.Date(
        string='Date',
        required=True,
    )
    montant = fields.Float(
        string='Montant',
        required=True,
    )
    montat_deja_paye = fields.Float(
        string='Montant déjà payé',
    )
    nombre = fields.Integer(
        string='Nombre de payement',
        default=5, required=True,
    )
    date_premier_tranche = fields.Date(string="Date de la première tranche", required=True,)
    line_ids = fields.One2many('gescoth.tranche.line','tranche_id', string="Linge de tranche")


    def calculer_tranche(self):
        reste_a_payer = self.montant - self.montat_deja_paye
        traches = self.env['gescoth.tranche.line'].search([('tranche_id','=', self.id)])
        for t in traches:
            t.unlink()
        my_date = self.date_premier_tranche
        for n in range(0, self.nombre):
            vals ={
                'date_echeanche': my_date,
                'montant': (reste_a_payer / self.nombre),
                'paye': False,
                'tranche_id': self.id,
            }
            my_date = my_date + timedelta(days=30)
            my_date = date(my_date.year, my_date.month, self.date_premier_tranche.day)

            self.env['gescoth.tranche.line'].create(vals)

class GescothPaiementLine(models.Model):
    _name = 'gescoth.tranche.line'
    _description = 'Ligne de tranche'

    date_echeanche = fields.Date(string="Date d'échéance", required=True,)
    montant = fields.Float(string="Montant", required=True,)
    paye = fields.Boolean(string="Payé", default=False,)
    tranche_id = fields.Many2one(
        'gescoth.tranche',
        string='Tranche', required=True,
    )

class GescothDepense(models.Model):
    _name = 'gescoth.depense'
    _description = 'Dépense'

    name = fields.Char(
        string='Libellé',
        required=True,
    )
    date_depense = fields.Date(
        string='Date',
        required=True,
        default=datetime.date.today(),
    )
    montant = fields.Float(string="Montant",required=True,)
    partenaire_id = fields.Many2one(
        'res.partner',
        string='Partenaire',
    )
    responsable_id = fields.Many2one(
        'res.users',
        string='Responsable',
        default=lambda self: self.env.user.id,
        readonly=True,
        )    


class GescothRecette(models.Model):
    _name = 'gescoth.recette'
    _description = 'Recette'

    name = fields.Char(
        string='Libellé',
        required=True,
    )
    date_depense = fields.Date(
        string='Date',
        required=True,
        default=datetime.date.today(),
    )
    montant = fields.Float(string="Montant",required=True,)
    partenaire_id = fields.Many2one(
        'res.partner',
        string='Partenaire',
    )
    responsable_id = fields.Many2one(
        'res.users',
        string='Responsable',
        default=lambda self: self.env.user.id,
        readonly=True,
        )
