# -*- coding: utf-8 -*-
from flask import Flask, request, redirect, render_template
from config import app_config, app_active
from flask_sqlalchemy import SQLAlchemy
from controller.User import UserController


config = app_config[app_active]


def create_app(config_name):
    app = Flask(__name__, template_folder='templates')

    app.secret_key = config.SECRET
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db = SQLAlchemy(config.APP)
    db.init_app(app)

    @app.route('/')
    def index():
        return 'Hello Word!'

    @app.route('/login/')
    def login():
        return 'Aqui entrará a tela de login'

    @app.route('/login/', methods=['POST'])
    def login_post():
        user = UserController()
        email = request.form['email']
        password = request.form['password']

        result = user.login(email, password)

        if result:
            return redirect('/admin')
        else:
            return render_template('login.html',
                                   data={'status': 40,
                                         'msg': 'Dados de usuário incorretos',
                                         'type': None})

    @app.route('/recovery-password/')
    def recovery_password():
        return 'Aqui entrará a tela de recuperar senha'

    @app.route('/recovery-password/', methods=['POST'])
    def send_recovery_password():
        user = UserController()

        result = user.recovery(request.form['email'])

        if result:
            msg = 'E-mail de recuperação enviado com sucesso'
            return render_template('recovery.html', data={'status': 200,
                                                          'msg': msg})
        else:
            msg = 'Erro ao enviar e-mail de recuperação'
            return render_template('recovery.html', data={'status': 401,
                                                          'msg': msg})

    return app
