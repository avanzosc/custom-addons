# -*- coding: utf-8 -*-
# Copyright © 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, api


class MailMail(models.Model):
    _inherit = 'mail.mail'

    @api.model
    def _postprocess_sent_message(self, mail, mail_sent=True):
        if mail_sent:
            mail._delete_partner_from_first_email()
        return super(MailMail, self)._postprocess_sent_message(
            mail, mail_sent=mail_sent)

    @api.multi
    def _delete_partner_from_first_email(self):
        for mail in self:
            partners = mail.recipient_ids.filtered(
                lambda x: x.delete_after_sending_email)
            if partners:
                partners.unlink()
