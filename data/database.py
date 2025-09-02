from peewee import *
import os
import sys
import shutil

def get_db_path():
    """
    Retorna o caminho do banco de dados.
    No .exe, salva em %AppData%\Financer\db.sqlite3 para garantir persistência.
    No Python normal, usa a pasta 'data' do projeto.
    """
    if getattr(sys, 'frozen', False):
        # No executável: usa AppData
        app_name = "CASCALHO"
        appdata_dir = os.path.join(os.getenv('APPDATA'), app_name)
        os.makedirs(appdata_dir, exist_ok=True)
        db_path = os.path.join(appdata_dir, "db.sqlite3")

        # Se o banco ainda não existe, copia o modelo do executável
        if not os.path.exists(db_path):
            bundled_db = os.path.join(sys._MEIPASS, "data", "db.sqlite3")
            if os.path.exists(bundled_db):
                shutil.copy2(bundled_db, db_path)
    else:
        # No Python normal: usa a pasta data do projeto
        base_path = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(base_path, "data", "db.sqlite3")

    return db_path


db = SqliteDatabase(get_db_path())


class Usuario_cascalho(Model):
    nome = CharField()
    salario = FloatField()
    maximo_valor = FloatField(default=1000.0)
    moeda_atual = CharField(default='R$')

    class Meta:
        database = db


class Movimentacao(Model):
    usuario = ForeignKeyField(Usuario_cascalho, backref='movimentacoes')
    descricao = CharField()
    valor = FloatField()
    tipo = CharField()  # "receita" ou "gasto"
    categoria = CharField(null=True)
    data = DateField()

    class Meta:
        database = db


# Cria as tabelas se não existirem
db.connect()
db.create_tables([Usuario_cascalho, Movimentacao])
