odoo.define('sitef_pos_integration.payment_control', function (require) {

    const Registries = require('point_of_sale.Registries');
    const PaymentScreen = require("point_of_sale.PaymentScreen");
    const NumberBuffer = require('point_of_sale.NumberBuffer');

    var Session = require("web.Session");
        
    const ControlSitef = PaymentScreen => class extends PaymentScreen {
        constructor() {
            super(...arguments);

        }

        async cambio() {
            if (this.selectedPaymentLine && this.selectedPaymentLine.amount < 0) {
                if (this.selectedPaymentLine.transaction_id) {
                    this.showPopup('ErrorPopup', {
                        title: this.env._t('Operación Fallida'),
                        body: this.env._t('No se puede aplicar el cambio porque ya se realizó anteriormente en esta línea.'),
                    });
                    return;
                } else {
                    const { confirmed, payload: payment_reference } = await this.showPopup('CambioForm', {amount: Math.abs(this.selectedPaymentLine.amount), orden:this.currentOrder.uid});
                    if (confirmed) {
                        this.selectedPaymentLine.transaction_id = payment_reference;
                        // this.selectedPaymentLine.ticket = "Cambio";
                    } else {
                        console.log('No se obtuvo referencia de pago');
                    }
                }
            } else {
                this.showPopup('ErrorPopup', {
                    title: this.env._t('Error'),
                    body: this.env._t('No se puede realizar un cambio.'),
                });
            }
        }

        async validarPagoMovil() {
            if (this.selectedPaymentLine && this.selectedPaymentLine.amount > 0) {
                if (this.selectedPaymentLine.transaction_id) {
                    this.showPopup('ErrorPopup', {
                        title: this.env._t('Operación Fallida'),
                        body: this.env._t('No se puede aplicar el cambio porque ya se realizó anteriormente en esta línea.'),
                    });
                    return;
                } else {
                    const { confirmed, payload: payment_reference } = await this.showPopup('ValidarPagoMovilForm', {amount: parseFloat(Math.abs(this.selectedPaymentLine.amount).toFixed(2)), orden:this.currentOrder.uid});
                    if (confirmed) {
                        console.log(payment_reference)
                        this.selectedPaymentLine.transaction_id = payment_reference;
                        // this.selectedPaymentLine.ticket = "Cambio";
                    } else {
                        console.log('No se obtuvo referencia de pago');
                    }
                }
            }
            else {
                this.showPopup('ErrorPopup', {
                    title: this.env._t('Error'),
                    body: this.env._t('No se puede realizar un pago móvil.'),
                });
            }
        }
        async validarTransferencia() {
            if (this.selectedPaymentLine && this.selectedPaymentLine.amount > 0) {
                this.showPopup('ValidarTransferenciaForm', {amount: Math.abs(this.selectedPaymentLine.amount)});
            }
            else {
                this.showPopup('ErrorPopup', {
                    title: this.env._t('Error'),
                    body: this.env._t('No se puede realizar una transferencia.'),
                });
            }
        }   
        
        async validarZelle() {
            if (this.selectedPaymentLine && this.selectedPaymentLine.amount > 0) {
                this.showPopup('ValidarZelleForm', { amount: Math.abs(this.selectedPaymentLine.amount) });
            }
            else {
                this.showPopup('ErrorPopup', {
                    title: this.env._t('Error'),
                    body: this.env._t('No se puede realizar un Zelle.'),
                });
            }
        }    
        AmountCambio(amount) {
            const metodo_pago = this.selectedPaymentLine.name;
            if (amount < 0 && metodo_pago == 'Banco') {
                return false;
            } else {
                return true;
            }
        }
        AmountPago(amount) {
            const metodo_pago = this.selectedPaymentLine.name;
            if (amount > 0 && metodo_pago == 'Banco') {
                return false;
            } else{
                return true;
            }
        }
        deletePaymentLine(event) {
            var self = this;
            const { cid } = event.detail;
            const line = this.paymentLines.find((line) => line.cid === cid);
            
            if (line.transaction_id) {
                return;
            }
        
            if (['waiting', 'waitingCard', 'timeout'].includes(line.get_payment_status())) {
                line.set_payment_status('waitingCancel');
                line.payment_method.payment_terminal.send_payment_cancel(this.currentOrder, cid).then(function() {
                    self.currentOrder.remove_paymentline(line);
                    NumberBuffer.reset();
                    self.render(true);
                })
            }
            else if (line.get_payment_status() !== 'waitingCancel') {
                this.currentOrder.remove_paymentline(line);
                NumberBuffer.reset();
                this.render(true);
            }
        }
        _updateSelectedPaymentline() {
            const transaction_id = this.selectedPaymentLine?.transaction_id || null;
            if (transaction_id) return;
            
            if (this.paymentLines.every((line) => line.paid)) {
                this.currentOrder.add_paymentline(this.payment_methods_from_config[0]);
            }
            if (!this.selectedPaymentLine) return; // do nothing if no selected payment line
            // disable changing amount on paymentlines with running or done payments on a payment terminal
            const payment_terminal = this.selectedPaymentLine.payment_method.payment_terminal;
            if (
                payment_terminal &&
                !['pending', 'retry'].includes(this.selectedPaymentLine.get_payment_status())
            ) {
                return;
            }
            if (NumberBuffer.get() === null) {
                this.deletePaymentLine({ detail: { cid: this.selectedPaymentLine.cid } });
            } else {
                this.selectedPaymentLine.set_amount(NumberBuffer.getFloat());
            }
        }
    };

    Registries.Component.extend(PaymentScreen, ControlSitef);
    return ControlSitef;
});