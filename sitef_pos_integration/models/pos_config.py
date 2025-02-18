from odoo import models, fields, api
import hashlib
import logging

_logger = logging.getLogger(__name__)


class PosConfig(models.Model):
    _inherit = "pos.config"

    username_sitef = fields.Char(related="company_id.username_sitef", string="Username", readonly=False)
    password_sitef = fields.Char(related="company_id.password_sitef", string="Password", readonly=False)
    idbranch_sitef = fields.Integer(related="company_id.idbranch_sitef", string="Id Branch", readonly=False)
    codestall_sitef = fields.Char(related="company_id.codestall_sitef", string="Code Stall", readonly=False)
    issuingbank_pm_sitef = fields.Selection(related="company_id.issuingbank_pm_sitef", string="Banco Emisor (Pago Móvil)", readonly=False)
    issuingbank_trf_sitef = fields.Selection(related="company_id.issuingbank_trf_sitef", string="Banco Emisor (Transferencia Bancaria)", readonly=False)
    issuingid_pm_sitef = fields.Char(related="company_id.issuingid_pm_sitef", string="Identificación Emisor (Pago Móvil)", readonly=False)
    issuingid_trf_sitef = fields.Char(related="company_id.issuingid_trf_sitef", string="Identificación Emisor", readonly=False)
    issuingmobilenumber_pm_sitef = fields.Char(related="company_id.issuingmobilenumber_pm_sitef", string="Número Telefónico Emisor (Pago Móvil)", readonly=False)
    issuingnumber_trf_sitef = fields.Char(related="company_id.issuingnumber_trf_sitef", string="Número de cuenta Emisor (Transferencia Bancaria)", readonly=False)
    url_sitef = fields.Char(related="company_id.url_sitef", string="URL", readonly=False)
    encrypted_password = fields.Char(string="Encrypted Password", compute="_encrypted_password")
    
    activated_cpm_sitef = fields.Boolean(related="company_id.activated_cpm_sitef", string="Activar Cambio (Pago Móvil)", readonly=False)
    activated_pm_sitef = fields.Boolean(related="company_id.activated_pm_sitef", string="Activar Pago Móvil", readonly=False)
    activated_trf_sitef = fields.Boolean(related="company_id.activated_trf_sitef", string="Activar Transferencia", readonly=False)
    activated_zelle_sitef = fields.Boolean(related="company_id.activated_zelle_sitef", string="Activar Zelle", readonly=False)
    
    @api.depends('password_sitef')
    def _encrypted_password(self):
        for record in self:
            if record.password_sitef:
                record.encrypted_password = hashlib.md5(record.password_sitef.encode()).hexdigest()
            else:
                record.encrypted_password = ''
    
    