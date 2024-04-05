import mysql.connector
from mysql.connector import errorcode
from flask_bcrypt import generate_password_hash

print("Conectando...")
try:
      conn = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='admin'
      )
except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('Existe algo errado no nome de usuário ou senha')
      else:
            print(err)

cursor = conn.cursor()

cursor.execute("DROP DATABASE IF EXISTS `meetup`;")

cursor.execute("CREATE DATABASE `meetup`;")

cursor.execute("USE `meetup`;")

# criando tabelas
TABLES = {}
TABLES['Usuarios'] = ('''
CREATE TABLE `usuarios` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nome` VARCHAR(50) NOT NULL,
  `email` VARCHAR(50) NOT NULL,
  `senha` VARCHAR(100) NOT NULL,
  `data_cadastro` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `ativo` BOOLEAN NOT NULL DEFAULT TRUE,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

for tabela_nome in TABLES:
      tabela_sql = TABLES[tabela_nome]
      try:
            print('Criando tabela {}:'.format(tabela_nome), end=' ')
            cursor.execute(tabela_sql)
      except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                  print('Já existe')
            else:
                  print(err.msg)
      else:
            print('OK')


# inserindo usuarios
usuario_sql = 'INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)'
usuarios = [
      ("Leonardo Ferreira", "leonardoferreira1002@live.com", generate_password_hash("12345").decode('utf-8')),
      ("Stephani Borzi", "stephaniborzi@meetup.com", generate_password_hash("12345").decode('utf-8')),
      ("Pedro Henrique", "pedrohenrique@meetup.com", generate_password_hash("12345").decode('utf-8'))
]
cursor.executemany(usuario_sql, usuarios)

cursor.execute('select * from meetup.usuarios')
print(' -------------  Usuários:  -------------')
for user in cursor.fetchall():
    print(user[1])

# commitando se não nada tem efeito
conn.commit()

cursor.close()
conn.close()