from odoo import models, api, fields
from odoo.exceptions import UserError, ValidationError
import logging
import requests
from datetime import datetime
import base64
import os

_logger = logging.getLogger(__name__)

class AccountMove(models.Model):

    _inherit = 'account.move'
    
    fecha_token_tfhka = fields.Datetime()
    token_actual_tfhka = fields.Char()
    
    def Emision(self):   
        tipoDocumento = self.env.context.get('tipoDocumento')
        url,token = self.GenerarToken()
        hasta, inicio = self.ConsultaNumeracion(url, token)
        numeroDocumento = self.UltimoDocumento(url, token)

        if numeroDocumento is inicio:
            self.AsignarNumeracion(self, url, token, hasta, inicio)
        _logger.info(f"Se esta ejecturando emision")
        
        data = self.FacturaBasica(numeroDocumento, tipoDocumento)
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(url + "/Emision", json=data, headers=headers)
        respuesta_json = response.json()
        _logger.warning(respuesta_json)
        codigo = respuesta_json.get("codigo")
        mensaje = respuesta_json.get("mensaje")
        validaciones = respuesta_json.get("validaciones")
        if response.status_code is 200:
            if codigo == "200":
                _logger.info("Documento emitido correctamente")
                raise UserError("Documento emitido correctamente")
            else:
                _logger.error(f"Error al emitir documento: {mensaje}")
                raise UserError(f"Error al emitir documento: {mensaje}")
        else:
            _logger.error(f"Error {response.status_code}, {mensaje}")
            raise UserError(f"Error {response.status_code}: {validaciones}")

    def FacturaBasica(self, numeroDocumento, tipoDocumento):
        for record in self:
            cliente = record.partner_id
            hora = record.create_date.strftime("%I:%M:%S %p").lower()
            telefono = cliente.mobile or cliente.phone
            if cliente.vat != "":
                if "-" in cliente.vat:
                    if "." in cliente.vat:
                        partes = cliente.vat.split("-")
                        prefijo = partes[0]
                        numeros = "-".join(partes[1:]).replace(".", "").replace("-", "")
                    else:
                        partes = cliente.vat.split("-")
                        prefijo = partes[0]
                        numeros = "-".join(partes[1:]).replace("-", "")
                else:
                    prefijo = cliente.vat[0]
                    numeros = cliente.vat[1:]
            fecha_emision = record.invoice_date.strftime("%d/%m/%Y") if record.invoice_date else ""
            fecha_vencimiento = record.invoice_date_due.strftime("%d/%m/%Y") if record.invoice_date_due else ""
            
            identificacionDocumento = {
                "tipoDocumento": tipoDocumento,
                "numeroDocumento": str(numeroDocumento + 1),
                "SerieFacturaAfectada": str(record.name),
                "NumeroFacturaAfectada": str(record.id),
                "FechaFacturaAfectada": fecha_emision,
                "MontoFacturaAfectada": str(record.amount_total),
                "ComentarioFacturaAfectada": "prueba",
                "fechaEmision": fecha_emision,
                "fechaVencimiento": fecha_vencimiento,
                "horaEmision": hora,
                "tipoDePago": record.invoice_payment_term_id.name or "",
                "serie": "",
                "tipoDeVenta": "*Interna",
                "moneda": record.currency_id.name,
            }
            vendedor = {
                "codigo": str(record.invoice_user_id.vat or record.invoice_user_id.id),
                "nombre": record.invoice_user_id.name,
            }
            comprador = {
                "tipoIdentificacion": prefijo,
                "numeroIdentificacion": numeros,
                "razonSocial": cliente.name,
                "direccion": cliente.street or "no definida",
                "pais": cliente.country_code or "",
                "telefono": [telefono],
                "notificar": "Si",
                "correo": [cliente.email or ""],
            }
            totales = {
                "nroItems": str(len(record.invoice_line_ids)),
                "montoGravadoTotal": str(sum(line.price_subtotal for line in record.invoice_line_ids if line.tax_ids)),
                "montoExentoTotal": str(round(sum(line.price_subtotal for line in record.invoice_line_ids if not line.tax_ids) * 100) / 100),
                "subtotal": str(record.amount_untaxed),
                "totalAPagar": str(record.amount_total),
                "totalIVA": str(record.amount_tax), 
                "montoTotalConIVA": str(record.amount_total),
            }
            detallesItems = []
            contador = 1
            for line in record.invoice_line_ids:
                detallesItems.append({
                    "numeroLinea": str(contador),
                    "codigoPLU": line.product_id.barcode or line.product_id.default_code or "",
                    "indicadorBienoServicio": "2" if line.product_id.type == 'service' else "1",
                    "descripcion": line.product_id.name,
                    "cantidad": str(line.quantity),
                    "precioUnitario": str(line.price_unit),
                    "precioItem": str(line.price_subtotal),
                    "codigoImpuesto": "G",
                    "tasaIVA": str(line.tax_ids[0].amount) if line.tax_ids else "0",
                    "valorIVA": str(round(line.price_total - line.price_subtotal, 2)),
                    "valorTotalItem": str(line.price_total),
                })
                contador += 1

        data = {
            "documentoElectronico": {
                "encabezado": {
                    "identificacionDocumento": identificacionDocumento,
                    "vendedor": vendedor,
                    "comprador": comprador,
                    "totales": totales,
                },
                "detallesItems": detallesItems,
            }
        }
        return data
    
    def UltimoDocumento(self, url, token):
        _logger.info(f"Se esta ejecutando ultimodocumento")

        headers = {
            "Authorization": f"Bearer {token}"
        }
        
        response = requests.post(url + "/UltimoDocumento", json={
                "serie": "",
                "tipoDocumento": "01",
            }, headers=headers)
        response_json = response.json()
        _logger.warning(response_json)
        codigo = response_json.get("codigo")
        mensaje = response_json.get("mensaje")
        
        if response.status_code == 200:
            if codigo == "200":
                numeroDocumento = response_json["numeroDocumento"]
                return numeroDocumento
            else:
                _logger.error(f"Error {codigo}, {mensaje}")
                raise UserError(f"Error {codigo}: {mensaje}")
        else:
            _logger.error(f"Error {response.status_code}, {mensaje}")
            raise UserError(f"Error {response.status_code}: {mensaje}")

    def AsignarNumeracion(self, url, token, hasta, inicio):
        fin = inicio + 20
        inicio += 1
        
        _logger.info(f"Se esta ejecutando asignar numeracion")
        if inicio <= hasta:
            headers = {
                "Authorization": f"Bearer {token}"
            }
            response = requests.post(url + "/AsignarNumeraciones", json={
                "serie": "",
                "tipoDocumento": "01",
                "numeroDocumentoInicio": inicio,
                "numeroDocumentoFin": fin
            }, headers=headers)
            response_json = response.json()
            _logger.warning(response_json)
            codigo = response_json.get("codigo")
            mensaje = response_json.get("mensaje")
            
            if response.status_code == 200:
                if codigo == "200":
                    _logger.info("Rango de numeración asignado correctamente.")
                else:
                    _logger.warning(f"Error {codigo}, {mensaje}")
                    raise UserError(f"Error {codigo}: {mensaje}")
            else:
                _logger.error(f"Error: {response.status_code}, {mensaje}")
                raise UserError(f"Error: {response.status_code}: {mensaje}")
        else:
            _logger.error("El rango de numeración asignado ha sido superado.")
            raise UserError("El rango de numeración asignado ha sido superado.")

    def ConsultaNumeracion(self, url, token):
        _logger.info(f"Se esta ejecutando consulta numeracion")

        headers = {
            "Authorization": f"Bearer {token}"
        }
        
        response = requests.post(url + "/ConsultaNumeraciones", json={
                "serie": "",
                "tipoDocumento": "",
                "prefix": ""
            }, headers=headers)
        respuesta_json = response.json()
        _logger.warning(respuesta_json)
        codigo = respuesta_json.get("codigo")
        mensaje = respuesta_json.get("mensaje")
        
        if response.status_code == 200:
            if codigo == "200":
                numeracion = respuesta_json["numeraciones"][0]
                hasta = numeracion.get("hasta")
                inicio = numeracion.get("correlativo")
                return hasta, inicio
            else:
                _logger.error(f"Error {codigo}, {mensaje}")
                raise UserError(f"Error {codigo}: {mensaje}")
        else:
            _logger.error(f"Error: {response.status_code}, {mensaje}")
            raise UserError(f"Error: {response.status_code}: {mensaje}")

    # def DescargarArchivo(self):
    #     url, token = self.GenerarToken()
    
    #     headers = {
    #         "Authorization": f"Bearer {token}"
    #     }
    
    #     response = requests.post(url + "/DescargaArchivo", json={
    #             "token": token,
    #             "serie": "",
    #             "tipoDocumento": "01",
    #             "numeroDocumento": "1"
    #         }, headers=headers)
    
    #     if response.status_code == 200:
    #         _logger.info("Petición realizada correctamente")
    
    #         try:
    #             respuesta_json = response.json()
    
    #             if respuesta_json.get("codigo") == "200":
    #                 base64_string = respuesta_json.get("archivo")
    
    #                 if base64_string:
    #                     try:
    #                         # Decodificar el archivo
    #                         decoded_file = base64.b64decode(base64_string)
    
    #                         # Ruta explícita
    #                         current_directory = ""
    #                         file_path = os.path.join(current_directory, "archivo_descargado.pdf")
    
    #                         # Guardar el archivo
    #                         with open(file_path, "wb") as file:
    #                             file.write(decoded_file)
    
    #                         _logger.info(f"Archivo guardado en: {file_path}")
    #                         return file_path
    #                     except Exception as e:
    #                         _logger.error(f"Error al decodificar o guardar el archivo: {e}")
    #                         raise UserError("No se pudo guardar el archivo descargado.")
    #                 else:
    #                     _logger.error("La respuesta no contiene el archivo en base64.")
    #                     raise UserError("La respuesta no contiene el archivo en base64.")
    #             else:
    #                 _logger.error(f"Error en la descarga: {respuesta_json.get('mensaje')}")
    #                 raise UserError(f"Error en la descarga: {respuesta_json.get('mensaje')}")
    #         except Exception as e:
    #             _logger.error(f"Error al procesar la respuesta JSON: {e}")
    #             raise UserError("No se pudo procesar la respuesta JSON.")
    #     else:
    #         _logger.error(f"Error HTTP: {response.status_code}")
    #         raise UserError(f"Error HTTP: {response.status_code}")
    
    def GenerarToken(self):           
        username, password, url = self.ObtenerCredencial()
        fecha_token_tfhka = self.fecha_token_tfhka 
        fecha_actual = datetime.now()    
        
        if not isinstance(fecha_token_tfhka, datetime) or fecha_token_tfhka < fecha_actual:
            respuesta = requests.post(url + "/Autenticacion", json={
                "usuario": username,
                "clave": password
            })
            respuesta_json = respuesta.json()
            _logger.warning(respuesta_json)
            codigo = respuesta_json.get("codigo")
            mensaje = respuesta_json.get("mensaje")
            
            if respuesta.status_code == 200:
                if codigo == 200 and "token" in respuesta_json:
                    token = respuesta_json["token"]
                    _logger.info(mensaje)
                    
                    expiracion_str = respuesta_json["expiracion"]
                    expiracion_str = expiracion_str[:26] + 'Z' 
                    expiracion = datetime.strptime(expiracion_str, "%Y-%m-%dT%H:%M:%S.%fZ")
                    
                    self.fecha_token_tfhka = expiracion
                    self.token_actual_tfhka = token
                    return url, token
                elif codigo == 403:
                    _logger.warning(mensaje)
                    raise ValidationError(f"Configuración del Módulo incorrecta: {mensaje}")
                else:
                    _logger.error(f"Error: {codigo}, {mensaje}")
                    raise UserError(f"Error: {codigo} \n{mensaje}")
            else: 
                _logger.error(f"Error: {respuesta.status_code}", {mensaje})
                raise UserError(f"Error {respuesta.status_code}: {mensaje}")
        else:
            _logger.info("El token aún es válido.")
            token = self.token_actual_tfhka
            return url, token

    def ObtenerCredencial(self):
        
        username = None
        password = None
        url = None
        
        for move in self:
            if move.company_id.username_tfhka and move.company_id.password_tfhka and move.company_id.url_tfhka:
                username = move.company_id.username_tfhka
                password = move.company_id.password_tfhka
                url = move.company_id.url_tfhka
            
                return username, password, url
            else:
                _logger.error("USERNAME, PASSWORD o URL vacío.")
                raise ValidationError("Configuración del Módulo incorrecta: USERNAME, PASSWORD o URL vacío.")