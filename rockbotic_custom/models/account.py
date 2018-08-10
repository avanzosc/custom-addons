# -*- coding: utf-8 -*-
# © 2016 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, models, fields, exceptions, _


class AccountTax(models.Model):
    _inherit = 'account.tax'

    tax_exempt = fields.Boolean(
        string='Tax exempt', default=False)


class AccountAnalyticAccont(models.Model):
    _inherit = 'account.analytic.account'

    recurring_first_day = fields.Boolean(default=True)
    recurring_last_day = fields.Boolean(default=False)

    @api.model
    def _prepare_invoice_data(self, contract):
        res = super(AccountAnalyticAccont,
                    self)._prepare_invoice_data(contract)
        if 'comment' in res and not res['comment']:
            del res['comment']
        return res

    @api.multi
    def name_get(self):
        if not self.env.context.get('only_name', False):
            return super(AccountAnalyticAccont, self).name_get()
        res = []
        for account in self:
            res.append((account.id, account.name))
        return res


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    literal_header_invoice = fields.Text(string='literal header invoice')

    def partners_for_send_automatic_pay_email(self):
        return self.partner_id.mapped(
            'other_child_ids').filtered(
            lambda l: l.send_email_unpaid_invoice).ids

    def send_by_email_customer_invoice(self):
        template = self.env.ref('account.email_template_edi_invoice', False)
        partners = self.partners_for_send_automatic_pay_email()
        if not partners:
            raise exceptions.Warning(
                _("Email not found, for partner: %s.") %
                self.partner_id.name)
        for partner in partners:
            mail = self.env['mail.compose.message'].with_context(
                default_composition_mode='mass_mail',
                default_template_id=template.id,
                default_use_template=True,
                default_partner_ids=[(6, 0, [partner])],
                active_id=self.id,
                active_ids=self.ids,
                active_model='account.invoice',
                default_model='account.invoice',
                default_res_id=self.id,
                force_send=True,
                mark_invoice_as_sent=True
            ).create({'subject': template.subject,
                      'body': template.body_html})
            mail.send_mail()
            self.sent = True
