from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import relationship
from dotenv import load_dotenv
from datetime import datetime
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
    nivel = db.Column(db.ARRAY(db.String(50)))
    email = db.Column(db.String, unique=True, nullable=False) #55
    telefone = db.Column(db.String) #16
    logradouro = db.Column(db.String)
    numero = db.Column(db.Integer)
    cep = db.Column(db.String) #9
    complemento = db.Column(db.String) #86
    cidade = db.Column(db.String) #55
    estado = db.Column(db.String) #2
    status = db.Column(db.Boolean, default=True)
    edificios = db.relationship('Edificios', backref = 'edificios')
    escolas_historico =  db.relationship('EscolasHistorico', backref = 'escolas_historico')
    data_criacao = db.Column(db.DateTime, server_default=func.now())
    
    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __init__(self, nome, cnpj, nivel, email, telefone, logradouro, numero, cep, complemento, cidade, estado):
        self.nome = nome
        self.cnpj = cnpj
        self.nivel = nivel
        self.email = email
        self.telefone = telefone
        self.logradouro = logradouro
        self.numero = numero
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
            "numero": self.numero,
            "cidade":self.cidade,
            "estado":self.estado
        }
      

class EscolasHistorico(db.Model):
    __table_args__ = {'schema':'main'}
    __tablename__ = 'escolas_historico'

    id = db.Column(db.Integer, primary_key=True)
    fk_escola = db.Column(db.Integer, db.ForeignKey('main.escolas.id'))
    cnpj = db.Column(db.String) #18
    nivel = db.Column(db.ARRAY(db.String(50)))
    cep = db.Column(db.String) #9
    data_alteracao = db.Column(db.DateTime, default=datetime.now)


class Edificios(db.Model):

    __table_args__ = {'schema':'main'}
    __tablename__ = 'edificios'

    id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    fk_escola = db.Column(db.Integer, db.ForeignKey('main.escolas.id'))
    numero_edificio = db.Column(db.String)
    nome_do_edificio = db.Column(db.String)
    cep_edificio = db.Column(db.String)
    cidade_edificio = db.Column(db.String)
    estado_edificio = db.Column(db.String)
    cnpj_edificio = db.Column(db.String)
    logradouro_edificio = db.Column(db.String)
    pavimentos_edificio = db.Column(db.Integer)
    area_total_edificio = db.Column(db.Float)
    reservatorio = db.Column(db.Boolean)
    capacidade_m3_edificio = db.Column(db.Float)
    agua_de_reuso = db.Column(db.Boolean)
    capacidade_reuso_m3_edificio= db.Column(db.Float)
    status = db.Column(db.Boolean, default=True)
    area_umida = db.relationship('AreaUmida', backref = 'area_umida')
    populacao = db.relationship('Populacao', backref = 'populacao')
    hidrometros = db.relationship('Hidrometros', backref = 'hidrometros')

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __init__(self, fk_escola, numero_edificio, nome_do_edificio,cep_edificio, cnpj_edificio, logradouro_edificio, cidade_edificio, estado_edificio, pavimentos_edificio, area_total_edificio, capacidade_m3_edificio , capacidade_reuso_m3_edificio,reservatorio=False, agua_de_reuso=False):

        self.fk_escola = fk_escola
        self.numero_edificio = numero_edificio
        self.nome_do_edificio = nome_do_edificio
        self.cep_edificio = cep_edificio
        self.cnpj_edificio = cnpj_edificio
        self.logradouro_edificio = logradouro_edificio
        self.estado_edificio = estado_edificio
        self.cidade_edificio = cidade_edificio
        self.pavimentos_edificio = pavimentos_edificio
        self.area_total_edificio = area_total_edificio
        self.reservatorio = reservatorio
        self.capacidade_m3_edificio  = capacidade_m3_edificio
        self.agua_de_reuso = agua_de_reuso
        self.capacidade_reuso_m3_edificio = capacidade_reuso_m3_edificio if capacidade_reuso_m3_edificio is not None else 0;

    def to_json(self):
        return {
            "id":self.id,
            "fk_escola":self.fk_escola,
            "numero_edificio":self.numero_edificio,
            "nome_do_edificio":self.nome_do_edificio,
            "cep_edificio":self.cep_edificio,
            "cnpj_edificio":self.cnpj_edificio,
            "logradouro_edificio":self.logradouro_edificio,
            "cidade_edificio":self.cidade_edificio,
            "estado_edificio":self.estado_edificio,
            "pavimentos_edificio":self.pavimentos_edificio,
            "area_total_edificio":self.area_total_edificio,
            "reservatorio":self.reservatorio,
            "capacidade_m3_edificio":self.capacidade_m3_edificio ,
            "agua_de_reuso":self.agua_de_reuso,
            "capacidade_reuso_m3_edificio": self.capacidade_reuso_m3_edificio
        }


class Populacao(db.Model):
        __table_args__ = {'schema': 'main'}
        __tablename__ = 'populacao'

        id = db.Column(db.Integer, autoincrement=True, primary_key=True)
        fk_edificios = db.Column(db.Integer, db.ForeignKey('main.edificios.id'))
        nivel_de_usuario = db.Column(db.ARRAY(db.String(50)))
        periodo = db.Column(db.String)
        quant_de_funcionarios_usuarios = db.Column(db.Integer)
        quant_de_alunos_usuarios = db.Column(db.Integer)
        status = db.Column(db.Boolean, default=True)


        def update(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)


        def __init__(self, fk_edificios, nivel_de_usuario, periodo, quant_de_funcionarios_usuarios, quant_de_alunos_usuarios):
            self.fk_edificios = fk_edificios
            self.nivel_de_usuario = nivel_de_usuario
            self.periodo = periodo
            self.quant_de_funcionarios_usuarios = quant_de_funcionarios_usuarios
            self.quant_de_alunos_usuarios = quant_de_alunos_usuarios

        def to_json(self):
            return {
                "id": self.id,
                "fk_edificios": self.fk_edificios,
                "nivel_de_usuario": self.nivel_de_usuario,
                "periodo": self.periodo,
                "quant_de_funcionarios_usuarios": self.quant_de_funcionarios_usuarios,
                "quant_de_alunos_usuarios": self.quant_de_alunos_usuarios
            }


class Hidrometros(db.Model):
        __table_args__ = {'schema': 'main'}
        __tablename__ = 'hidrometros'

        id = db.Column(db.Integer, autoincrement=True, primary_key=True)
        fk_edificios = db.Column(db.Integer, db.ForeignKey('main.edificios.id'))
        hidrometro_edificio = db.Column(db.String)
        status = db.Column(db.Boolean, default=True)


        def update(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)


        def __init__(self, fk_edificios, hidrometro_edificio ):
            self.fk_edificios = fk_edificios
            self.hidrometro_edificio = hidrometro_edificio

        def to_json(self):
            return {
                "id": self.id,
                "fk_edificios": self.fk_edificios,
                "hidrometro_edificio":self.hidrometro_edificio
            }



class AreaUmida(db.Model):
    
        __table_args__ = {'schema':'main'}
        __tablename__ = 'area_umida'

        id = db.Column(db.Integer, autoincrement = True, primary_key = True)
        fk_edificios = db.Column(db.Integer, db.ForeignKey('main.edificios.id'))
        tipo_area_umida = db.Column(db.String)
        nome_area_umida = db.Column(db.String)
        localizacao_area_umida = db.Column(db.String)
        status_area_umida = db.Column(db.String)
        status = db.Column(db.Boolean, default=True)
        equipamentos = db.relationship('Equipamentos', backref = 'equipamentos')

        def update(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)

        def __init__(self, fk_edificios, tipo_area_umida, nome_area_umida, localizacao_area_umida, status_area_umida):

            self.fk_edificios = fk_edificios
            self.tipo_area_umida= tipo_area_umida
            self.nome_area_umida = nome_area_umida
            self.localizacao_area_umida = localizacao_area_umida
            self.status_area_umida = status_area_umida


        def to_json(self):
            return {
                "id":self.id,
                "fk_edificios":self.fk_edificios,
                "tipo_area_umida":self.tipo_area_umida,
                "nome_area_umida":self.nome_area_umida,
                "localizacao_area_umida":self.localizacao_area_umida,
                "status_area_umida":self.status_area_umida
            }



class Equipamentos(db.Model):

    __table_args__ = {'schema':'main'}
    __tablename__ = 'equipamentos'

    id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    fk_area_umida= db.Column(db.Integer, db.ForeignKey('main.area_umida.id'))
    tipo_equipamento = db.Column(db.String)
    quant_total = db.Column(db.Integer)
    quant_com_problema = db.Column(db.Integer)
    # vazamentos = db.Column(db.Integer)
    quant_inutilizadas = db.Column(db.Integer)
    status = db.Column(db.Boolean, default=True)

    def update(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)

    def __init__(self, fk_area_umida, tipo_equipamento, quant_total, quant_com_problema, quant_inutilizadas):

        self.fk_area_umida = fk_area_umida
        self.tipo_equipamento= tipo_equipamento
        self.quant_total = quant_total
        self.quant_com_problema = quant_com_problema
        self.quant_inutilizadas = quant_inutilizadas

    def to_json(self):
        return {
            "id":self.id,
            "fk_area_umida":self.fk_area_umida,
            "tipo_equipamento":self.tipo_equipamento,
            "quant_total":self.quant_total,
            "quant_com_problema":self.quant_com_problema,
            "quant_inutilizadas":self.quant_inutilizadas
        }