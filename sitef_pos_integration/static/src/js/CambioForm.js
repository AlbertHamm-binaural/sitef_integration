/** @odoo-module **/

import AbstractAwaitablePopup from 'point_of_sale.AbstractAwaitablePopup';
import Registries from 'point_of_sale.Registries';
import { useRef, useState } from "@odoo/owl";
import { _lt } from 'web.core';

const ajax = require('web.ajax');

class CambioForm extends AbstractAwaitablePopup {
    setup() {
        super.setup();
        this.tipDoc = useRef('tipDocSelect');
        this.doc = useRef('docInput');
        this.tipNum = useRef('tipNumSelect')
        this.telefono = useRef('telefonoInput');
        this.banco = useRef('bancoSelect');
        this.isDisabled = useState({value: false});
    }
    
    async confirm() {
        this.isDisabled.value = true;
        if (this.doc.el.value != "" && this.telefono.el.value != "" && this.banco.el.value != "") {
            let username = this.env.pos.config.username_sitef;
            let password = this.env.pos.config.encrypted_password;
            let url = this.env.pos.config.url_sitef;
            let idbranch = this.env.pos.config.idbranch_sitef;        
            let codestall = this.env.pos.config.codestall_sitef;
            let issuingbank = parseInt(this.env.pos.config.issuingbank_pm_sitef, 10);
            
            let invoicenumber = this.props.orden;
            let tipDoc = this.tipDoc.el.value;
            let doc = this.doc.el.value;
            let telefono = this.tipNum.el.value + this.telefono.el.value;
            
            let destinationbank = parseInt(this.banco.el.value, 10);
            let amount = this.props.amount;
            let destinationid = tipDoc + doc;

            let destinationmobilenumber = '58' + telefono.substring(1);
            const token = await this.generarToken(url, username, password);
            if (token) {
                const cambio = await this.generarCambio(url, username, token, idbranch, codestall, destinationid, destinationmobilenumber, destinationbank, issuingbank, invoicenumber, amount);
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
            return null
        } else{
            return result;
        }
    }
    
    async generarCambio(url, username, token, idbranch, codestall, destinationid, destinationmobilenumber, destinationbank, issuingbank, invoicenumber, amount) {
        try {    
            const result = await ajax.jsonRpc(
                "/sitef_pos_integration/cambio_sitef", "call",
                { url, username, token, idbranch, codestall, destinationid, destinationmobilenumber, destinationbank, issuingbank, invoicenumber, amount}
            );
            if (result.trx_status == "approved") {
                this.showPopup('ConfirmPopup', {
                    title: this.env._t('Pago Móvil realizado con éxito'),
                    body: this.env._t('Referencia: ') + result.payment_reference
                });
                this.env.posbus.trigger('close-popup', {
                    popupId: this.props.id,
                    response: { confirmed: true, payload: result.payment_reference},
                });    
                return result.payment_reference;
            } else if (result.error) {
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
}

CambioForm.defaultProps = {
    cancelText: _lt('Cancel'),
    confirmText: _lt('Confirm'),
};

CambioForm.template = 'CambioForm';

Registries.Component.add(CambioForm);
export default CambioForm;