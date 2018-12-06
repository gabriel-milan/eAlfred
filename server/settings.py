###
# File that configures everything. Set macros here
###

# Database
DATABASE_NAME = 'eAlfred'
DATABASE_URI = 'mongodb://127.0.0.1:27017/' + DATABASE_NAME

# Flask app
CSRF_SECRET_KEY = 'IUUIH@*HA#()RU)(A9102u'

# Models settings
MAX_DEVICE_NAME = 50

# Types of requests
READ_REQUEST = 0
WRITE_REQUEST = 1
PWM_WRITE_REQUEST = 2

# Types of ports
ANALOG_PORT = 0
DIGITAL_PORT = 1

# Types of devices
TIPO_SENSOR = True
TIPO_ATUADOR = False

# Error messages
HTTP_401_DEFAULT_MESSAGE = 'Você não está autorizado a realizar essa ação!'

# Arduino configurations
ARDUINO_IP = "192.168.88.111"