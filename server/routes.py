#
#   Imports
#
from forms import *
from models import *
from flask_table import Table, Col, LinkCol
from flask import render_template, request, redirect, url_for, jsonify, flash

#
#   Edit Research table class
#
class WriteActuatorTable (Table):
    classes = ['table']
    id = Col('Id', show = False)
    identificacao = Col('Identificação')
    tipo = Col('Tipo de dispositivo')
    porta = Col('Porta')
    ultimo_valor = Col('Último valor')
    edit = LinkCol('Enviar novo valor', 'write', url_kwargs=dict(id = 'id'))

#
#   Apply Research table class
#
class ReadSensorTable (Table):
    classes = ['table']
    id = Col('Id', show = False)
    identificacao = Col('Identificação')
    tipo = Col('Tipo de dispositivo')
    porta = Col('Porta')
    ultimo_valor = Col('Último valor')
    read = LinkCol('Realizar leitura', 'read', url_kwargs=dict(id = 'id'))

#
#   Devices table class
#
class DevicesTable (Table):
    classes = ['table']
    name = Col('Identificação')
    port_type = Col('Tipo de dispositivo')
    port_number = Col('Porta')
    last_value = Col('Último valor')

#
#   Exception class (from flask Docs, minor changes)
#
class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['error_message'] = self.message
        rv['error_code'] = self.status_code
        return rv

#
#   Error pages
#
@app.errorhandler(InvalidUsage)
def unauthorized (error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return render_template('error_page.html', error_code = error.status_code, error_message = error.message)

#
#   Routes
#

# Route to homepage
@app.route('/')
def homepage():
    return render_template('dashboard.html')

# Route to the main register page
@app.route('/new-device', methods = ['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST':
        if form.porta.data:
            try:
                existing_device = Dispositivo.objects(porta=form.porta.data).first()
            except:
                raise InvalidUsage('Foi detectado um problema no banco de dados, entre em contato com nosso time!', status_code = 400)
            if existing_device is None:
                if form.identificacao.data:
                    if form.tipo_dispositivo.data == TIPO_SENSOR:
                        new_device = Sensor(identificacao = form.identificacao.data, porta = form.porta.data, tipo = form.tipo_porta.data).save()
                        return redirect(url_for('homepage'))
                    else:
                        new_device = Atuador(identificacao = form.identificacao.data, porta = form.porta.data, tipo = form.tipo_porta.data).save()
                        return redirect(url_for('homepage'))
                else:
                    flash ('Favor inserir a identificação!')
            else:
                flash('Um dispositivo já está cadastrado nessa porta!')
        else:
            flash('Favor inserir o número da porta!')
    return render_template('register.html', form = form)

# Route to list all available sensors
@app.route('/sensores', methods = ['GET', 'POST'])
def sensors():
    sensors_list = Dispositivo.objects(_cls = "Dispositivo.Sensor")
    table = ReadSensorTable(sensors_list)
    return render_template('table_layout.html', table = table, title = "Sensores")

# Route to list all available actuators
@app.route('/atuadores', methods = ['GET', 'POST'])
def actuators():
    actuators_list = Dispositivo.objects(_cls = "Dispositivo.Atuador")
    table = WriteActuatorTable(actuators_list)
    return render_template('table_layout.html', table = table, title = "Atuadores")

# Route to edit a single research
@app.route('/write-actuator/<id>', methods=['GET', 'POST'])
def write (id):
    actuator = Dispositivo.objects(id = id).first()
    if actuator:
        form = WriteForm(obj=actuator)
        if request.method == 'POST':
            pwm = form.pwm.data
            actuator.ultimo_valor = form.value.data
            actuator.EscreverValor(pwm = pwm)
            actuator.save()
            return redirect('/atuadores')
        return render_template('write_device.html', form = form, title = "Escrever num atuador", id = id, button_message = "Enviar!", actuator = actuator)
    else:
        raise InvalidUsage('Erro ao tentar carregar o ID #{id}'.format(id = id), status_code = 500)

# Route to apply to a single research
@app.route('/read-sensor/<id>')
def read(id):
    sensor = Dispositivo.objects(id = id).first() 
    if sensor:
        flash('Você enviou uma solicitação de leitura para o sensor {}'.format(sensor.identificacao))
        sensor.ultimo_valor = sensor.LerValor()
        sensor.save()
        return redirect('/sensores')
    else:
        raise InvalidUsage('Erro ao tentar carregar o ID #{id}'.format(id = id), status_code = 500)

# Route to all requests
@app.route('/requests')
def requests():
    user_type = get_user_type()
    if (user_type == PROFESSOR_USER):
        researches_list = Research.objects(professor = current_user.full_name)
        requests_list = []
        for research in researches_list:
            if research.requests != []:
                for req in research.requests:
                    requests_list.append({
                        'title' : research.title,
                        'full_name' : req.full_name,
                        'lattes' : req.lattes,
                        'email' : req.email
                    })
        requests_list.reverse()
        table = RequestsTable(requests_list)
        return render_template('researches.html', table = table, user_type = 'professor')
    else:
        raise InvalidUsage(HTTP_401_DEFAULT_MESSAGE, status_code = 401)

# Route to test API
@app.route('/test-api', methods = ['POST'])
def test_api ():
    from random import randint
    return str({"data" : randint(0, 255)})

# class RequestsTable (Table):
#     title = Col('Pesquisa')
#     full_name = Col('Nome do aluno')
#     lattes = Col('Link Lattes')
#     email = Col('E-mail')

if __name__ == '__main__':
    app.run(host = "0.0.0.0", debug = True)