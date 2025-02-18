from odoo import fields, models

class ResCompany(models.Model):
    _inherit = "res.company"
    
    username_sitef = fields.Char()
    password_sitef = fields.Char()
    idbranch_sitef = fields.Integer()
    codestall_sitef = fields.Char()
    issuingbank_pm_sitef = fields.Selection([
        ("102", "(0102) Banco de Venezuela, S.A. Banco Universal"),
        ("104", "(0104) Banco Venezolano de Crédito, S.A. Banco Universal"),
        ("105", "(0105) Banco Mercantil C.A., Banco Universal"),
        ("108", "(0108) Banco Provincial, S.A. Banco Universal"),
        ("114", "(0114) Banco del Caribe C.A., Banco Universal"),
        ("115", "(0115) Banco Exterior C.A., Banco Universal"),
        ("128", "(0128) Banco Caroní C.A., Banco Universal"),
        ("134", "(0134) Banesco Banco Universal, C.A."),
        ("137", "(0137) Banco Sofitasa Banco Universal, C.A."),
        ("138", "(0138) Banco Plaza, Banco Universal"),
        ("146", "(0146) Banco de la Gente Emprendedora C.A."),
        ("151", "(0151) Banco Fondo Común, C.A Banco Universal"),
        ("156", "(0156) 100% Banco, Banco Comercial, C.A"),
        ("157", "(0157) DelSur, Banco Universal C.A."),
        ("163", "(0163) Banco del Tesoro C.A., Banco Universal"),
        ("166", "(0166) Banco Agrícola de Venezuela C.A., Banco Universal"),
        ("168", "(0168) Bancrecer S.A., Banco Microfinanciero"),
        ("169", "(0169) Mi Banco, Banco Microfinanciero, C.A."),
        ("171", "(0171) Banco Activo C.A., Banco Universal"),
        ("172", "(0172) Bancamiga Banco Universal, C.A."),
        ("173", "(0173) Banco Internacional de Desarrollo, C.A., Banco Universal"),
        ("174", "(0174) Banplus Banco Universal, C.A."),
        ("175", "(0175) Banco Bicentenario del Pueblo, Banco Universal C.A."),
        ("177", "(0177) Banco de la Fuerza Armada Nacional Bolivariana (BANFANB)"),
        ("191", "(0191) Banco Nacional de Crédito (BNC)")
    ])
    issuingbank_trf_sitef = fields.Selection([
        ("102", "(0102) Banco de Venezuela, S.A. Banco Universal"),
        ("104", "(0104) Banco Venezolano de Crédito, S.A. Banco Universal"),
        ("105", "(0105) Banco Mercantil C.A., Banco Universal"),
        ("108", "(0108) Banco Provincial, S.A. Banco Universal"),
        ("114", "(0114) Banco del Caribe C.A., Banco Universal"),
        ("115", "(0115) Banco Exterior C.A., Banco Universal"),
        ("128", "(0128) Banco Caroní C.A., Banco Universal"),
        ("134", "(0134) Banesco Banco Universal, C.A."),
        ("137", "(0137) Banco Sofitasa Banco Universal, C.A."),
        ("138", "(0138) Banco Plaza, Banco Universal"),
        ("146", "(0146) Banco de la Gente Emprendedora C.A."),
        ("151", "(0151) Banco Fondo Común, C.A Banco Universal"),
        ("156", "(0156) 100% Banco, Banco Comercial, C.A"),
        ("157", "(0157) DelSur, Banco Universal C.A."),
        ("163", "(0163) Banco del Tesoro C.A., Banco Universal"),
        ("166", "(0166) Banco Agrícola de Venezuela C.A., Banco Universal"),
        ("168", "(0168) Bancrecer S.A., Banco Microfinanciero"),
        ("169", "(0169) Mi Banco, Banco Microfinanciero, C.A."),
        ("171", "(0171) Banco Activo C.A., Banco Universal"),
        ("172", "(0172) Bancamiga Banco Universal, C.A."),
        ("173", "(0173) Banco Internacional de Desarrollo, C.A., Banco Universal"),
        ("174", "(0174) Banplus Banco Universal, C.A."),
        ("175", "(0175) Banco Bicentenario del Pueblo, Banco Universal C.A."),
        ("177", "(0177) Banco de la Fuerza Armada Nacional Bolivariana (BANFANB)"),
        ("191", "(0191) Banco Nacional de Crédito (BNC)")
    ])
    issuingid_pm_sitef = fields.Char()
    issuingid_trf_sitef = fields.Char()
    issuingmobilenumber_pm_sitef = fields.Char()
    issuingnumber_trf_sitef = fields.Char()
    url_sitef = fields.Char()
    
    activated_cpm_sitef = fields.Boolean()
    activated_pm_sitef = fields.Boolean()
    activated_trf_sitef = fields.Boolean()
    activated_zelle_sitef = fields.Boolean()