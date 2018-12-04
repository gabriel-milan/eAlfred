#
#   Imports
#
import json
import requests
from app import *
from flask_mongoengine import Document
from wtforms import StringField, BooleanField

#
#   Dispositivo model
#
class Dispositivo (db.Document):
    meta = {
        'collection': 'Dispositivo',
        'allow_inheritance': True
    }
    identificacao = db.StringField(max_length = MAX_DEVICE_NAME)
    porta = db.IntField (min_value = 0, required = True)
    tipo = db.BooleanField ()
    ultimo_valor = db.IntField ()

    # Function to generate JSON
    def __generate_json (self, request_type):
        output = json.dumps({
            "request_type" : request_type,
            "port_type" : int(self.tipo),
            "port_number" : int(self.porta),
            "value" : int(self.ultimo_valor) if self.ultimo_valor else 0
        })
        print (output)
        return output

    # Function to send request to Arduino
    def __request_arduino (self, json_message):
        request = requests.post("http://" + ARDUINO_IP, data = json_message)
        print ("======================REQUEST CONTENT======================")
        print (request.content)
        return request.content.decode('utf-8').replace("'", "\"")

    # Function to parse data from Arduino
    def __parse_response (self, json_message):
        response_dict = json.loads(json_message)
        print ("======================RESPONSE DICT======================")
        print (response_dict)
        return response_dict['data']

    # Function to wrap all previous function into a single one, sending the request to Arduino and receiving it back
    def arduino_communication (self, request_type, pwm = False):
        if (pwm == True):
            request_type = PWM_WRITE_REQUEST
        json_message = self.__generate_json(request_type)
        response = self.__request_arduino(json_message)
        return self.__parse_response(response)

#
#   Sensor model
#
class Sensor (Dispositivo):
    meta = {
        'collection': 'Sensor',
    }

    # Function to read values
    def LerValor (self):
        return self.arduino_communication(request_type = READ_REQUEST)

#
#   Atuador model
#
class Atuador (Dispositivo):
    meta = {
        'collection': 'Atuador',
    }

    # Function to write values
    def EscreverValor (self, pwm = False):
        self.arduino_communication(request_type = WRITE_REQUEST, pwm = pwm)