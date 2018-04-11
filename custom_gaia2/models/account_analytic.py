# Copyright 2018 Mikel Arregi Etxaniz - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models

class AccountAnalytic(models.Model):
    _inherit='account.analytic.account'
    
    project_area=fields.Many2one(comodel_name='project.area', 
                                    string ='Project Area')
    project_espaces=fields.Many2one(comodel_name='project.espaces',
                                          string='Project Espaces')
    project_id=fields.Many2one(comodel_name='project.id',
                                              string='Project Id')
    project_pe=fields.Many2one(comodel_name='project.pe',
                                     string ='Project PE')
    project_teams=fields.Many2one(comodel_name='project.teams',
                                          string='Project Teams')
    project_nature=fields.Many2one(comodel_name='project.nature',
                                             string='Project Nature')
    project_sector_objetive=fields.Many2one(comodel_name='project.sector_objetive',
                                             string='Project Sector Objetive')
    project_financiation=fields.Many2one(comodel_name='project.financiation',
                                         string='Project Financiation')
class Project(models.Model):
    
    _inherit='project.project'

    project_area=fields.Many2one(comodel_name='project.area',
                                    string='Project Area',
                                    related='analytic_account_id.project_area')
    project_espaces=fields.Many2one(comodel_name='project.espaces',
                                    string='Project Espaces',
                                    related='analytic_account_id.project_espaces')
    project_id=fields.Many2one(comodel_name='project.id',
                                    string='Project Id',
                                    related='analytic_account_id.project_id')
    project_pe=fields.Many2one(comodel_name='project.pe',
                                    string='Project Pe',
                                    related='analytic_account_id.project_pe')
    project_teams=fields.Many2one(comodel_name='project.teams',
                                    string='Project Teams',
                                    related='analytic_account_id.project_teams')
    project_nature=fields.Many2one(comodel_name='project.nature',
                                    string='Project Nature',
                                    related='analytic_account_id.project_nature')
    project_sector_objetive=fields.Many2one(comodel_name='project.sector_objetive',
                                    string='Project Sector Objetive',
                                    related='analytic_account_id.project_sector_objetive')
    project_financiation=fields.Many2one(comodel_name='project.financiation',
                                    string='Project Financiation',
                                    related='analytic_account_id.project_financiation')
class AccountArea(models.Model):
    
    _name='account.area' 
    name=fields.Char(string ='Name')
    description=fields.Char(string ='Description')
class AccountEspaces(models.Model):
    
    _name='account.espaces'
    name=fields.Char(string='Name')
    description=fields.Char(string ='Description')

class AccountOportunity(models.Model):
    
    _name='account.oportunity'
    name=fields.Char(string='Name')
    description=fields.Char(string='Description')
class AccountPe(models.Model):
    _name='account.pe'
    name=fields.Char(string='Name')
    oportunity_id=fields.Integer(string='Id')
    description=fields.Char(string='Description')
class AccountTeams(models.Model):
    _name='account.teams' 

    name=fields.Char(string='Name')
    description=fields.Char(string ='Description')

class AccountNature(models.Model):
    _name='account.nature'
    
    name=fields.Char(string='Name')
    description=fields.Char(string ='Description')

class AccountSectorObjetive(models.Model):
    _name='account.sector_objetive'
    
    name=fields.Char(string='Name')
    description=fields.Char(string='Description')

class AccountFinanciation(models.Model):
    #ALDAKETAK: tipo de financiacion(subencion, credito blando, mixto)
    # programa de financiacion partner_id may ¿zone?
    _name='account.financiation'

    name=fields.Char(string='Name')
    description=fields.Char(string='Description')
    grant=fields.Char(string='Grant')#SUBVENCION
    soft_credit=fields.Char(string='Soft Credit')#credito blando
    mixed_credit=fields.Char(string='Mixed Credit')#credito mixto
    partner_id=fields.Char(string='Partner Id')
    finantiation_account=fields.Char(string='Finantiation account')
    
    external_attendees=fields.Many2many(comodel_name='res.partner',
                                        string='External attendees')
    internal_attendees=fields.Many2many(comodel_name='res.users',
                                        string='Internal attendees')
  

