import os

SECRET_KEY = 'meetup'

#ORM SQLALCHEMY SERVE PARA EM CASOS DE TROCA DE SGBD, TEM COMO TROCAR DIRETO NA VAIRAVEL SGBD
#Object-Relational-Mapper

SQLALCHEMY_DATABASE_URI = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(

    SGBD = 'mysql+mysqlconnector',
    usuario = 'root',
    senha = 'admin',
    servidor = 'localhost',
    database = 'meetup'
)

UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + '/uploads'

