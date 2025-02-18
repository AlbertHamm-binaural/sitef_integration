/** @odoo-module **/

import AbstractAwaitablePopup from 'point_of_sale.AbstractAwaitablePopup';
import Registries from 'point_of_sale.Registries';
import { useRef, useState } from "@odoo/owl";
import { _lt } from 'web.core';

const ajax = require('web.ajax');

class ValidarZelleForm extends AbstractAwaitablePopup {
    setup() {
        super.setup();
        this.aut = useRef('inputAutorizacion');
        this.banco = useRef('bancoSelect');
        this.fecha = useRef('fecha');
        this.fechaActual = useState({value: (new Date(Date.now() - 4 * 60 * 60 * 1000)).toISOString().split('T')[0]})
        this.phone = useRef('phoneInput');
        this.seq = useRef('seqInput');
        this.state = useState({ amount: 0 });
        this.isDisabled = useState({value: false});

        this.initializeAmount();
    }

    async confirm() {
        this.isDisabled.value = true;
        this.fechaActual.value = this.fecha.el.value
        if (this.aut.el.value != "" && this.phone.el.value != "" && this.seq.el.value != "" && this.banco.el.value != "" && this.fecha.el.value != "") {
            let username = this.env.pos.config.username_sitef;
            let password = this.env.pos.config.encrypted_password;
            let url = this.env.pos.config.url_sitef;
            let idbranch = this.env.pos.config.idbranch_sitef;
            let codestall = this.env.pos.config.codestall_sitef;

            let authorizationcode = this.aut.el.value;
            let phonenumber = this.phone.el.value;
            let sequentialnumber = this.seq.el.value;

            let trxdate = this.fecha.el.value;

            let amount = this.state.amount;

            const token = await this.generarToken(url, username, password);
            if (token) {
                const cambio = await this.validarZelle(url, username, token, idbranch, codestall, amount, trxdate, authorizationcode, phonenumber, sequentialnumber);
            }
        } else {
            this.showPopup('ErrorPopup', {
                title: this.env._t('Campos vacíos'),
                body: this.env._t('Debe ingresar TODOS los campos')
            });
        }
        this.isDisabled.value = false;
    }

    async initializeAmount() {
        this.isDisabled.value = true;
        const bcv = await this.BCV();
        if (bcv) {
            this.state.amount = (this.props.amount / bcv).toFixed(2);
        } else {
            this.state.amount = NaN; 
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
        } else {
            return result;
        }
    }

    async validarZelle(url, username, token, idbranch, codestall, amount, trxdate, authorizationcode, phonenumber, sequentialnumber) {
        try {
            const result = await ajax.jsonRpc(
                "/sitef_pos_integration/validarZelle_sitef", "call",
                { url, username, token, idbranch, codestall, amount, trxdate, authorizationcode, phonenumber, sequentialnumber }
            );
            if (result == "marcada") {
                this.showPopup('ConfirmPopup', {
                    title: this.env._t('Validación de Zelle'),
                    body: this.env._t('La Zelle fue validada con éxito')
                });
                this.env.posbus.trigger('close-popup', {
                    popupId: this.props.id,
                    response: { confirmed: true, payload: await this.getPayload() },
                });
                return result;
            }
            if (result == "verified") {
                this.showPopup('ErrorPopup', {
                    title: this.env._t('Validación de Zelle'),
                    body: this.env._t('La Zelle ya fue validada anteriormente'),
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

    async BCV() {
        try {
            const result = await ajax.jsonRpc(
                "/sitef_pos_integration/obtener_precio_dolar", "call", {}
            );
            if (result) {
                return result;
            } else {
                console.log("No se pudo obtener el precio del dólar.");
            }
        } catch (error) {
            console.error("Error fetching BCV price:", error);
        }
    }
    
}

ValidarZelleForm.defaultProps = {
    cancelText: _lt('Cancel'),
    confirmText: _lt('Confirm'),
};

ValidarZelleForm.template = 'ValidarZelleForm';

Registries.Component.add(ValidarZelleForm);
export default ValidarZelleForm;