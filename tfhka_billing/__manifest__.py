{
    "name": "Binaural TFHKA",
    "license": "LGPL-3",
    "author": "Binauraldev",
    "website": "https://binauraldev.com/",
    "category": "Accounting/Accounting",
    "version": "1.0",
    "depends": [
        "base",
        "account",
    ],
    
    "images": ["static/description/icon.png"],
    "application": True,
    "data": [
        "views/res_config_settings.xml",
        "views/view_move_form.xml",
    ],
    
    # "assets": {
    #     "account.assets": [
    #         "tfhka_billing/static/src/js/*.js",
    #         "tfhka_billing/static/src/xml/*.xml",
    #         "tfhka_billing/static/src/css/*.css",
    #     ],
    # },
    "binaural": True,
}