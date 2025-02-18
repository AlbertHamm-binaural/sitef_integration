from unittest.mock import patch
from odoo.tests.common import TransactionCase
from odoo.tests import tagged
import requests
import logging
import hashlib

_logger = logging.getLogger(__name__)

@tagged("bin","-at_install","post_install")
class TestCambioSitef(TransactionCase):
    
    def test_get_token(self, url="https://api.sitefdevenezuela.com/prod/s4/sitef/apiToken", username="arkisoft", password="9cf483db1c106c3c30694d4f0375e2ab"):
        if username != "" and password != "":
            _logger.warning("INSIDE GET TOKEN")
            response = requests.post(url, json={
                "username": username,
                "password": password
            })
            response_json = response.json()
            _logger.warning(response_json)
            
            if response.status_code == 200 and "data" in response_json and "token" in response_json["data"]:
                token = response_json["data"]["token"]
                _logger.warning(token)
                return token, username
            else:
                return {"error": "Campo username o password incorrecto."}
        else:
            return {"error": "Campo username o password vacío."}

        

    @patch('requests.post')
    def test_empty_destinationmobilenumber(self):
        """Prueba cuando el campo de telefono está vacío."""
        token, username = self.test_get_token()
        token_md5 = hashlib.md5(token.encode()).hexdigest()
        # Configuración inicial para las pruebas
        self.url = "https://api.sitefdevenezuela.com/prod/s4/sitefAuth/setVueltoSitef"
        self.username = username
        self.token = token_md5
        self.idbranch = "117"
        self.codestall = "003"
        self.destinationid = "V30396029"
        self.destinationmobilenumber = ""
        self.destinationbank = "172"
        self.issuingbank = "172"
        self.invoicenumber = "41229921"
        self.amount = 1.0

        # Realiza una solicitud real a la API
        response = requests.post(self.url, json={
            "username": self.username,
            "token": self.token,
            "idbranch": self.idbranch,
            "codestall": self.codestall,
            "destinationid": self.destinationid,
            "destinationmobilenumber": self.destinationmobilenumber,
            "destinationbank": self.destinationbank,
            "issuingbank": self.issuingbank,
            "invoicenumber": self.invoicenumber,
            "amount": self.amount
        })

        _logger.warning(response.status_code)
        # Verifica que la respuesta sea la esperada
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "success")

    @patch('requests.post')
    def test_empty_destinationid(self):
        """Prueba cuando el campo de cedula está vacío."""
        token, username = self.get_token()
        token_md5 = hashlib.md5(token.encode()).hexdigest()
        # Configuración inicial para las pruebas
        self.url = "https://api.sitefdevenezuela.com/prod/s4/sitefAuth/setVueltoSitef"
        self.username = username
        self.token = token_md5
        self.idbranch = "117"
        self.codestall = "003"
        self.destinationid = ""
        self.destinationmobilenumber = "584122397209"
        self.destinationbank = "172"
        self.issuingbank = "172"
        self.invoicenumber = "41229921"
        self.amount = 1.0
        
        # Realiza una solicitud real a la API
        response = requests.post(self.url, json={
            "username": self.username,
            "token": self.token,
            "idbranch": self.idbranch,
            "codestall": self.codestall,
            "destinationid": self.destinationid,
            "destinationmobilenumber": self.destinationmobilenumber,
            "destinationbank": self.destinationbank,
            "issuingbank": self.issuingbank,
            "invoicenumber": self.invoicenumber,
            "amount": self.amount
        })

        _logger.warning(response.status_code)
        # Verifica que la respuesta sea la esperada
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "success")

    @patch('requests.post')
    def test_incorrect_destinationid(self):
        """Prueba cuando el campo de cedula incorrecta."""
        token, username = self.get_token()
        token_md5 = hashlib.md5(token.encode()).hexdigest()
        # Configuración inicial para las pruebas
        self.url = "https://api.sitefdevenezuela.com/prod/s4/sitefAuth/setVueltoSitef"
        self.username = username
        self.token = token_md5
        self.idbranch = "117"
        self.codestall = "003"
        self.destinationid = "V30396028"
        self.destinationmobilenumber = "584122397209"
        self.destinationbank = "172"
        self.issuingbank = "172"
        self.invoicenumber = "41229921"
        self.amount = 1.0
        
        # Realiza una solicitud real a la API
        response = requests.post(self.url, json={
            "username": self.username,
            "token": self.token,
            "idbranch": self.idbranch,
            "codestall": self.codestall,
            "destinationid": self.destinationid,
            "destinationmobilenumber": self.destinationmobilenumber,
            "destinationbank": self.destinationbank,
            "issuingbank": self.issuingbank,
            "invoicenumber": self.invoicenumber,
            "amount": self.amount
        })

        _logger.warning(response.status_code)
        # Verifica que la respuesta sea la esperada
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "success")


    @patch('requests.post')
    def test_empty_destinationmobilenumber(self):
        """Prueba cuando el campo telefono es incorrecto."""
        token, username = self.get_token()
        token_md5 = hashlib.md5(token.encode()).hexdigest()
        # Configuración inicial para las pruebas
        self.url = "https://api.sitefdevenezuela.com/prod/s4/sitefAuth/setVueltoSitef"
        self.username = username
        self.token = token_md5
        self.idbranch = "117"
        self.codestall = "003"
        self.destinationid = "V30396029"
        self.destinationmobilenumber = "584122397208"
        self.destinationbank = "172"
        self.issuingbank = "172"
        self.invoicenumber = "41229921"
        self.amount = 1.0
        
        # Realiza una solicitud real a la API
        response = requests.post(self.url, json={
            "username": self.username,
            "token": self.token,
            "idbranch": self.idbranch,
            "codestall": self.codestall,
            "destinationid": self.destinationid,
            "destinationmobilenumber": self.destinationmobilenumber,
            "destinationbank": self.destinationbank,
            "issuingbank": self.issuingbank,
            "invoicenumber": self.invoicenumber,
            "amount": self.amount
        })

        _logger.warning(response.status_code)
        # Verifica que la respuesta sea la esperada
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "success")
        
    @patch('requests.post')
    def test_incorrect_destinationbank(self):
        """Prueba cuando el campo telefono es incorrecto."""
        token, username = self.get_token()
        token_md5 = hashlib.md5(token.encode()).hexdigest()
        # Configuración inicial para las pruebas
        self.url = "https://api.sitefdevenezuela.com/prod/s4/sitefAuth/setVueltoSitef"
        self.username = username
        self.token = token_md5
        self.idbranch = "117"
        self.codestall = "003"
        self.destinationid = "V30396029"
        self.destinationmobilenumber = "584122397209"
        self.destinationbank = "132"
        self.issuingbank = "172"
        self.invoicenumber = "41229921"
        self.amount = 1.0
    #CADA BANCO DA UNA RESPUESTA DIFERENTE
    
    # Realiza una solicitud real a la API
        response = requests.post(self.url, json={
            "username": self.username,
            "token": self.token,
            "idbranch": self.idbranch,
            "codestall": self.codestall,
            "destinationid": self.destinationid,
            "destinationmobilenumber": self.destinationmobilenumber,
            "destinationbank": self.destinationbank,
            "issuingbank": self.issuingbank,
            "invoicenumber": self.invoicenumber,
            "amount": self.amount
        })

        _logger.warning(response.status_code)
        # Verifica que la respuesta sea la esperada
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "success")