# Copyright 2018 Mikel Arregi Etxaniz - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models


class ProjectArea(models.Model):
    _name='project.area'

    name=fields.Char(string='Name')
    description=fields.Char(string='Description')


class ProjectEspaces(models.Model):
    
    _name='project.espaces' 
    name=fields.Char(string='Name')
    description=fields.Char(string='Description')

class ProjectId(models.Model):
    
    _name='project.id'
    name=fields.Char(string='Name')
    description=fields.Char(string='Description')
    
class ProjectPE(models.Model):
    
    _name='project.pe' 
    name=fields.Char(string='Name')
    oportunity_id=fields.Integer(string='Id')
    description=fields.Char(string='Description')
    
class ProjectTeams(models.Model):
    _name='project.teams'

    name=fields.Char(string='Name')
    description=fields.Char(string='Description')

class ProjectNature(models.Model):
    _name='project.nature'
    
    name=fields.Char(string='Name')
    description=fields.Char(string='Description')

class ProjectSectorObjetive(models.Model):
    _name='project.sector_objetive'
    
    name=fields.Char(string='Name')
    description=fields.Char(string='Description')

class ProjectFinanciation(models.Model):
    _name='project.financiation'

    name=fields.Char(string='Name')
    description=fields.Char(string='Description')
    grant=fields.Char(string='Grant')#SUBVENCION
    soft_credit=fields.Char(string='Soft Credit')#credito blando
    mixed_credit=fields.Char(string='Mixed Credit')#credito mixto
    partner=fields.Char(string='Partner')
    finantiation_account=fields.Char(string='Finantiation account')
    
    external_attendees=fields.Many2many(comodel_name='res.partner',
                                             string='External attendees')
    internal_attendees=fields.Many2many(comodel_name='res.users',
                                          string='Internal attendees')
    
