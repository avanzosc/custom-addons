# -*- coding: utf-8 -*-
# (c) 2016 Daniel Campos <danielcampos@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, models, fields


class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.model
    def _get_group(self):
        result = super(ResUsers, self)._get_group()
        dataobj = self.env['ir.model.data']
        try:
            dummy, group_id = dataobj.sudo().get_object_reference(
                'ds_custom', 'group_ds_portal_user')
            result.append(group_id)
        except ValueError:
            # If these groups does not exists anymore
            pass
        return result

    groups_id = fields.Many2many(
        comodel_name='res.groups', relation='res_groups_users_rel',
        column1='uid', column2='gid', string='Groups', default=_get_group)
