from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from dotenv import load_dotenv
from os import path
import os



db = SQLAlchemy()

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, "../../.env"))

class Escolas(db.Model):

    __table_args__ = {'schema':'main'}
    __tablename__ = 'escolas'

    id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    nome = db.Column(db.String, nullable = False) #255
    cnpj = db.Column(db.String, unique=True, nullable=False) #18
    nivel = db.Column(db.String) #25
    email = db.Column(db.String, unique=True, nullable=False) #55
    telefone = db.Column(db.String) #16
    logradouro = db.Column(db.String)
    cep = db.Column(db.String) #9
    complemento = db.Column(db.String) #86
    cidade = db.Column(db.String) #55
    estado = db.Column(db.String) #2

    #edificios = db.relationship('Edificios', backref = 'edificios')

    def __init__(self, nome, cnpj, nivel, email, telefone, logradouro, cep, complemento, cidade, estado):
        self.nome = nome
        self.cnpj = cnpj
        self.nivel = nivel
        self.email = email
        self.telefone = telefone
        self.logradouro = logradouro
        self.cep = cep
        self.complemento = complemento
        self.cidade = cidade
        self.estado = estado

    def to_json(self):
        return {
            "nome":self.nome,
            "cnpj":self.cnpj,
            "nivel":self.nivel,
            "email":self.email,
            "telefone":self.telefone,
            "logradouro":self.logradouro,
            "cep":self.cep,
            "complemento":self.complemento,
            "cidade":self.cidade,
            "estado":self.estado
        }


class Edificios(db.Model):

    __table_args__ = {'schema':'main'}
    __tablename__ = 'edificios'

    id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    fk_escola = db.Column(db.Integer ) #db.ForeignKey('main.escolas.id')
    nome_do_edificio = db.Column(db.String)
    nivel = db.Column(db.String)
    periodos = db.Column(db.String)
    cep = db.Column(db.String)
    logradouro = db.Column(db.String)
    numero_do_hidrometro = db.Column(db.String)
    quanti_de_pavimentos = db.Column(db.Integer)
    area_total = db.Column(db.Float)
    quant_de_colaboradores = db.Column(db.Integer)
    quant_de_alunos = db.Column(db.Integer)
    reservatorio = db.Column(db.String)
    capacidade_reservatorio = db.Column(db.Float)
    agua_de_reuso = db.Column(db.String)

    def __init__(self, fk_escola, nome_do_edificio, nivel, periodos, cep, logradouro, numero_do_hidrometro, quanti_de_pavimentos, area_total, quant_de_colaboradores, quant_de_alunos, capacidade_reservatorio, reservatorio='off', agua_de_reuso='off'):

        self.fk_escola = fk_escola
        self.nome_do_edificio = nome_do_edificio
        self.nivel = nivel
        self.periodos = periodos
        self.cep = cep
        self.logradouro = logradouro
        self.numero_do_hidrometro = numero_do_hidrometro
        self.quanti_de_pavimentos = quanti_de_pavimentos
        self.area_total = area_total
        self.quant_de_colaboradores = quant_de_colaboradores
        self.quant_de_alunos = quant_de_alunos
        self.reservatorio = reservatorio
        self.capacidade_reservatorio = capacidade_reservatorio
        self.agua_de_reuso = agua_de_reuso

    def to_json(self):
        return {

            "fk_escola":self.fk_escola,
            "nome_do_edificio":self.nome_do_edificio,
            "nivel":self.nivel,
            "periodos":self.periodos,
            "cep":self.cep,
            "logradouro":self.logradouro,
            "numero_do_hidrometro":self.numero_do_hidrometro,
            "quanti_de_pavimentos":self.quanti_de_pavimentos,
            "area_total":self.area_total,
            "quant_de_colaboradores":self.quant_de_colaboradores,
            "quant_de_alunos":self.quant_de_alunos,
            "reservatorio":self.reservatorio,
            "capacidade_reservatorio":self.capacidade_reservatorio,
            "agua_de_reuso":self.agua_de_reuso
        }


class AreaUmida(db.Model):

        __table_args__ = {'schema':'main'}
        __tablename__ = 'area_umida'

        id = db.Column(db.Integer, autoincrement = True, primary_key = True)
        fk_edificios = db.Column(db.Integer, db.ForeignKey('main.edificios.id'))
        tipo = db.Column(db.String)
        nome_da_area_umida = db.Column(db.String)
        localizacao = db.Column(db.String)
        status = db.Column(db.String)
        equipamentos = db.relationship('Equipamentos', backref = 'equipamentos')

        def __init__(self, fk_edificios, tipo, nome_da_area_umida, localizacao, status):

            self.fk_edificios = fk_edificios
            self.tipo= tipo
            self.nome_da_area_umida = nome_da_area_umida
            self.localizacao = localizacao
            self.status = status


        def to_json(self):
            return {
                "id":self.id,
                "fk_edificios":self.fk_edificios,
                "tipo":self.tipo,
                "nome_da_area_umida":self.nome_da_area_umida,
                "localizacao":self.localizacao,
                "status":self.status
            }


class Equipamentos(db.Model):

    __table_args__ = {'schema':'main'}
    __tablename__ = 'equipamentos'

    id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    fk_area_umida= db.Column(db.Integer, db.ForeignKey('main.area_umida.id'))
    tipo = db.Column(db.String)
    quant_total = db.Column(db.Integer)
    quant_problemas = db.Column(db.Integer)
    vazamentos = db.Column(db.Integer)
    quant_inutilizada = db.Column(db.Integer)

    def __init__(self, fk_area_umida, tipo, quant_total, quant_problemas, vazamentos, quant_inutilizada):

        self.fk_area_umida = fk_area_umida
        self.tipo= tipo
        self.quant_total = quant_total
        self.quant_problemas = quant_problemas
        self.vazamentos = vazamentos
        self.quant_inutilizada = quant_inutilizada

    def to_json(self):
        return {
            "id":self.id,
            "fk_area_umida":self.fk_area_umida,
            "tipo":self.tipo,
            "quant_total":self.quant_total,
            "quant_problemas":self.quant_problemas,
            "vazamentos":self.vazamentos,
            "quant_inutilizada":self.quant_inutilizada
        }