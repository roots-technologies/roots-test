# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

# classe pour gérer les matières
class GescothMatiere(models.Model):
	_name = 'gescoth.matiere'
	_description = 'Gestion des matière'
	_sql_constraints = [
	('name_uniq', 'unique (name)', _('Cette matière existe déjà !')),
	]

	name = fields.Char(string="Nom de la matière", required=True)
	nom_abrege = fields.Char(string="Nom abrégé")
	user_abrege = fields.Boolean(string="Utiliser le nom abrégé")
	type_matiere = fields.Selection([
		('theorie','Théorique'),
		('sport','Stportive')
	], 
	string="Type de matière", 
	default="theorie", 
	required=True,)


#classe pour ger les professeur
class GescothProfesseur(models.Model):
	_name = 'gescoth.professeur'
	_inherit = ['mail.thread','mail.activity.mixin']
	_description = 'Gestion des professeurs'

	name = fields.Char(string="Nom et prénoms", required=True, track_visibility='onchange')
	photo = fields.Binary(string="Photo de l'élève")
	date_naissance = fields.Date(string="Date de naissance",track_visibility='onchange')
	lieu_naissance = fields.Char(string="Lieu de naissance", track_visibility='onchange')
	sexe = fields.Selection([('masculin','Masculin'),('feminin','Féminin')], string="Sexe")
	nationalite = fields.Many2one('res.country', string="Nationalité")
	telephone = fields.Char(string="Téléphone", track_visibility='onchange')
	email =  fields.Char(string="E-mail")
	adresse= fields.Text(string="Adresse complète")
	date_service = fields.Date(
		string='Date de prise de service'
		)
	statut = fields.Selection([('volontaire','Volontaire'),('permanent','Permanent'),('partiel','Partiel')], string='Statut')
	matieres = fields.Many2many('gescoth.matiere', string="Matière enseignées")
	active = fields.Boolean(string="Active", default=True)



#classe pour gerer les classes
class GescothClasse(models.Model):
	_name = 'gescoth.classe'
	_description = 'Gestion des classes'
	_sql_constraints = [
	('name_uniq', 'unique (name)', _('Cette classe existe déjà !')),
	]

	name = fields.Char(string="Nom de la classe", required=True, index=True)
	description = fields.Char(string='Description')
	filiere = fields.Many2one('gescoth.filiere')
	professeur = fields.Many2one('gescoth.professeur', string="Professeur titulaire")
	coeficient_ids = fields.One2many('gescoth.coeficient', 'name', string="Coeficient de matières")
	eleve_ids =  fields.One2many('gescoth.eleve', 'classe', string="Liste des élèves")
	liste_des_eleves_total = fields.Integer(
	    string='Total',
	    compute="_liste_des_eleves_total"
	)

	@api.multi
	def liste_des_eleves(self):
		return{
			'name':('Elèves'),
			'domain':[('classe','=', self.id)],
			'view_type':'form',
			'res_model':'gescoth.eleve',
			'view_id':False,
			'view_mode':'tree,form',
			'type':'ir.actions.act_window',
		}

	def _liste_des_eleves_total(self):
		self.liste_des_eleves_total = len(self.env['gescoth.eleve'].search([('classe','=', self.id)]))


#classe pour gerer les filières(series)
class GescothFiliere(models.Model):
	_name = 'gescoth.filiere'
	_description = 'Gestion des filiere'
	_sql_constraints = [
	('name_uniq', 'unique (name)', _('Cette filiere existe déjà !')),
	]

	name = fields.Char(string="Nom de filiere", required=True)
	specialite = fields.Char(string="Spécialité")
	classe_ids = fields.One2many('gescoth.classe', 'filiere', string="Liste des classe")


class GescothAnneeScolaire(models.Model):
	_name = 'gescoth.anneescolaire'
	_description = 'Gestion des années scolaire'
	_sql_constraints = [
	('name_uniq', 'unique (name)', _('Cette années scolaire existe déjà !')),
	]

	name = fields.Char(string="Année scolaire", required=True)
	date_rentree = fields.Date(string="Date de la rentrée", required=True)
	date_vacance = fields.Date(string="Date des vacance")
	note = fields.Text(
		string='Notes',
		)


class gescothHoraire(models.Model):
    _name = 'gescoth.horaire'
    _description = 'Horaire'

    name = fields.Char(
    	string='Horaire',
    	required=True,
    )
    heure_debut = fields.Float(
        string='Heure de début',
        required=True,
    )
    heure_fin = fields.Float(
        string='Heure de fin',
        required=True,
    )


class gescothEmploiTemps(models.Model):
    _name = 'gescoth.emploi.temps'
    _description = 'Emploi du temps'
    _rec_name = 'jour'

    jour = fields.Selection([
    	('lundi','lundi'),
    	('mardi','Mardi'),
    	('mercredi','Mercredi'),
    	('jeudi','Jeudi'),
    	('vendredi','Vendredi'),
    	('samedi','Samedi'),
    	('dimanche','Dimanche'),
    ], string="Jour", required=True,)

    classe_id = fields.Many2one(
        'gescoth.classe',
        string='Classe',
        required=True,
    )
    professeur_id = fields.Many2one(
        'gescoth.professeur',
        string='Professeur',
        required=True,
    )

    horaire_id = fields.Many2one(
        'gescoth.horaire',
        string='Horaire',
    )
    heure_debut = fields.Float(
        string='Heure de début',
        # compute="_calculer_heure",
    )
    heure_fin = fields.Float(
        string='Heure de fin', 
        # compute="_calculer_heure",
    )

    @api.onchange('horaire_id')
    def _onchange_horaire_id(self):
        for rec in self:
        	rec.heure_fin = rec.horaire_id.heure_fin
        	rec.heure_debut = rec.horaire_id.heure_debut