import base64
import logging
import os
import shutil
import subprocess

import xlsxwriter

from odoo import models
from odoo.http import request
from odoo.tools import config

_logger = logging.getLogger(__name__)


class ProductCatalogWeb(models.Model):
    _inherit = "product.catalog.web"

    def create_excel_file(self, file_name=None, sale_order=None):
        if not file_name:
            file_name = f"catalog_products_{self.name.replace(' ', '_')}.xlsx"
        filename = os.path.expanduser("~/") + file_name
        workbook = xlsxwriter.Workbook(filename)
        user_id = request.env.user if request else self.env.user

        pricelist = (
            sale_order.pricelist_id
            if sale_order
            else user_id.partner_id.property_product_pricelist
        )
        base_pricelists = pricelist.item_ids.mapped("base_pricelist_id")
        pricelist_product_ids = pricelist.product_ids.ids
        base_pricelist_product_ids = base_pricelists.mapped("product_ids").ids
        product_ids = self.product_ids.filtered(
            lambda p: p.is_published
            and (
                p.id in pricelist_product_ids
                or (base_pricelists and p.id in base_pricelist_product_ids)
            )
        ).sorted(key=lambda p: p.categ_id.name)

        table_header = workbook.add_format(
            {
                "bold": True,
                "border": 1,
                "align": "center",
                "valign": "vcenter",
                "fg_color": "#D7E4BC",
            }
        )
        table_header.set_text_wrap()
        table_detail_right_num = workbook.add_format(
            {
                "border": 1,
                "align": "right",
                "valign": "vcenter",
            }
        )
        table_detail_right_num.set_num_format("#,##0.00")
        worksheet = workbook.add_worksheet("Page1")

        worksheet.write(0, 0, "Internal Reference", table_header)
        worksheet.write(0, 1, "Barcode", table_header)
        worksheet.write(0, 2, "Name", table_header)
        worksheet.write(0, 3, "Sales Price", table_header)
        worksheet.write(0, 4, "RRP with Taxes", table_header)
        worksheet.write(0, 5, "Available Stock", table_header)
        worksheet.write(0, 6, "Category", table_header)

        # Productos
        n = 1
        for line in product_ids:
            for variant in line.product_variant_ids:
                comb_info = line.with_context(
                    pricelist=pricelist.id
                )._get_combination_info(product_id=variant.id)
                worksheet.write(n, 0, variant.default_code)
                worksheet.write(n, 1, variant.barcode)
                name = variant.display_name.split("] ")
                if len(name) > 1:
                    name = name[1]
                else:
                    name = variant.display_name
                worksheet.write(n, 2, name)
                price = (
                    comb_info["price"] if "price" in comb_info else variant.list_price
                )
                pvp_price = (
                    comb_info["pvp_price"]
                    if "pvp_price" in comb_info
                    else variant.list_price_tax
                )
                worksheet.write(n, 3, price)
                worksheet.write(n, 4, pvp_price)
                worksheet.write(
                    n,
                    5,
                    variant.with_context(
                        force_company=self.company_id.id
                    ).b2b_virtual_available,
                )
                worksheet.write(n, 6, variant.categ_id.name)

                n = n + 1
        workbook.close()

        act_id = self.add_file_in_attachment(filename)
        attachment_id = act_id.id
        return attachment_id, file_name

    def create_excel_file_extended(
        self, partner, catalog, file_name=None, sale_order=None
    ):
        datas_fname = f"catalog_{catalog.name.replace(' ', '_')}.xlsx"
        render_data = {
            "partner_id": partner.id,
            "catalog_id": catalog.id,
        }
        data = self.env["ir.actions.report"]._render(
            "website_portal_catalog.catalog_product_record_website_xlsx",
            catalog.ids,
            data=render_data,
        )[0]
        # save the attachment
        att_id = (
            self.env["ir.attachment"]
            .sudo()
            .create(
                {
                    "name": datas_fname,
                    "type": "binary",
                    "datas": base64.b64encode(data),
                    "res_model": "product.catalog.web",
                    "res_id": catalog.id,
                    #     'mimetype': 'application/x-pdf'
                }
            )
        )
        return att_id.id, datas_fname

    def add_file_in_attachment(self, file_name):
        byte_data = 0
        with open(file_name, "rb") as xlfile:
            byte_data = xlfile.read()
        attachment = self.env["ir.attachment"].create(
            {
                "name": file_name,
                "datas": base64.b64encode(byte_data),
                "res_model": "res.users",
                "res_id": 1,
            }
        )
        return attachment

    def _create_catalog_file_cron(self, partner_ids=None):
        partners = self.env["res.partner"].browse(partner_ids) if partner_ids else None
        for partner in partners:
            catalog = partner.send_catalog_id
            sale_order = (
                partner.sale_order_ids.sorted(
                    lambda s, catalog_id=catalog.id: s.catalog_id.id == catalog_id
                )
                if catalog
                else None
            )
            if sale_order and len(sale_order) > 1:
                sale_order = sale_order[0]
            partner_name = partner.name.replace(" ", "_").upper()
            file_name = f"catalog_products_{partner_name}.xlsx"
            attachment_id, file_name = catalog.with_context(
                force_company=catalog.company_id.id
            ).create_excel_file_extended(
                partner, catalog, file_name=file_name, sale_order=sale_order
            )
            catalog_attachment = self.env["ir.attachment"].browse(attachment_id)
            catalog_attachment.partner_id = partner.id
            self.move_file_to_dest_folder(catalog_attachment, file_name)

    def _get_ftp_config(self):
        keys = [
            "ftp_data_dir",
            "ftp_dest_user",
            "ftp_dest_dir",
            "ftp_dest_pass",
            "ftp_dest_server",
        ]
        values = {key: config.get(key) for key in keys}
        missing = [key for key, value in values.items() if not value]
        if missing:
            raise ValueError(
                "Missing Odoo config parameters for catalog FTP sync: "
                f"{', '.join(missing)}"
            )
        return values

    def move_file_to_dest_folder(self, attachment, file_name):
        ftp_config = self._get_ftp_config()
        ftp_data_dir = ftp_config["ftp_data_dir"]
        ftp_dest_user = ftp_config["ftp_dest_user"]
        ftp_dest_dir = ftp_config["ftp_dest_dir"]
        ftp_dest_pass = ftp_config["ftp_dest_pass"]
        ftp_dest_server = ftp_config["ftp_dest_server"]
        if ftp_data_dir:
            current_path = attachment._full_path(attachment.store_fname)
            shutil.copy(current_path, ftp_data_dir + "/" + file_name)
            # shutil.move(current_path, ftp_data_dir+"/"+file_name)
        # command_line = 'sh ' + ftp_sh_dir + '/ftp_reload_script.sh'
        args = [
            "sshpass",
            "-p",
            ftp_dest_pass,
            "rsync",
            "-a",
            ftp_data_dir,
            f"{ftp_dest_user}@{ftp_dest_server}:{ftp_dest_dir}",
        ]
        _logger.info(args)
        subprocess.Popen(args)  # Success!
        # stdout, stderr = process.communicate()
        # stdout = stdout.strip()
        # stderr = stderr.strip()
        # if stdout:
        #     _logger.info(stdout)
        # if stderr:
        #     _logger.info(stderr)

    def mirror_file_to_dest_ftpserver(self, attachment, file_name):
        ftp_config = self._get_ftp_config()
        ftp_data_dir = ftp_config["ftp_data_dir"]
        ftp_dest_user = ftp_config["ftp_dest_user"]
        ftp_dest_server = ftp_config["ftp_dest_server"]
        if ftp_data_dir:
            current_path = attachment._full_path(attachment.store_fname)
            shutil.move(current_path, ftp_data_dir + "/" + file_name)
        args = ["lftp", ftp_dest_server, "-u", ftp_dest_user]
        _logger.warning("Start FTP connection...")
        _logger.info(args)
        subprocess.Popen(args)  # Success!
