# Copyright 2026 Inael
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    fichar = fields.Selection(
        selection=[
            ("no", "No Ficha"),
            ("oficina", "Oficina/Almacen"),
            ("fabrica", "Fabrica"),
        ],
        string="Fichar en",
        default="fabrica",
    )

    entrada_ultima = fields.Datetime("Ultima Entrada")
    salida_ultima = fields.Datetime("Ultima Salida")
    proximo_movi = fields.Selection(
        selection=[("Entrada", "Entrada"), ("Salida", "Salida")],
        string="Tienes que hacer",
        default="Entrada",
    )
    # Definicion real: compute="_compute_presencia" (ver metodo comentado
    # mas abajo).

    tipo = fields.Selection(
        selection=[
            ("of", "En Fabricacion"),
            ("repara", "En Reparacion"),
            ("laser", "En Laser"),
            ("impro", "En Improductivo"),
            ("no", "No tienes Orden"),
        ],
        string="Orden Actual",
        default="no",
    )
    workorder_id = fields.Many2one(
        comodel_name="mrp.workorder", string="Orden de Trabajo"
    )
    production_id = fields.Many2one(
        comodel_name="mrp.production", string="OF", related="workorder_id.production_id"
    )
    repara_id = fields.Many2one(comodel_name="repair.order", string="Reparacion")
    laser_id = fields.Many2one(comodel_name="order.olaser", string="Laser")
    improductivo = fields.Many2one(comodel_name="mrp.workcenter.productivity.loss")
    puesto_id = fields.Many2one(comodel_name="hr.puesto.fichar")

    ot_qty_aproducir = fields.Float(
        "Cant. a producir", digits=(9, 2), related="workorder_id.qty_production"
    )
    ot_qty_comunicada = fields.Float("Cant. Comunicada", digits=(9, 2))
    # Definicion real: compute="_compute_ot_qty_comunicada" (ver metodo
    # comentado mas abajo).
    ot_qty_producida = fields.Float(
        "Cant. Producida", digits=(9, 2), related="workorder_id.qty_produced"
    )
    ot_product_id = fields.Many2one(
        comodel_name="product.product", related="workorder_id.product_id"
    )

    la_qty_aproducir = fields.Float(
        "Cant. a producir", digits=(9, 2), related="laser_id.cantidad"
    )
    la_qty_comunicada = fields.Float(
        "Cant. Comunicada", digits=(9, 2), related="laser_id.comunicado"
    )
    la_qty_producida = fields.Float(
        "Cant. Producida", digits=(9, 2), related="laser_id.terminado"
    )
    la_product_id = fields.Many2one(
        comodel_name="product.product", related="laser_id.product_id"
    )

    editar_orden = fields.Boolean("Editar orden", default=False)
    # Definicion real: compute="_compute_grupos" (ver metodo comentado mas
    # abajo).

    line_ids = fields.One2many(
        comodel_name="hr.fichar.historico",
        inverse_name="employee_id",
        string="Lineas Fichar",
        copy=False,
    )

    falta_material = fields.Boolean(
        related="workorder_id.falta_material",
    )

    # --- Logica operativa comentada: solo referencia, no se ejecuta. ---

    # @api.depends()
    # def _compute_presencia(self):
    #     for r in self:
    #         attendance = self.env["hr.attendance"].search(
    #             [
    #                 ("employee_id", "=", r.id),
    #                 ("check_out", "=", False),
    #             ],
    #             limit=1,
    #         )
    #         r.proximo_movi = "Salida" if attendance else "Entrada"

    # def _compute_grupos(self):
    #     for r in self:
    #         r.editar_orden = self.env.user.has_group(
    #             "ina_mc_permisos.group_inael_fabrica_respon_fichar"
    #         )

    # @api.depends("workorder_id.aceptada", "workorder_id.rechazada")
    # def _compute_ot_qty_comunicada(self):
    #     for r in self:
    #         r.ot_qty_comunicada = r.workorder_id.aceptada + r.workorder_id.rechazada

    # def _get_ahora(self):
    #     ff = datetime.utcnow().replace(microsecond=0)
    #     tz = pytz.timezone("Europe/Madrid")
    #     ff_local = pytz.utc.localize(ff).astimezone(tz)
    #     ahora = ff
    #     if ff_local.minute >= 30 and ff_local.hour in (5, 13):
    #         ahora = ff.replace(minute=0, second=0) + timedelta(hours=1)
    #     return ahora

    # def _get_attendance_abierta(self, employee_id):
    #     return self.env["hr.attendance"].search(
    #         [
    #             ("employee_id", "=", employee_id),
    #             ("check_out", "=", False),
    #         ],
    #         order="check_in DESC",
    #         limit=1,
    #     )

    def action_entrada_salida(self):
        return True
        # self.ensure_one()
        # ff = datetime.utcnow().replace(microsecond=0)
        #
        # w_usuario = self.env.user.id
        # w_puesto = w_centro = False
        # puesto = self.env["hr.puesto.fichar"].search(
        #     [("user_id", "=", w_usuario)], limit=1
        # )
        # if puesto:
        #     w_puesto = puesto.id
        #     w_centro = puesto.centro_id.id
        #
        # attendance = self._get_attendance_abierta(self.id)
        #
        # if attendance:
        #     attendance.write({"check_out": ff})
        #     self.write({"salida_ultima": ff, "puesto_id": w_puesto})
        #     w_estado = "interrumpir"
        # else:
        #     self.env["hr.attendance"].create(
        #         {"employee_id": self.id, "check_in": ff}
        #     )
        #     self.write({"entrada_ultima": ff, "puesto_id": w_puesto})
        #     w_estado = "abrir"
        #
        # if self.workorder_id:
        #     if w_estado == "interrumpir":
        #         self.comuni_fab(self, 0, 0, False, True, "interrumpida")
        #     else:
        #         self.comuni_fab(self, 0, 0, False, True, "abrir")
        # elif self.repara_id:
        #     if w_estado == "interrumpir":
        #         self.comuni_rep(self, 0, False, True, "interrumpida")
        #     else:
        #         self.comuni_rep(self, 0, False, True, "abrir")
        # elif self.laser_id:
        #     if w_estado == "interrumpir":
        #         self.comuni_las(self, 0, False, True, "interrumpida")
        #     else:
        #         self.comuni_las(self, 0, False, True, "abrir")
        # elif self.improductivo:
        #     if w_estado == "interrumpir":
        #         self.comuni_imp(self, 0, False, True, "interrumpida")
        #     else:
        #         self.comuni_imp(self, 0, False, True, "abrir")
        #
        # if w_estado == "abrir" and self.tipo == "no" and self.fichar == "fabrica":
        #     return {
        #         "name": "Fichar Orden",
        #         "type": "ir.actions.act_window",
        #         "res_model": "wiz.fichar.orden",
        #         "view_mode": "form",
        #         "target": "new",
        #         "context": dict(
        #             self.env.context,
        #             active_ids=self.ids,
        #             active_model="hr.employee",
        #         ),
        #     }
        # return True

    def action_ver_a_consumir(self):
        return True
        # self.ensure_one()
        # return {
        #     "name": "Material a Consumir",
        #     "type": "ir.actions.act_window",
        #     "res_model": "stock.move",
        #     "view_mode": "list",
        #     "view_id": self.env.ref(
        #         "ina_mp_production_fichar.ina_stock_move_fichar_view"
        #     ).id,
        #     "target": "current",
        #     "domain": [("workorder_id", "=", self.workorder_id.id)],
        # }

    def action_parada(self):
        return True
        # self.ensure_one()
        # for r in self:
        #     if r.workorder_id:
        #         self.comuni_fab(r, 0, 0, False, True, "procesada")
        #     elif r.repara_id:
        #         self.comuni_rep(r, 0, False, True, "cerrada")
        #     elif r.laser_id:
        #         self.comuni_las(r, 0, False, True, "cerrada")
        #     elif r.improductivo:
        #         self.comuni_imp(r, 0, False, True, "cerrada")
        # return self.action_fichar_nueva()

    def action_completada(self):
        return True
        # for r in self:
        #     if r.workorder_id:
        #         r.workorder_id.write({"falta_material": False})
        # return True

    def action_fichar_nueva(self):
        return True
        # self.ensure_one()
        # return {
        #     "name": "Fichar Orden",
        #     "type": "ir.actions.act_window",
        #     "res_model": "wiz.fichar.orden",
        #     "view_mode": "form",
        #     "target": "new",
        #     "context": dict(
        #         self.env.context,
        #         active_ids=self.ids,
        #         active_model="hr.employee",
        #     ),
        # }

    def button_scrap(self):
        return True
        # self.ensure_one()
        # production = self.workorder_id.production_id
        # product_ids = (
        #     production.move_raw_ids.filtered(
        #         lambda x: x.state not in ("done", "cancel")
        #     )
        #     | production.move_finished_ids.filtered(lambda x: x.state == "done")
        # ).mapped("product_id").ids
        # return {
        #     "name": _("Scrap"),
        #     "view_mode": "form",
        #     "res_model": "stock.scrap",
        #     "view_id": self.env.ref("stock.stock_scrap_form_view2").id,
        #     "type": "ir.actions.act_window",
        #     "context": {
        #         "default_workorder_id": self.workorder_id.id,
        #         "default_puesto_id": self.puesto_id.id,
        #         "default_production_id": production.id,
        #         "product_ids": product_ids,
        #     },
        #     "target": "new",
        # }

    # def _get_loss_productive(self):
    #     return self.env["mrp.workcenter.productivity.loss"].search(
    #         [("loss_type", "=", "productive")], limit=1
    #     )

    # def grabar_fab(self, r, ahora):
    #     self.env["mrp.workcenter.productivity"].create(
    #         {
    #             "loss_id": self._get_loss_productive().id,
    #             "workcenter_id": r.workorder_id.workcenter_id.id,
    #             "workorder_id": r.workorder_id.id,
    #             "employee_id": r.id,
    #             "date_start": ahora,
    #             "aceptada": 0,
    #             "estado": "activa",
    #         }
    #     )
    #     self.env["hr.fichar.historico"].create(
    #         {
    #             "employee_id": r.id,
    #             "tipo": "of",
    #             "orden": r.workorder_id.name,
    #             "workorder_id": r.workorder_id.id,
    #             "fecha_ini": ahora,
    #             "aceptada": 0,
    #             "rechazada": 0,
    #             "puesto_id": r.puesto_id.id,
    #             "estado": "activa",
    #         }
    #     )

    # def grabar_rep(self, r, ahora):
    #     self.env["mrp.repair.tiempos"].create(
    #         {
    #             "repara_id": r.repara_id.id,
    #             "workcenter_id": r.puesto_id.centro_id.id,
    #             "employee_id": r.id,
    #             "entrada": ahora,
    #             "estado": "activa",
    #         }
    #     )
    #     self.env["hr.fichar.historico"].create(
    #         {
    #             "employee_id": r.id,
    #             "tipo": "repara",
    #             "orden": r.repara_id.name,
    #             "fecha_ini": ahora,
    #             "puesto_id": r.puesto_id.id,
    #             "estado": "activa",
    #         }
    #     )

    # def grabar_las(self, r, ahora):
    #     self.env["order.olaser.tiempos"].create(
    #         {
    #             "laser_tiempos_id": r.laser_id.id,
    #             "employee_id": r.id,
    #             "entrada": ahora,
    #             "estado": "activa",
    #         }
    #     )
    #     self.env["hr.fichar.historico"].create(
    #         {
    #             "employee_id": r.id,
    #             "tipo": "laser",
    #             "orden": r.laser_id.name,
    #             "fecha_ini": ahora,
    #             "puesto_id": r.puesto_id.id,
    #             "estado": "activa",
    #         }
    #     )

    # def grabar_imp(self, r, ahora):
    #     self.env["mrp.improductivo"].create(
    #         {
    #             "loss_id": r.improductivo.id,
    #             "workcenter_id": r.puesto_id.centro_id.id,
    #             "employee_id": r.id,
    #             "entrada": ahora,
    #             "estado": "activa",
    #         }
    #     )
    #     self.env["hr.fichar.historico"].create(
    #         {
    #             "employee_id": r.id,
    #             "tipo": "impro",
    #             "orden": r.improductivo.name,
    #             "fecha_ini": ahora,
    #             "puesto_id": r.puesto_id.id,
    #             "estado": "activa",
    #         }
    #     )

    # def comuni_fab(
    #     self, r_fichar, w_canti, w_rechazada, w_refer_faltan, solo_parar, w_estado
    # ):
    #     ahora = self._get_ahora()
    #     ref_ids = self.env["mrp.workcenter.productivity"].search(
    #         [
    #             ("workorder_id", "=", r_fichar.workorder_id.id),
    #             ("estado", "in", ("activa", "interrumpida")),
    #             ("employee_id", "=", r_fichar.id),
    #         ],
    #         limit=5,
    #         order="date_start DESC",
    #     )
    #     if not ref_ids:
    #         raise exceptions.UserError(
    #             _("No se ha encontrado ningun fichaje en tiempos.")
    #         )
    #     sw = 0
    #     for r in ref_ids:
    #         if w_estado == "abrir":
    #             r.write({"estado": "procesada"})
    #             if r.workorder_id.state in ("done", "cancel"):
    #                 r_fichar.write({"workorder_id": False, "tipo": "no"})
    #                 return True
    #             self.grabar_fab(r_fichar, ahora)
    #             return True
    #
    #         ahora = self._get_ahora()
    #         sw += 1
    #         if ahora < r.date_start:
    #             ahora = r.date_start
    #         r.write(
    #             {
    #                 "date_end": ahora,
    #                 "aceptada": w_canti,
    #                 "rechazada": w_rechazada,
    #                 "estado": w_estado,
    #                 "falta_material": bool(w_refer_faltan),
    #             }
    #         )
    #         if r.duration > 540:
    #             r.date_end = r.date_start
    #
    #         w_acep = r.workorder_id.aceptada + w_canti
    #         w_recha = r.workorder_id.rechazada + w_rechazada
    #         w_refer2 = (r.workorder_id.refer_falta_material or "") + (
    #             (w_refer_faltan.strip() + " ") if w_refer_faltan else ""
    #         )
    #         r.workorder_id.write(
    #             {
    #                 "state": "progress",
    #                 "falta_material": bool(w_refer2),
    #                 "refer_falta_material": w_refer2,
    #                 "aceptada": w_acep,
    #                 "rechazada": w_recha,
    #             }
    #         )
    #         historico = self.env["hr.fichar.historico"].search(
    #             [
    #                 ("employee_id", "=", r_fichar.id),
    #                 ("tipo", "=", "of"),
    #                 ("fecha_fin", "=", False),
    #             ],
    #             limit=1,
    #             order="id DESC",
    #         )
    #         vals_hist = {
    #             "fecha_fin": ahora,
    #             "aceptada": w_canti,
    #             "rechazada": w_rechazada,
    #             "estado": w_estado,
    #             "workorder_id": r_fichar.workorder_id.id,
    #         }
    #         if historico:
    #             historico.write(vals_hist)
    #         else:
    #             vals_hist.update({
    #                 "employee_id": r_fichar.id,
    #                 "tipo": "of",
    #                 "orden": r_fichar.workorder_id.name,
    #                 "puesto_id": r_fichar.puesto_id.id,
    #             })
    #             self.env["hr.fichar.historico"].create(vals_hist)
    #         if w_estado == "interrumpida":
    #             return True
    #         if solo_parar:
    #             r_fichar.write({"tipo": "no", "workorder_id": False})
    #         elif sw == 1:
    #             self.grabar_fab(r_fichar, ahora)
    #     return True

    # def comuni_las(self, r_fichar, w_canti, w_refer_faltan, solo_parar, w_estado):
    #     ahora = self._get_ahora()
    #     ref_ids = self.env["order.olaser.tiempos"].search(
    #         [
    #             ("laser_tiempos_id", "=", r_fichar.laser_id.id),
    #             ("estado", "in", ("activa", "interrumpida")),
    #             ("employee_id", "=", r_fichar.id),
    #         ],
    #         limit=5,
    #         order="entrada DESC",
    #     )
    #     if not ref_ids:
    #         raise exceptions.UserError(
    #             _("No se ha encontrado ningun fichaje en tiempos.")
    #         )
    #     sw = 0
    #     for r in ref_ids:
    #         if w_estado == "abrir":
    #             r.write({"estado": "cerrada"})
    #             self.grabar_las(r_fichar, ahora)
    #             return True
    #
    #         ahora = self._get_ahora()
    #         sw += 1
    #         r.write({"salida": ahora, "comunicado": w_canti, "estado": w_estado})
    #         if r.tiempo > 9:
    #             r.salida = r.entrada
    #         r.laser_tiempos_id.write(
    #             {
    #                 "comunicado": r.laser_tiempos_id.comunicado + w_canti,
    #                 "state": "proceso",
    #             }
    #         )
    #         historico = self.env["hr.fichar.historico"].search(
    #             [
    #                 ("employee_id", "=", r_fichar.id),
    #                 ("tipo", "=", "laser"),
    #                 ("fecha_fin", "=", False),
    #             ],
    #             limit=1,
    #             order="id DESC",
    #         )
    #         vals_hist = {"fecha_fin": ahora, "aceptada": w_canti, "estado": w_estado}
    #         if historico:
    #             historico.write(vals_hist)
    #         else:
    #             vals_hist.update({
    #                 "employee_id": r_fichar.id,
    #                 "tipo": "laser",
    #                 "orden": r_fichar.laser_id.name,
    #                 "puesto_id": r_fichar.puesto_id.id,
    #             })
    #             self.env["hr.fichar.historico"].create(vals_hist)
    #         if w_estado == "interrumpida":
    #             return True
    #         if solo_parar:
    #             r_fichar.write({"tipo": "no", "laser_id": False})
    #         elif sw == 1:
    #             self.grabar_las(r_fichar, ahora)
    #     return True

    # def comuni_rep(self, r_fichar, w_canti, w_refer_faltan, solo_parar, w_estado):
    #     ahora = self._get_ahora()
    #     ref_ids = self.env["mrp.repair.tiempos"].search(
    #         [
    #             ("repara_id", "=", r_fichar.repara_id.id),
    #             ("estado", "in", ("activa", "interrumpida")),
    #             ("employee_id", "=", r_fichar.id),
    #         ],
    #         limit=5,
    #         order="entrada DESC",
    #     )
    #     if not ref_ids:
    #         raise exceptions.UserError(
    #             _("No se ha encontrado ningun fichaje en tiempos.")
    #         )
    #     sw = 0
    #     for r in ref_ids:
    #         if w_estado == "abrir":
    #             r.write({"estado": "cerrada"})
    #             self.grabar_rep(r_fichar, ahora)
    #             return True
    #
    #         ahora = self._get_ahora()
    #         sw += 1
    #         r.write({"salida": ahora, "estado": w_estado})
    #         if r.tiempo > 9:
    #             r.salida = r.entrada
    #         historico = self.env["hr.fichar.historico"].search(
    #             [
    #                 ("employee_id", "=", r_fichar.id),
    #                 ("tipo", "=", "repara"),
    #                 ("fecha_fin", "=", False),
    #             ],
    #             limit=1,
    #             order="id DESC",
    #         )
    #         vals_hist = {"fecha_fin": ahora, "estado": w_estado}
    #         if historico:
    #             historico.write(vals_hist)
    #         else:
    #             vals_hist.update({
    #                 "employee_id": r_fichar.id,
    #                 "tipo": "repara",
    #                 "orden": r_fichar.repara_id.name,
    #                 "puesto_id": r_fichar.puesto_id.id,
    #             })
    #             self.env["hr.fichar.historico"].create(vals_hist)
    #         if w_estado == "interrumpida":
    #             return True
    #         if solo_parar:
    #             r_fichar.write({"tipo": "no", "repara_id": False})
    #         elif sw == 1:
    #             self.grabar_rep(r_fichar, ahora)
    #     return True

    # def comuni_imp(self, r_fichar, w_canti, w_refer_faltan, solo_parar, w_estado):
    #     ahora = self._get_ahora()
    #     ref_ids = self.env["mrp.improductivo"].search(
    #         [
    #             ("estado", "in", ("activa", "interrumpida")),
    #             ("employee_id", "=", r_fichar.id),
    #         ],
    #         limit=5,
    #         order="entrada DESC",
    #     )
    #     if not ref_ids:
    #         raise exceptions.UserError(
    #             _("No se ha encontrado ningun fichaje en improductivo.")
    #         )
    #     sw = 0
    #     for r in ref_ids:
    #         if w_estado == "abrir":
    #             r.write({"estado": "cerrada"})
    #             self.grabar_imp(r_fichar, ahora)
    #             return True
    #
    #         ahora = self._get_ahora()
    #         sw += 1
    #         r.write({"salida": ahora, "estado": w_estado})
    #         if r.tiempo > 9:
    #             r.salida = r.entrada
    #         historico = self.env["hr.fichar.historico"].search(
    #             [
    #                 ("employee_id", "=", r_fichar.id),
    #                 ("tipo", "=", "impro"),
    #                 ("fecha_fin", "=", False),
    #             ],
    #             limit=1,
    #             order="id DESC",
    #         )
    #         vals_hist = {"fecha_fin": ahora, "estado": w_estado}
    #         if historico:
    #             historico.write(vals_hist)
    #         else:
    #             vals_hist.update({
    #                 "employee_id": r_fichar.id,
    #                 "tipo": "impro",
    #                 "orden": r_fichar.improductivo.name,
    #                 "puesto_id": r_fichar.puesto_id.id,
    #             })
    #             self.env["hr.fichar.historico"].create(vals_hist)
    #         if w_estado == "interrumpida":
    #             return True
    #         if solo_parar:
    #             r_fichar.write({"tipo": "no", "improductivo": False})
    #         elif sw == 1:
    #             self.grabar_imp(r_fichar, ahora)
    #     return True


class HrFicharHistorico(models.Model):
    _name = "hr.fichar.historico"
    _description = "Historico de fichajes"
    _order = "id DESC"

    employee_id = fields.Many2one(
        comodel_name="hr.employee",
        string="Empleado",
        ondelete="cascade",
    )
    tipo = fields.Selection(
        selection=[
            ("of", "Fabricacion"),
            ("repara", "Reparacion"),
            ("laser", "Laser"),
            ("impro", "Improductivo"),
            ("no", ""),
        ],
        string="Fichado en",
        default="no",
    )
    orden = fields.Char()
    workorder_id = fields.Many2one(
        comodel_name="mrp.workorder",
        string="Orden de Trabajo",
        ondelete="set null",
    )
    fecha_ini = fields.Datetime("Inicio")
    fecha_fin = fields.Datetime("Final")
    aceptada = fields.Float("Cantidad Aceptada")
    rechazada = fields.Float("Cantidad Rechazada")
    puesto_id = fields.Many2one(comodel_name="hr.puesto.fichar")
    estado = fields.Char()

    # --- Logica operativa comentada: solo referencia, no se ejecuta. Al
    # borrar una linea ya no se resta automaticamente de la OT lo que esa
    # linea hubiera sumado. ---

    # def unlink(self):
    #     for r in self:
    #         if r.tipo == "of" and r.workorder_id and (r.aceptada or r.rechazada):
    #             r.workorder_id.write(
    #                 {
    #                     "aceptada": max(r.workorder_id.aceptada - r.aceptada, 0),
    #                     "rechazada": max(r.workorder_id.rechazada - r.rechazada, 0),
    #                 }
    #             )
    #     return super().unlink()
