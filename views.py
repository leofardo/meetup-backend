from flask import request, redirect, session, flash, url_for, send_from_directory, jsonify
from app import app, db
from flask_bcrypt import check_password_hash, generate_password_hash
from models import Usuarios
from helpers import *
import time

@app.route('/')
def index():
    return '<h1>Hello World</h1>'


@app.route('/cadastrar', methods=['POST'])
def cadastrar():

    nome = request.form['nome'].strip(" ")
    email = request.form['email'].strip(" ")
    senha = request.form['senha'].strip(" ")

    if nome == '' or email == '' or senha == '':
        return jsonify({'erro': 'Todos os campos são necessários (email, nome, senha).'}), 400

    if Usuarios.query.filter_by(email=email).first():
        return jsonify({'erro': 'Conta com este email já existe.'}), 409

    senha_criptografada = generate_password_hash(senha).decode('utf-8')

    novo_usuario = Usuarios(
        nome=nome,
        email=email,
        senha=senha_criptografada
    )

    db.session.add(novo_usuario)
    db.session.commit()

    return jsonify({'mensagem': 'Usuário cadastrado com sucesso!'}), 201

@app.route('/autenticar', methods=['POST',])
def autenticar():

    #fazendo o select com o ORM SQLALCHEMY
    usuario = Usuarios.query.filter_by(email=request.form['email']).first()

    if usuario:
        if check_password_hash(usuario.senha, request.form['senha']):
            if usuario.ativo:
                session['usuario_logado'] = usuario.email
                return jsonify({'status': 'sucesso', 'mensagem': f'{usuario.nome} logado com sucesso!', 'dados':{'email': usuario.email, 'nome': usuario.nome, 'id': usuario.id}})
            else:
                return jsonify({'status': 'erro', 'mensagem': 'Conta inativa.'}), 401 # 401 Unauthorized
        else:
            return jsonify({'status': 'erro', 'mensagem': 'Senha incorreta.'}), 401  # 401 Unauthorized
    else:
        return jsonify({'status': 'erro', 'mensagem': 'Usuário não encontrado.'}), 404  # 404 Not Found

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    return jsonify({'status': 'sucesso', 'mensagem': 'Logout efetuado com sucesso!'})

@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)

