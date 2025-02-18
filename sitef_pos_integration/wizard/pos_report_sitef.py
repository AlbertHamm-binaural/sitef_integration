from odoo import api, fields, models
from odoo.exceptions import UserError
import json
from ..controllers.sitef_request import SitefController

class PosSitef(models.TransientModel):
    _name = 'pos.report.sitef'
    _description = 'Point of Sale Sitef Report'

    start_date = fields.Date(required=True, default=fields.Datetime.now, string='Fecha de inicio')
    end_date = fields.Date(required=True, default=fields.Datetime.now, string='Fecha de finalización')
    type_report = fields.Selection([
        ('totales', 'Aprobados'),
        ('detallado', 'Todos')
    ], string='Tipo de Reporte', default='totales')

    pos_config_id = fields.Many2one('pos.config', string='Punto de Venta', required=True, default=lambda s: s.env['pos.config'].search([]))

    @api.onchange('start_date')
    def _onchange_start_date(self):
        if self.start_date and self.end_date and self.end_date < self.start_date:
            self.end_date = self.start_date

    @api.onchange('end_date')
    def _onchange_end_date(self):
        if self.end_date and self.start_date and self.end_date < self.start_date:
            self.start_date = self.end_date

    def generate_report(self):
        url = self.pos_config_id.url_sitef
        username = self.pos_config_id.username_sitef
        password = self.pos_config_id.encrypted_password
        id_branch = self.pos_config_id.idbranch_sitef
        codestall = self.pos_config_id.codestall_sitef

        adquiriente = None
        trxdateini = str(self.start_date)
        trxdateend = str(self.end_date)
        typereport = self.type_report

        token = self._get_token(url, username, password)
        if token:
            data = self._get_data_report(url, username, token, id_branch, codestall, trxdateini, trxdateend, typereport, adquiriente)
            if data:
                return self.env.ref(
                    "sitef_pos_integration.action_pos_report_sitef"
                ).report_action(
                    self,
                    data={'data': data,
                            'start_date': self.start_date.strftime('%d-%m-%Y'),
                            'end_date': self.end_date.strftime('%d-%m-%Y'),},
                )
    
    def _get_token(self, url, username, password):
        
        response = SitefController.get_token(self, url, username, password)
        if response:
            if "error" in response:
                raise UserError("%s: %s" % (response["title_error"], response["error"]))
            else:
                return response
        else:
            raise UserError("No se recibió respuesta")

    def _get_data_report(self, url, username, token, id_branch, codestall, trxdateini, trxdateend, typereport, adquiriente):
        response = SitefController.reporteCaja_sitef(self, url, username, token, id_branch, codestall, trxdateini, trxdateend, typereport, adquiriente)
        if response:
            return response
        else:
            raise UserError("No se recibió respuesta")