/** @odoo-module **/

import AbstractAwaitablePopup from 'point_of_sale.AbstractAwaitablePopup';
import Registries from 'point_of_sale.Registries';
import { useRef, useState } from "@odoo/owl";
import { _lt } from 'web.core';

const ajax = require('web.ajax');

class ValidarPagoMovilForm extends AbstractAwaitablePopup {
    setup() {
        super.setup();
        this.referencia = useRef('referenciaInput');
        this.tipNum = useRef('tipNumSelect')
        this.telefono = useRef('telefonoInput');
        this.banco = useRef('bancoSelect');
        this.fecha = useRef('fecha');
        this.fechaActual = useState({value: (new Date(Date.now() - 4 * 60 * 60 * 1000)).toISOString().split('T')[0]})
        this.isDisabled = useState({value: false});
    }

    async confirm() {
        this.isDisabled.value = true;
        this.fechaActual.value = this.fecha.el.value
        if (this.referencia.el.value != "" && this.telefono.el.value != "" && this.banco.el.value != "" && this.fecha.el.value != "") {
            let username = this.env.pos.config.username_sitef;
            let password = this.env.pos.config.encrypted_password;
            let url = this.env.pos.config.url_sitef;
            let idbranch = this.env.pos.config.idbranch_sitef;        
            let codestall = this.env.pos.config.codestall_sitef;
            let receivingbank = parseInt(this.env.pos.config.issuingbank_pm_sitef, 10);
    
            let paymentreference = this.referencia.el.value;
            let telefono = this.tipNum.el.value + this.telefono.el.value;
            let origenbank = parseInt(this.banco.el.value, 10);
            let amount = this.props.amount;
            let debitphone = '58' + telefono.substring(1);
            let trxdate = this.fecha.el.value;

            const token = await this.generarToken(url, username, password);
            if (token) {
                const pago = await this.validarPago(url, username, token, idbranch, codestall, amount, paymentreference, debitphone, origenbank, receivingbank, trxdate);
            }
        } else {
            this.showPopup('ErrorPopup', {
                title: this.env._t('Campos vacíos'),
                body: this.env._t('Debe ingresar TODOS los campos')
            });
        }
        this.isDisabled.value = false;
    }

    async generarToken(url, username, password) {
        const result = await ajax.jsonRpc(
            "/sitef_pos_integration/get_token", "call",
            { url, username, password }
        );
        if (result.error) {
            this.showPopup('ErrorPopup', {
                title: this.env._t(result.title_error),
                body: this.env._t(result.error),
            });
        } else{
            return result;
        }
    }
    
    async validarPago(url, username, token, idbranch, codestall, amount, paymentreference, debitphone, origenbank, receivingbank, trxdate) {
        try {
            const result = await ajax.jsonRpc(
                "/sitef_pos_integration/validarPago_sitef", "call",
                { url, username, token, idbranch, codestall, amount, paymentreference, debitphone, origenbank, receivingbank, trxdate }
            );
            if (result == "marcada") {
                this.showPopup('ConfirmPopup', {
                    title: this.env._t('Validación de pago móvil'),
                    body: this.env._t('El pago móvil fue validado con éxito')
                });
                this.env.posbus.trigger('close-popup', {
                    popupId: this.props.id,
                    response: { confirmed: true, payload: await this.getPayload() },
                });    
                return result;
            } 
            else if (result == "verified") {
                this.showPopup('ErrorPopup', {
                    title: this.env._t('Validación de pago móvil'),
                    body: this.env._t('El pago móvil ya fue validado anteriormente'),
                });
                return result;
            } 
            else if (result.error) {
                this.showPopup('ErrorPopup', {
                    title: this.env._t(result.title_error),
                    body: this.env._t(result.error),
                });
                return null;
            } else {
                this.showPopup('ErrorPopup', {
                    title: this.env._t(result.error_code),
                    body: this.env._t(result.description),
                });
                return null;
            }
        } catch (error) {
            this.showPopup('ErrorPopup', {
                title: this.env._t('Error de validación'),
                body: this.env._t(error),
            });
            return null;
        }
    }
    mostrarBanco() {
        const bancos = {
            102: '(0102) Banco de Venezuela',
            104: '(0104) Banco Venezolano de Crédito',
            105: '(0105) Banco Mercantil',
            108: '(0108) Banco Provincial',
            114: '(0114) Banco del Caribe',
            115: '(0115) Banco Exterior',
            128: '(0128) Banco Caroní',
            134: '(0134) Banesco',
            137: '(0137) Banco Sofitasa',
            138: '(0138) Banco Plaza',
            146: '(0146) Banco de la Gente Emprendedora',
            151: '(0151) Banco Fondo Común',
            156: '(0156) 100% Banco',
            157: '(0157) DelSur',
            163: '(0163) Banco del Tesoro',
            166: '(0166) Banco Agrícola de Venezuela',
            168: '(0168) Bancrecer',
            169: '(0169) Mi Banco',
            171: '(0171) Banco Activo',
            172: '(0172) Bancamiga',
            173: '(0173) Banco Internacional de Desarrollo',
            174: '(0174) Banplus',
            175: '(0175) Banco Bicentenario del Pueblo',
            177: '(0177) BANFANB',
            191: '(0191) Banco Nacional de Crédito',
        };
        return bancos[this.env.pos.config.issuingbank_pm_sitef]
    }
    mostrarDatos() {
        var $div = $('#datosPago');
        if ($div.is(':visible')) {
            $div.slideUp();
        } else {
            $div.slideDown();
        }
    }
}

ValidarPagoMovilForm.defaultProps = {
    cancelText: _lt('Cancel'),
    confirmText: _lt('Confirm'),
};

ValidarPagoMovilForm.template = 'ValidarPagoMovilForm';

Registries.Component.add(ValidarPagoMovilForm);
export default ValidarPagoMovilForm;