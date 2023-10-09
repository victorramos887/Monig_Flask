from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, text, DDL, and_, not_
from datetime import datetime
from sqlalchemy import inspect
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy.orm.collections as col
import sqlalchemy as sa
from sqlalchemy_continuum import make_versioned


db = SQLAlchemy()


make_versioned(user_cls=None)

# migrate = Migrate(db)


class Cliente(db.Model):

    __table_args__ = {'schema': 'main'}
    __tablename__ = 'cliente'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    nome = db.Column(db.String(255), nullable=False, unique=True)
    email = db.Column(db.String(55), unique=True, nullable=False)
    cnpj = db.Column(db.String(18), unique=True, nullable=False)
    telefone = db.Column(db.String(12))

    usuarios = db.relationship('Usuarios', backref='usuarios')

    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __init__(self, nome, cnpj, email, telefone):
        self.nome = nome
        self.email = email
        self.cnpj = cnpj
        self.telefone = telefone

    def to_json(self):
        return {attr.name: getattr(self, attr.name) for attr in self.__table__.columns}


class Escolas(db.Model):

    __versioned__ = {}
    __table_args__ = {'schema': 'main'}
    __tablename__ = 'escolas'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    nome = db.Column(db.String, unique=True)  # 255
    cnpj = db.Column(db.String)  # 18
    email = db.Column(db.String)  # 55
    telefone = db.Column(db.String(25))  # 16
    status_do_registro = db.Column(db.Boolean, default=True)
    edificios = db.relationship('Edificios', backref='edificios')
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __init__(self, nome, cnpj, email, telefone):
        self.nome = nome
        self.cnpj = cnpj
        self.email = email
        self.telefone = telefone

    def to_json(self):
        return {attr.name: getattr(self, attr.name) for attr in self.__table__.columns}


class Reservatorios(db.Model):

    __versioned__ = {}
    __table_args__ = {'schema': 'main'}
    __tablename__ = 'reservatorios'

    id: db.Mapped[int] = db.mapped_column(
        db.Integer, autoincrement=True, primary_key=True)
    fk_escola = db.Column(db.Integer, db.ForeignKey('main.escolas.id'))
    nome_do_reservatorio = db.Column(db.String, nullable=False)
    status_do_registro = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    edificio = db.relationship(
        'Edificios',
        back_populates="reservatorio",
        secondary="main.reservatorio_edificio",
    )

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __init__(self, fk_escola, nome_do_reservatorio):

        self.fk_escola = fk_escola
        self.nome_do_reservatorio = nome_do_reservatorio

    def to_json(self):
        return {attr.name: getattr(self, attr.name) for attr in self.__table__.columns}


class Edificios(db.Model):

    __versioned__ = {}
    # trunk-ignore(ruff/D300)
    '''__table_args__ = (db.UniqueConstraint('nome_do_edificio', 'fk_escola', name='nome_edifico_unico'),
                      db.Index('ix_edificio_nome_escola',
                               'nome_do_edificio', 'fk_escola', unique=True),
                      {'schema': 'main'})'''
    __table_args__ = {'schema': 'main'}
    __tablename__ = 'edificios'

    id: db.Mapped[int] = db.mapped_column(
        db.Integer, autoincrement=True, primary_key=True)
    fk_escola = db.Column(db.Integer, db.ForeignKey('main.escolas.id'))
    numero_edificio = db.Column(db.String)
    nome_do_edificio = db.Column(db.String, nullable=False)
    principal = db.Column(db.Boolean)
    cep_edificio = db.Column(db.String)
    bairro_edificio = db.Column(db.String)
    cidade_edificio = db.Column(db.String)
    estado_edificio = db.Column(db.String)
    cnpj_edificio = db.Column(db.String)
    logradouro_edificio = db.Column(db.String)
    complemento_edificio = db.Column(db.String)
    pavimentos_edificio = db.Column(db.Integer)
    area_total_edificio = db.Column(db.Float)
    capacidade_reuso_m3_edificio = db.Column(db.Float)
    agua_de_reuso = db.Column(db.Boolean, default=False)
    status_do_registro = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    area_umida = db.relationship('AreaUmida', backref='area_umida')
    populacao = db.relationship('Populacao', backref='populacao')
    hidrometros = db.relationship('Hidrometros', backref='hidrometros')
    reservatorio = db.relationship(
        'Reservatorios',
        back_populates="edificio",
        secondary="main.reservatorio_edificio"
    )

    def update(self, **kwargs):

        for key, value in kwargs.items():
            setattr(self, key, value)

    def update_principal(self):
        print(self.id)
        escola_principal = Edificios.query.filter(
            Edificios.fk_escola == self.fk_escola, Edificios.principal == True).first()
        print(escola_principal.fk_escola)
        if escola_principal:
            escola_principal.principal = False
            self.principal = True  # Correção aqui
            db.session.commit()

            return self.to_json()
        else:
            return {}

    def __init__(self, fk_escola, numero_edificio, nome_do_edificio, cnpj_edificio, logradouro_edificio, cep_edificio=None, bairro_edificio=None, complemento_edificio=None, cidade_edificio=None, estado_edificio=None, agua_de_reuso=False, capacidade_reuso_m3_edificio=None, pavimentos_edificio=None, area_total_edificio=None, principal=False):

        self.fk_escola = fk_escola
        self.numero_edificio = numero_edificio
        self.bairro_edificio = bairro_edificio
        self.nome_do_edificio = nome_do_edificio
        self.cep_edificio = cep_edificio
        self.cnpj_edificio = cnpj_edificio
        self.logradouro_edificio = logradouro_edificio
        self.bairro_edificio = bairro_edificio
        self.estado_edificio = estado_edificio
        self.cidade_edificio = cidade_edificio
        self.complemento_edificio = complemento_edificio
        self.pavimentos_edificio = pavimentos_edificio
        self.area_total_edificio = area_total_edificio
        self.capacidade_reuso_m3_edificio = capacidade_reuso_m3_edificio if isinstance(
            capacidade_reuso_m3_edificio, int) else 0
        self.agua_de_reuso = agua_de_reuso

        # PRINCIPAL
        verificar = self.query.filter_by(fk_escola=self.fk_escola).count()
        if verificar == 0:
            self.principal = True
        else:
            self.principal = False

    def to_json(self):
        jsonRetorn = {}

        jsonRetorn.update({attr.name: getattr(self, attr.name)
                          for attr in self.__table__.columns})
        jsonRetorn.update({'reservatorio': [
                          reservatorios.nome_do_reservatorio for reservatorios in self.reservatorio]})
        return jsonRetorn


class Populacao(db.Model):

    __versioned__ = {}
    __table_args__ = {'schema': 'main'}
    __tablename__ = 'populacao'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fk_edificios = db.Column(db.Integer, db.ForeignKey('main.edificios.id'))
    fk_niveis = db.Column(db.Integer, db.ForeignKey('main.aux_opniveis.id'))
    fk_periodo = db.Column(db.Integer, db.ForeignKey(
        'main.aux_populacao_periodos.id'))
    funcionarios = db.Column(db.Integer)
    alunos = db.Column(db.Integer)
    status_do_registro = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())

    populacao_periodos = db.relationship(
        'AuxPopulacaoPeriodo', backref='populacao_periodos')
    opniveis = db.relationship('AuxOpNiveis', backref='opniveis')
    # hidrometros = db.relationship('Hidrometros', backref='hidrometros')

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __init__(self, fk_edificios, fk_niveis, fk_periodo, funcionarios, alunos):
        self.fk_edificios = fk_edificios
        self.fk_niveis = fk_niveis
        self.fk_periodo = fk_periodo
        self.funcionarios = funcionarios
        self.alunos = alunos

    def to_json(self):

        jsonRetorno = {}
        jsonRetorno['id'] = self.id
        jsonRetorno['periodo'] = self.populacao_periodos.periodo if self.populacao_periodos else None
        jsonRetorno['nivel'] = self.opniveis.nivel
        jsonRetorno['alunos'] = self.alunos
        jsonRetorno['funcionarios'] = self.funcionarios
        jsonRetorno['status_do_registro'] = self.status_do_registro

        # {attr.name: getattr(self, attr.name) for attr in self.__table__.columns}
        return jsonRetorno


class Hidrometros(db.Model):

    __versioned__ = {}
    __table_args__ = {'schema': 'main'}
    __tablename__ = 'hidrometros'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fk_edificios = db.Column(db.Integer, db.ForeignKey('main.edificios.id'))
    fk_hidrometro = db.Column(
        db.Integer, db.ForeignKey('main.aux_tipo_hidrometros.id'), default=1)
    status_do_registro = db.Column(db.Boolean, default=True)
    hidrometro = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    tipo_hidrometros = db.relationship(
        'AuxTipoHidrometro', backref='tipo_hidrometros')

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __init__(self, fk_edificios, hidrometro, fk_hidrometro=1):
        self.fk_edificios = fk_edificios
        self.hidrometro = hidrometro
        self.fk_hidrometro = fk_hidrometro

    def to_json(self):
        return {attr.name: getattr(self, attr.name) for attr in self.__table__.columns}


class AreaUmida(db.Model):

    __versioned__ = {}
    __table_args__ = {'schema': 'main'}
    __tablename__ = 'area_umida'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fk_edificios = db.Column(db.Integer, db.ForeignKey('main.edificios.id'))
    tipo_area_umida = db.Column(
        db.Integer, db.ForeignKey('main.aux_tipo_area_umida.id'))
    status_area_umida = db.Column(db.Boolean, default=True)
    operacao_area_umida = db.Column(
        db.Integer, db.ForeignKey('main.aux_operacao_area_umida.id')
    )
    nome_area_umida = db.Column(db.String)
    localizacao_area_umida = db.Column(db.String)
    status_do_registro = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    equipamentos = db.relationship('Equipamentos', backref='equipamentos')
    tipo_area_umida_rel = db.relationship(
        'AuxTipoAreaUmida', backref='aux_tipo_area_umida')
    operacao_area_umida_rel = db.relationship(
        'AuxOperacaoAreaUmida', backref='aux_operacao_area_umida'
    )

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __init__(self, fk_edificios, tipo_area_umida, nome_area_umida, localizacao_area_umida=None, status_area_umida=True, operacao_area_umida=4):

        self.fk_edificios = fk_edificios
        self.tipo_area_umida = tipo_area_umida
        self.nome_area_umida = nome_area_umida
        self.localizacao_area_umida = localizacao_area_umida
        self.status_area_umida = status_area_umida
        self.operacao_area_umida = operacao_area_umida

    def to_json(self):

        area_umida_descricao = self.tipo_area_umida_rel.tipo if self.tipo_area_umida_rel else None
        operacao = self.operacao_area_umida_rel.operacao if self.operacao_area_umida_rel else None

        jsonRetorno = {attr.name: getattr(self, attr.name)
                       for attr in self.__table__.columns}
        jsonRetorno['tipo_area_umida'] = area_umida_descricao
        jsonRetorno['operacao_area_umida'] = operacao
        # jsonRetorno['status_area_umida'] = status_area_umida
        return jsonRetorno


class Equipamentos(db.Model):

    __versioned__ = {}
    __table_args__ = {'schema': 'main'}
    __tablename__ = 'equipamentos'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fk_area_umida = db.Column(db.Integer, db.ForeignKey('main.area_umida.id'))
    tipo_equipamento = db.Column(
        db.Integer, db.ForeignKey('main.aux_tipo_equipamentos.id'))
    quantTotal = db.Column(db.Integer)
    quantProblema = db.Column(db.Integer)
    quantInutil = db.Column(db.Integer)
    status_do_registro = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    tipo_equipamento_rel = db.relationship(
        'AuxTiposEquipamentos', backref='main.aux_tipo_equipamentos.id')

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __init__(self, fk_area_umida, tipo_equipamento, quantTotal, quantProblema=0, quantInutil=0):

        self.fk_area_umida = fk_area_umida
        self.tipo_equipamento = tipo_equipamento
        self.quantTotal = int(quantTotal)
        self.quantProblema = int(
            quantProblema) if quantProblema != '' and quantProblema is not None else 0
        self.quantInutil = int(
            quantInutil) if quantInutil != '' and quantInutil is not None else 0

    def to_json(self):
        tipo_equipamento = self.tipo_equipamento_rel.aparelho_sanitario if self.tipo_equipamento_rel else None

        jsonRetorno = {attr.name: getattr(self, attr.name)
                       for attr in self.__table__.columns}
        jsonRetorno['tipo_equipamento'] = tipo_equipamento
        return jsonRetorno

# Tabela auxiliar


class Customizados(db.Model):
    __table_args__ = {'schema': 'main'}
    __tablename__ = 'aux_customizado_cliente'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    nivel_escola = db.Column(db.String)
    tipo_area_umida = db.Column(db.String)
    status_area_umida = db.Column(db.String)
    tipo_equipamento = db.Column(db.String)
    descricao_equipamento = db.Column(db.String)
    periodo_populacao = db.Column(db.String)

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __init__(self, nivel_escola, tipo_area_umida, status_area_umida, tipo_equipamento, descricao_equipamento, periodo_populacao):
        self.nivel_escola = nivel_escola
        self.tipo_area_umida = tipo_area_umida
        self.status_area_umida = status_area_umida
        self.tipo_equipamento = tipo_equipamento
        self.descricao_equipamento = descricao_equipamento
        self.periodo_populacao = periodo_populacao

    def to_json(self):
        return {attr.name: getattr(self, attr.name) for attr in self.__table__.columns}

# USUARIOS


class Usuarios(db.Model):

    __versioned__ = {}
    __table_args__ = {'schema': 'main'}
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    nome = db.Column(db.String, nullable=False),
    email = db.Column(db.String, nullable=False, unique=True)
    senha = db.Column(db.String(126), nullable=False)
    cod_cliente = db.Column(db.Integer,  db.ForeignKey('main.cliente.id'))
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __init__(self, email, cod_cliente, senha, nome):
        self.email = email
        self.senha = senha
        self.cod_cliente = cod_cliente
        self.nome = nome

    def to_json(self):
        return {attr.name: getattr(self, attr.name) for attr in self.__table__.columns}

# TABELAS DE OPÇÕES


class PopulacaoNiveis(db.Model):

    __versioned__ = {}
    __table_args__ = {'schema': 'main'}
    __tablename__ = 'populacao_niveis'

    populacao_id = db.Column(db.Integer, db.ForeignKey(
        'main.populacao.id'), primary_key=True)
    nivel_escola_id = db.Column(db.Integer, db.ForeignKey(
        'main.aux_opniveis.id'), primary_key=True)


class AuxPopulacaoPeriodo(db.Model):
    __table_args__ = {'schema': 'main'}
    __tablename__ = 'aux_populacao_periodos'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    periodo = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())

    def __init__(self, periodo):
        self.periodo = periodo

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def to_json(self):
        return {attr.name: getattr(self, attr.name) for attr in self.__table__.columns}


class AuxTipoAreaUmida(db.Model):

    __table_args__ = {'schema': 'main'}
    __tablename__ = 'aux_tipo_area_umida'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    tipo = db.Column(db.String, nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())

    def __init__(self, tipo):
        self.tipo = tipo

    def to_json(self):
        return {attr.name: getattr(self, attr.name) for attr in self.__table__.columns}

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class AuxOperacaoAreaUmida(db.Model):

    __table_args__ = {'schema': 'main'}
    __tablename__ = 'aux_operacao_area_umida'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    operacao = db.Column(db.String, nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())

    def __init__(self, operacao):
        self.operacao = operacao

    def to_json(self):
        return {attr.name: getattr(self, attr.name) for attr in self.__table__.columns}

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class AuxOpNiveis(db.Model):
    __table_args__ = {'schema': 'main'}
    __tablename__ = 'aux_opniveis'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    nivel = db.Column(db.String, nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())

    def __init__(self, nivel):
        self.nivel = nivel

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def to_json(self):
        return {attr.name: getattr(self, attr.name) for attr in self.__table__.columns}


class AuxTiposEquipamentos(db.Model):

    __table_args__ = {'schema': 'main'}
    __tablename__ = 'aux_tipo_equipamentos'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    aparelho_sanitario = db.Column(db.String, nullable=False)
    vazao = db.Column(db.Float)
    peso = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __init__(self, aparelho_sanitario, peso, vazao):
        self.aparelho_sanitario = aparelho_sanitario
        self.vazao = vazao
        self.peso = peso

    def to_json(self):
        return {attr.name: getattr(self, attr.name) for attr in self.__table__.columns}


class AuxTipoHidrometro(db.Model):
    __table_args__ = {'schema': 'main'}
    __tablename__ = 'aux_tipo_hidrometros'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    tipo_hidrometro = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())

    def __init__(self, tipo_hidrometro):
        self.tipo_hidrometro = tipo_hidrometro

    def to_json(self):
        return {attr.name: getattr(self, attr.name) for attr in self.__table__.columns}


# Tabelas auxiliares MxM
class EscolaNiveis(db.Model):

    __versioned__ = {}
    __table_args__ = {'schema': 'main'}
    __tablename__ = 'escola_niveis'

    escola_id = db.Column(db.Integer, db.ForeignKey(
        'main.escolas.id'), primary_key=True)
    nivel_ensino_id = db.Column(db.Integer, db.ForeignKey(
        'main.aux_opniveis.id'), primary_key=True)


class ReservatorioEdificio(db.Model):

    __versioned__ = {}
    # esta podendo ter nomes de reservatorios iguais para o mesmo edificio
    __table_args__ = {'schema': 'main'}
    __tablename__ = 'reservatorio_edificio'

    edificio_id = db.Column(db.Integer, db.ForeignKey(
        'main.edificios.id'), primary_key=True)
    reservatorio_id = db.Column(db.Integer, db.ForeignKey(
        'main.reservatorios.id'), primary_key=True)


class AuxTipoDeAreaUmidaTipoDeEquipamento(db.Model):
    __table_args__ = {'schema': 'main'}
    __tablename__ = 'aux_area_umida_equipamento'

    tipo_equipamento_id = db.Column(db.Integer, db.ForeignKey(
        'main.aux_tipo_equipamentos.id'), primary_key=True)
    tipo_area_umida_id = db.Column(db.Integer, db.ForeignKey(
        'main.aux_tipo_area_umida.id'), primary_key=True)

    tipo_equipamento_string = db.relationship(
        'AuxTiposEquipamentos',
        backref='tipo_equipamentos'
    )

    def __init__(self, tipo_equipamento_id, tipo_area_umida_id):
        self.tipo_equipamento_id = tipo_equipamento_id
        self.tipo_area_umida_id = tipo_area_umida_id

    def to_json(self):
        tipo = self.tipo_equipamento_string.aparelho_sanitario
        jsonEnviar = {}

        jsonEnviar['tipo'] = tipo
        jsonEnviar['equipamento_id'] = self.tipo_equipamento_id
        return jsonEnviar


# EVENTOS
class Eventos(db.Model):

    __versioned__ = {}
    __table_args__ = {"schema": "main"}
    __tablename__ = 'eventos'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fk_tipo = db.Column(db.Integer, db.ForeignKey(
        'main.aux_tipo_de_eventos.id'))
    nome = db.Column(db.String)
    datainicio = db.Column(db.DateTime)
    datafim = db.Column(db.DateTime)
    local = db.Column(db.Integer)  # 200
    tipo_de_local = db.Column(db.Integer, db.ForeignKey(
        'main.aux_de_locais.id'))  # 3
    observacao = db.Column(db.Text)

    tipodeevento = db.relationship(
        'AuxTipoDeEventos', backref='tipodeevento')
    tipodelocal = db.relationship(
        'AuxDeLocais', backref='tipodelocal'
    )

    created_at = db.Column(db.DateTime, default=datetime.now())

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __init__(self, fk_tipo, nome, datainicio, datafim, local, tipo_de_local, observacao):  # cod_usuarios
        self.fk_tipo = fk_tipo
        self.nome = nome
        self.datainicio = datainicio
        self.datafim = datafim
        self.local = local
        self.tipo_de_local = tipo_de_local
        self.observacao = observacao

    def to_json(self):

        colors = {
            "verde": "#9cb56e",
            "rosa": "#d57272",
            "azul": "#99C8E9",
            "roxo": "#BCA2E1",
            "amarelo": "#FEE57F",
            "laranja": "#F27B37"
        }
        retorno = {
            attr.name: colors[getattr(self, attr.name)] if attr.name == "color" and getattr(self, attr.name) in colors else
            getattr(self, attr.name)
            for attr in self.__table__.columns
        }
        
        retorno['tipodoevento'] = self.tipodeevento.recorrente
        retorno['fk_tipo'] = self.tipodeevento.nome_do_tipo_de_evento
        retorno['tipo_de_local'] = self.tipodelocal.nome_da_tabela
        retorno['datafim'] = self.datafim.strftime("%Y-%m-%d")
        retorno['datainicio'] = self.datainicio.strftime("%Y-%m-%d")
        
        
        if self.tipodelocal.nome_da_tabela == "Escola":
            retorno['local'] = Escolas.query.filter_by(id =self.local).first().nome
        elif self.tipodelocal.nome_da_tabela == "Edificação":
            retorno['local'] = Edificios.query.filter_by(id =self.local).first().nome_do_edificio
        elif self.tipodelocal.nome_da_tabela == "Área Úmida":
            retorno['local'] = AreaUmida.query.filter_by(id =self.local).first().nome_area_umida
        elif self.tipodelocal.nome_da_tabela == "Reservatório":
            retorno['local'] = Reservatorios.query.filter_by(id =self.local).first().nome_do_reservatorio
        elif self.tipodelocal.nome_da_tabela == "Hidrômetro":
            retorno['local'] = Hidrometros.query.filter_by(id =self.local).first().hidrometro
        else:
            retorno['local'] = ""

        return retorno

    def retornoFullCalendar(self):
    
        calendar = {
            "id": self.id,
            "title": self.nome,
            "start": str(self.datainicio).format("%d/%m/%Y"),
            "end": str(self.datafim).format("%d/%m/%Y"),
            "color": self.tipodeevento.color,
            "recorrente":self.tipodeevento.recorrente
        }

        return calendar


class AuxDeLocais(db.Model):

    __table_args__ = {"schema": "main"}
    __tablename__ = 'aux_de_locais'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    nome_da_tabela = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __init__(self, nome_da_tabela):

        self.nome_da_tabela = nome_da_tabela

    def to_json(self):
        return {attr.name: getattr(self, attr.name) for attr in self.__table__.columns}


class AuxTipoDeEventos(db.Model):
    __table_args__ = {"schema": "main"}
    __tablename__ = 'aux_tipo_de_eventos'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fk_cliente = db.Column(db.Integer, db.ForeignKey("main.cliente.id"))
    nome_do_tipo_de_evento = db.Column(db.String)
    recorrente = db.Column(db.Boolean)
    dia = db.Column(db.Integer)
    mes = db.Column(db.Integer)
    requer_acao = db.Column(db.Boolean)
    tempo = db.Column(db.Integer)
    unidade = db.Column(db.String)
    acao = db.Column(db.Boolean)
    usuario = db.Column(db.Integer,  db.ForeignKey('main.usuarios.id'))
    color = db.Column(db.String)
    status_do_registro = db.Column(db.Boolean, default=True)
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    created_at = db.Column(db.DateTime, default=datetime.now())

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __init__(self, fk_cliente=None, nome_do_tipo_de_evento=None, recorrente=None, dia=None, mes=None, requer_acao=None, tempo=None, unidade=None, acao=None, color=None):

        self.fk_cliente = fk_cliente
        self.nome_do_tipo_de_evento = nome_do_tipo_de_evento
        self.recorrente = recorrente
        self.dia = dia
        self.mes = mes
        self.requer_acao = requer_acao
        self.tempo = tempo
        self.unidade = unidade
        self.acao = acao
        self.color = color

    def to_json(self):
        meses_dict = {
            1: "Janeiro",
            2: "Fevereiro",
            3: "Março",
            4: "Abril",
            5: "Maio",
            6: "Junho",
            7: "Julho",
            8: "Agosto",
            9: "Setembro",
            10: "Outubro",
            11: "Novembro",
            12: "Dezembro"
        }

        return {
            attr.name: meses_dict[getattr(self, attr.name)] if attr.name == "mes" and getattr(self, attr.name) in meses_dict else
            getattr(self, attr.name)
            for attr in self.__table__.columns
        }


def add_opniveis():
    op_nome_da_tabela = ['Escola', 'Edificação', 'Área Úmida',
                         'Reservatório', 'Equipamento', 'Hidrômetro']
    opniveis = ['Médio', 'Superior', 'Fundamental', 'CEU', 'Berçario', 'EJA']
    tipoareaumida = ['Banheiro', 'Cozinha', 'Lavanderia',
                     'Piscina', 'Jardim', 'Areas Umida Comum']
    operacaoareaumida = ['Fechado', 'Em Manutenção',
                         'Parcialmente funcionando', 'Aberto']

    tipohidrometro = ['Tipo A', 'Tipo B', 'Tipo C', 'Pulsada', 'Normal']
    populacao_periodos = ['Manhã', 'Tarde', 'Noite', 'Integral']
    tipoequipamento = {
        "tipoequipamento": [
            {
                "aparelho_sanitario": "Bacia sanitária Caixa de descarga",
                "vazao": 0.15,
                "peso": 0.3
            },
            {
                "aparelho_sanitario": "Bacia sanitária Válvula de descarga",
                "vazao": 1.7,
                "peso": 32
            },
            {
                "aparelho_sanitario": "Banheira",
                "vazao": 0.3,
                "peso": 1
            },
            {
                "aparelho_sanitario": "Bebedouro",
                "vazao": 0.1,
                "peso": 0.1
            },
            {
                "aparelho_sanitario": "Bidê",
                "vazao": 0.1,
                "peso": 0.1
            },
            {
                "aparelho_sanitario": "Chuveiro ou ducha",
                "vazao": 0.2,
                "peso": 0.4
            },
            {
                "aparelho_sanitario": "Chuveiro elétrico",
                "vazao": 0.1,
                "peso": 0.1
            },
            {
                "aparelho_sanitario": "Lavadora de pratos ou de roupas",
                "vazao": 0.3,
                "peso": 1
            },
            {
                "aparelho_sanitario": "Lavatório",
                "vazao": 0.15,
                "peso": 0.3
            },
            {
                "aparelho_sanitario": "Mictório cerâmico Válvula de descarga",
                "vazao": 0.5,
                "peso": 2.8
            },
            {
                "aparelho_sanitario": "Mictório Caixa de descarga, registro de pressão ou válvula de descarga para mictório",
                "vazao": 0.15,
                "peso": 0.3
            },
            {
                "aparelho_sanitario": "Mictório tipo calha",
                "vazao": "0.15",
                "peso": 0.3
            },
            {
                "aparelho_sanitario": "Pia Torneira Gás",
                "vazao": 0.25,
                "peso": 0.7
            },
            {
                "aparelho_sanitario": "Pia Toneira (Elétrica)",
                "vazao": 0.1,
                "peso": 0.1
            },
            {
                "aparelho_sanitario": "Tanque",
                "vazao": 0.25,
                "peso": 0.7
            },
            {
                "aparelho_sanitario": "Torneira de jardim ou lavagem em geral",
                "vazao": 0.2,
                "peso": 0.4
            }
        ]
    }
    tipoareaumidaequipamento = {
        "Banheiro": [
            "Bacia sanitária Caixa de descarga",
            "Bacia sanitária Válvula de descarga",
            "Chuveiro ou ducha",
            "Chuveiro elétrico",
            "Mictório Caixa de descarga, registro de pressão ou válvula de descarga para mictório",
            "Mictório cerâmico Válvula de descarga",
            "Mictório tipo calha",
            "Torneira de jardim ou lavagem em geral",
            "Banheira",
            "Bidê"
        ],
        "Cozinha": [
            "Pia Torneira Gás",
            "Pia Toneira (Elétrica)",
            "Torneira de jardim ou lavagem em geral",
            "Lavadora de pratos ou de roupas",
            "Tanque",
            "Bebedouro"
        ],
        "Piscina": [
            "Banheira",
            "Bidê",
            "Chuveiro ou ducha",
            "Chuveiro elétrico",
            "Mictório Caixa de descarga, registro de pressão ou válvula de descarga para mictório",
            "Lavatório",
            "Mictório tipo calha",
            "Tanque",
            "Torneira de jardim ou lavagem em geral",
            "Bacia sanitária Caixa de descarga",
            "Bacia sanitária Válvulade descarga"
        ],
        "Lavanderia": [
            "Tanque",
            "Lavadora de pratos ou de roupas",
            "Pia Torneira Gás",
            "Pia Toneira (Elétrica)",
            "Torneira de jardim ou lavagem em geral"
        ],
        "Areas Umida Comum": [
            "Pia Torneira Gás",
            "Pia Toneira (Elétrica)",
            "Tanque",
            "Bebedouro"
        ]
    }

    for nome_da_tabela in op_nome_da_tabela:
        opnome = AuxDeLocais.query.filter_by(
            nome_da_tabela=nome_da_tabela).first()
        if not opnome:
            opnome = AuxDeLocais(nome_da_tabela=nome_da_tabela)
            db.session.add(opnome)

    for nivel in opniveis:
        opnivel = AuxOpNiveis.query.filter_by(nivel=nivel).first()
        if not opnivel:
            opnivel = AuxOpNiveis(nivel=nivel)
            db.session.add(opnivel)

    for areaumida in tipoareaumida:
        tipo = AuxTipoAreaUmida.query.filter_by(tipo=areaumida).first()
        if not tipo:
            tipo = AuxTipoAreaUmida(tipo=areaumida)
            db.session.add(tipo)

    for operacao in operacaoareaumida:
        st = AuxOperacaoAreaUmida.query.filter_by(operacao=operacao).first()

        if not st:
            st = AuxOperacaoAreaUmida(operacao=operacao)
            db.session.add(st)

    for hidrometro in tipohidrometro:
        hid = AuxTipoHidrometro.query.filter_by(
            tipo_hidrometro=hidrometro).first()

        if not hid:
            hid = AuxTipoHidrometro(tipo_hidrometro=hidrometro)
            db.session.add(hid)

    for periodo in populacao_periodos:
        operiodo = AuxPopulacaoPeriodo.query.filter_by(periodo=periodo).first()
        if not operiodo:
            operiodo = AuxPopulacaoPeriodo(periodo=periodo)
            db.session.add(operiodo)

    for equipamento in tipoequipamento['tipoequipamento']:
        oequipamento = AuxTiposEquipamentos.query.filter_by(
            aparelho_sanitario=equipamento['aparelho_sanitario']).first()

        if not oequipamento:
            oequipamento = AuxTiposEquipamentos(
                aparelho_sanitario=equipamento['aparelho_sanitario'],
                vazao=equipamento['vazao'],
                peso=equipamento['peso']
            )
            db.session.add(oequipamento)

    db.session.commit()

    for key, values in tipoareaumidaequipamento.items():
        idarea = AuxTipoAreaUmida.query.filter_by(tipo=key).first()
        if idarea:
            idarea = idarea.id

            for value in values:
                idEquipamento = AuxTiposEquipamentos.query.filter_by(
                    aparelho_sanitario=value).first()
                if idEquipamento:
                    idEquipamento = idEquipamento.id

                    query = AuxTipoDeAreaUmidaTipoDeEquipamento.query.filter_by(
                        tipo_equipamento_id=idEquipamento,
                        tipo_area_umida_id=idarea
                    )

                    if not query.first():
                        areaumidaequipamento = AuxTipoDeAreaUmidaTipoDeEquipamento(
                            tipo_equipamento_id=idEquipamento, tipo_area_umida_id=idarea)
                        db.session.add(areaumidaequipamento)

            db.session.commit()


sa.orm.configure_mappers()
