from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from datetime import datetime
from sqlalchemy import inspect
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy.orm.collections as col




db = SQLAlchemy()


# EVENTOS
class Eventos(db.Model):
    __table_args__ = {"schema":"main"}
    __tablename__ = 'eventos'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fk_tipo = db.Column(db.Integer, db.ForeignKey('main.tipo_de_eventos.id'))
    nome = db.Column(db.String)
    datainicio = db.Column(db.DateTime)
    datafim = db.Column(db.DateTime, default=None)
    prioridade = db.Column(db.Integer, db.ForeignKey('main.prioridade_eventos.id'))
    local = db.Column(db.Integer) # 200
    tipo_de_local = db.Column(db.Integer, db.ForeignKey('main.tabela_de_locais.id')) # 3
    observacao = db.Column(db.Text)
    #usuarios = db.relationship('Usuarios', backref='usuarios')
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __init__(self, fk_tipo, nome, datainicio, datafim, prioridade, local, tipo_de_local, observacao):
        self.fk_tipo = fk_tipo
        self.nome = nome
        self.datainicio = datainicio
        self.datafim = datafim
        self.prioridade = prioridade
        self.local = local
        self.tipo_de_local = tipo_de_local
        self.observacao = observacao

    def to_json(self):
        return {attr.name: getattr(self, attr.name) for attr in self.__table__.columns}


class TabelasDeLocais(db.Model):
    __table_args__ = {"schema":"main"}
    __tablename__ = 'tabela_de_locais'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    nome_da_tabela = db.Column(db.String)       

    def update(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)

    def __init__(self, nome_da_tabela):
        self.nome_da_tabela = nome_da_tabela
        

    def to_json(self):
        return {attr.name: getattr(self, attr.name) for attr in self.__table__.columns}
    
    
    
class PrioridadeEventos(db.Model):
    __table_args__ = {"schema":"main"}
    __tablename__ = 'prioridade_eventos'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    prioridade = db.Column(db.String)

    def update(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)

    def __init__(self, prioridade ):
        self.prioridade = prioridade
        
    def to_json(self):
        return {attr.name: getattr(self, attr.name) for attr in self.__table__.columns}
    


class TipoDeEventos(db.Model):
    __table_args__ = {"schema":"main"}
    __tablename__ = 'tipo_de_eventos'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    nome_do_evento = db.Column(db.String)
    periodicidade = db.Column(db.String)
    sazonal_periodo = db.Column(db.Date, default=None)
    requer_resposta = db.Column(db.Boolean, default=False) 
    tempo_de_tolerancia = db.Column(db.Integer)
    unidade_de_tempo = db.Column(db.String)
    e_resposta = db.Column(db.Boolean, default=False)
    resposta_para = db.Column(db.String)
   
    def update(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)

    def __init__(self, nome_do_evento, periodicidade, sazonal_periodo, requer_resposta, tempo_de_tolerancia, unidade_de_tempo, e_resposta, resposta_para ):
        self.nome_do_evento = nome_do_evento
        self.periodicidade = periodicidade
        self.sazonal_periodo =  sazonal_periodo
        self.requer_resposta = requer_resposta
        self.tempo_de_tolerancia = tempo_de_tolerancia
        self.unidade_de_tempo = unidade_de_tempo
        self.e_resposta = e_resposta
        self.resposta_para = resposta_para
        

    def to_json(self):
        return {attr.name: getattr(self, attr.name) for attr in self.__table__.columns}




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


#Historico geral
class Historico(db.Model):
    __table_args__ = {'schema': 'main'}
    __tablename__ = 'historico'

    id = db.Column(db.Integer, primary_key=True)
    tabela = db.Column(db.String, nullable=False)
    dados = db.Column(db.JSON, nullable=False)
    data_alteracao = db.Column(db.DateTime, default=datetime.now)

    def to_json(self):
        return {attr.name: getattr(self, attr.name) for attr in self.__table__.columns}



class Escolas(db.Model):

    __table_args__ = {'schema': 'main'}
    __tablename__ = 'escolas'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    nome = db.Column(db.String)  # 255
    cnpj = db.Column(db.String)  # 18
    email = db.Column(db.String)  # 55
    telefone = db.Column(db.String(16))  # 16
    status_do_registro = db.Column(db.Boolean, default=True)
    edificios = db.relationship('Edificios', backref='edificios')
    escolas_historico = db.relationship(
        'EscolasHistorico', backref='escolas_historico')
    data_criacao = db.Column(db.DateTime, server_default=func.now())

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


class EscolasHistorico(db.Model):
    __table_args__ = {'schema': 'main'}
    __tablename__ = 'escolas_historico'

    id = db.Column(db.Integer, primary_key=True)
    fk_escola = db.Column(db.Integer, db.ForeignKey('main.escolas.id'))
    cnpj = db.Column(db.String)  # 18
    nivel = db.Column(db.JSON(db.String))
    data_alteracao = db.Column(db.DateTime, default=datetime.now)



class Reservatorios(db.Model):
    __table_args__ = {'schema': 'main'}
    __tablename__ = 'reservatorios'

    id: db.Mapped[int] = db.mapped_column(
        db.Integer, autoincrement=True, primary_key=True)
    fk_escola = db.Column(db.Integer, db.ForeignKey('main.escolas.id'))
    nome_do_reservatorio = db.Column(db.String, nullable=False)
    status_do_registro = db.Column(db.Boolean, default=True)
    edificio = db.relationship(
        'Edificios',
        back_populates="reservatorio",
        secondary="main.reservatorio_edificio"
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

    '''__table_args__ = (db.UniqueConstraint('nome_do_edificio', 'fk_escola', name='nome_edifico_unico'),
                      # cria unicidade das combinações chave e coluna
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
    bairro_edificio = db.Column(db.String)
    complemento_edificio = db.Column(db.String)
    pavimentos_edificio = db.Column(db.Integer)
    area_total_edificio = db.Column(db.Float)
    capacidade_reuso_m3_edificio = db.Column(db.Float)
    agua_de_reuso = db.Column(db.Boolean, default=False)
    status_do_registro = db.Column(db.Boolean, default=True)
    data_criacao = db.Column(db.DateTime, server_default=func.now())
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
            if key == 'principal':
                verificar = self.query.filter_by(fk_escola=self.fk_escola).count()
                if verificar == 1:
                    self.principal = True
                else:
                    if value:
                        edificioprincipal = self.query.filter_by(principal=True).first()
                        if edificioprincipal is not None:
                            edificioprincipal.principal = False  # Corrigido aqui
                        self.principal = True
                    else:
                        edificios = self.query.filter_by(id = self.id).first()
                        if edificios.principal:
                            self.principal = True
                        else:
                            self.principal = False
    
            else:
                setattr(self, key, value)


    def __init__(self, fk_escola, numero_edificio, bairro_edificio, nome_do_edificio, cep_edificio, cnpj_edificio, logradouro_edificio, complemento_edificio, cidade_edificio, estado_edificio, agua_de_reuso=False, capacidade_reuso_m3_edificio=None, pavimentos_edificio=None, area_total_edificio=None, principal=False):

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
        self.capacidade_reuso_m3_edificio = capacidade_reuso_m3_edificio if isinstance(capacidade_reuso_m3_edificio, int) else 0
        self.agua_de_reuso = agua_de_reuso

        # PRINCIPAL
        verificar = self.query.filter_by(fk_escola=self.fk_escola).count()
        if verificar == 0:
            self.principal = True
        else:
            self.principal = False
                      


    def to_json(self):
        jsonRetorn = {}

        jsonRetorn.update({attr.name: getattr(self, attr.name) for attr in self.__table__.columns})
        jsonRetorn.update({'reservatorio': [reservatorios.nome_do_reservatorio for reservatorios in self.reservatorio]})
        return jsonRetorn


class Populacao(db.Model):
    __table_args__ = {'schema': 'main'}
    __tablename__ = 'populacao'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fk_edificios = db.Column(db.Integer, db.ForeignKey('main.edificios.id'))
    fk_niveis = db.Column(db.Integer, db.ForeignKey('main.opniveis.id'))
    fk_periodo = db.Column(db.Integer, db.ForeignKey(
        'main.populacao_periodos.id'))
    funcionarios = db.Column(db.Integer)
    alunos = db.Column(db.Integer)
    status_do_registro = db.Column(db.Boolean, default=True)
    data_criacao = db.Column(db.DateTime, server_default=func.now())

    populacao_periodos = db.relationship(
        'PopulacaoPeriodo', backref='populacao_periodos')
    opniveis = db.relationship('OpNiveis', backref='opniveis')
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

        # {attr.name: getattr(self, attr.name) for attr in self.__table__.columns}
        return jsonRetorno


class Hidrometros(db.Model):
    __table_args__ = {'schema': 'main'}
    __tablename__ = 'hidrometros'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fk_edificios = db.Column(db.Integer, db.ForeignKey('main.edificios.id'))
    fk_hidrometro = db.Column(
        db.Integer, db.ForeignKey('main.tipo_hidrometros.id'), default=1)
    status_do_registro = db.Column(db.Boolean, default=True)
    hidrometro = db.Column(db.String, nullable=False)
    data_criacao = db.Column(db.DateTime, server_default=func.now())
    tipo_hidrometros = db.relationship(
        'TipoHidrometro', backref='tipo_hidrometros')

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __init__(self, fk_edificios, hidrometro):
        self.fk_edificios = fk_edificios
        self.hidrometro = hidrometro

    def to_json(self):
        return {attr.name: getattr(self, attr.name) for attr in self.__table__.columns}


class AreaUmida(db.Model):

    __table_args__ = {'schema': 'main'}
    __tablename__ = 'area_umida'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fk_edificios = db.Column(db.Integer, db.ForeignKey('main.edificios.id'))
    tipo_area_umida = db.Column(
        db.Integer, db.ForeignKey('main.aux_tipo_area_umida.id'))
    status_area_umida = db.Column(db.Integer, db.ForeignKey('main.aux_status_area_umida.id'))
    operacao_area_umida = db.Column(
        db.Integer, db.ForeignKey('main.aux_operacao_area_umida.id')
    )
    nome_area_umida = db.Column(db.String)
    localizacao_area_umida = db.Column(db.String)
    status_do_registro = db.Column(db.Boolean, default=True)
    data_criacao = db.Column(db.DateTime, server_default=func.now())
    equipamentos = db.relationship('Equipamentos', backref='equipamentos')
    tipo_area_umida_rel = db.relationship(
        'TipoAreaUmida', backref='aux_tipo_area_umida')
    
    operacao_area_umida_rel = db.relationship(
        'OperacaoAreaUmida', backref = 'aux_operacao_area_umida'
    )

    status_area_umida_rel = db.relationship( 
        'StatusAreaUmida', backref='aux_status_area_umida'
    )

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __init__(self, fk_edificios, tipo_area_umida, operacao_area_umida, nome_area_umida, localizacao_area_umida, status_area_umida):

        self.fk_edificios = fk_edificios
        self.tipo_area_umida = tipo_area_umida
        self.nome_area_umida = nome_area_umida
        self.localizacao_area_umida = localizacao_area_umida
        self.status_area_umida = status_area_umida
        self.operacao_area_umida = operacao_area_umida

    def to_json(self):

        status_area_umida = self.status_area_umida_rel.status if self.status_area_umida_rel else None
        area_umida_descricao = self.tipo_area_umida_rel.tipo if self.tipo_area_umida_rel else None
        operacao = self.operacao_area_umida_rel.operacao if self.operacao_area_umida_rel else None

        jsonRetorno = {attr.name: getattr(self, attr.name)
                       for attr in self.__table__.columns}
        jsonRetorno['tipo_area_umida'] = area_umida_descricao
        jsonRetorno['operacao_area_umida'] = operacao
        jsonRetorno['status_area_umida'] = status_area_umida
        return jsonRetorno


class Equipamentos(db.Model):

    __table_args__ = {'schema': 'main'}
    __tablename__ = 'equipamentos'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fk_area_umida = db.Column(db.Integer, db.ForeignKey('main.area_umida.id'))
    tipo_equipamento = db.Column(
        db.Integer, db.ForeignKey('main.tipo_equipamentos.id'))
    quantTotal = db.Column(db.Integer)
    quantProblema = db.Column(db.Integer)
    quantInutil = db.Column(db.Integer)
    status_do_registro = db.Column(db.Boolean, default=True)
    data_criacao = db.Column(db.DateTime, server_default=func.now())
    tipo_equipamento_rel = db.relationship(
        'TiposEquipamentos', backref='main.tipo_equipamentos.id')

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __init__(self, fk_area_umida, tipo_equipamento, quantTotal, quantProblema, quantInutil):

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
    nivel_escola = db.Column(db.JSON(db.String))
    tipo_area_umida = db.Column(db.JSON(db.String))
    status_area_umida = db.Column(db.JSON(db.String))
    tipo_equipamento = db.Column(db.JSON(db.String))
    descricao_equipamento = db.Column(db.JSON(db.String))
    periodo_populacao = db.Column(db.JSON(db.String))

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
    __table_args__ = {'schema': 'main'}
    __tablename__ = 'populacao_niveis'

    populacao_id = db.Column(db.Integer, db.ForeignKey(
        'main.populacao.id'), primary_key=True)
    nivel_escola_id = db.Column(db.Integer, db.ForeignKey(
        'main.opniveis.id'), primary_key=True)


class PopulacaoPeriodo(db.Model):
    __table_args__ = {'schema': 'main'}
    __tablename__ = 'populacao_periodos'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    periodo = db.Column(db.String)

    def __init__(self, periodo):
        self.periodo = periodo

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def to_json(self):
        return {attr.name: getattr(self, attr.name) for attr in self.__table__.columns}


class TipoAreaUmida(db.Model):

    __table_args__ = {'schema': 'main'}
    __tablename__ = 'aux_tipo_area_umida'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    tipo = db.Column(db.String, nullable=False, unique=True)

    def __init__(self, tipo):
        self.tipo = tipo

    def to_json(self):
        return {attr.name: getattr(self, attr.name) for attr in self.__table__.columns}

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class StatusAreaUmida(db.Model):

    __table_args__ = {'schema': 'main'}
    __tablename__ = 'aux_status_area_umida'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    status = db.Column(db.String, nullable=False, unique=True)

    def __init__(self, status):
        self.status = status

    def to_json(self):
        return {attr.name: getattr(self, attr.name) for attr in self.__table__.columns}

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

class OperacaoAreaUmida(db.Model):

    __table_args__ = {'schema': 'main'}
    __tablename__ = 'aux_operacao_area_umida'

    id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    operacao = db.Column(db.String, nullable=False, unique=True)

    def __init__(self, operacao):
        self.operacao = operacao

    def to_json(self):
        return {attr.name: getattr(self, attr.name) for attr in self.__table__.columns}

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

  

class OpNiveis(db.Model):
    __table_args__ = {'schema': 'main'}
    __tablename__ = 'opniveis'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    nivel = db.Column(db.String, nullable=False, unique=True)

    def __init__(self, nivel):
        self.nivel = nivel

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def to_json(self):
        return {attr.name: getattr(self, attr.name) for attr in self.__table__.columns}


class TiposEquipamentos(db.Model):

    __table_args__ = {'schema': 'main'}
    __tablename__ = 'tipo_equipamentos'

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

class TipoHidrometro(db.Model):
    __table_args__ = {'schema': 'main'}
    __tablename__ = 'tipo_hidrometros'

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
    __table_args__ = {'schema': 'main'}
    __tablename__ = 'escola_niveis'

    escola_id = db.Column(db.Integer, db.ForeignKey(
        'main.escolas.id'), primary_key=True)
    nivel_ensino_id = db.Column(db.Integer, db.ForeignKey(
        'main.opniveis.id'), primary_key=True)


class ReservatorioEdificio(db.Model):

     #esta podendo ter nomes de reservatorios iguais para o mesmo edificio
    __table_args__ = {'schema': 'main'}
    __tablename__ = 'reservatorio_edificio'


    edificio_id = db.Column(db.Integer, db.ForeignKey(
        'main.edificios.id'), primary_key=True)
    reservatorio_id = db.Column(db.Integer, db.ForeignKey(
        'main.reservatorios.id'), primary_key=True)


class TipoDeAreaUmidaTipoDeEquipamento(db.Model):
    __table_args__ = {'schema': 'main'}
    __tablename__ = 'area_umida_equipamento'

    tipo_equipamento_id = db.Column(db.Integer, db.ForeignKey(
        'main.tipo_equipamentos.id'), primary_key=True)
    tipo_area_umida_id = db.Column(db.Integer, db.ForeignKey(
        'main.aux_tipo_area_umida.id'), primary_key=True)

    tipo_equipamento_string = db.relationship(
        'TiposEquipamentos',
        backref = 'tipo_equipamentos'
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


def add_opniveis():
    op_nome_da_tabela = ['Escola', 'Edificação','Área Umida', 'Reservatório', 'Equipamento', 'Hidrômetro']
    op_unidade_de_tempo = ['Horas', 'Dias', 'Semanas', 'Meses']
    op_nome_do_evento = ['Férias', 'Festa', 'Manutenção']
    op_prioridade = ['Alta', 'Média', 'Baixa']

    opniveis = ['Médio', 'Superior', 'Fundamental', 'CEU', 'Berçario', 'EJA']
    tipoareaumida = ['Banheiro', 'Cozinha', 'Lavanderia',
                     'Piscina', 'Jardim', 'Areas Umida Comum']
    operacaoareaumida = ['Fechado', 'Em Manutenção', 'Parcialmente funcionando']
    status_area_umida = ['True', 'False']
    tipohidrometro = ['Tipo A', 'Tipo B', 'Tipo C']
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
        opnome = TabelasDeLocais.query.filter_by(nome_da_tabela=nome_da_tabela).first()
        if not opnome:
            opnome = TabelasDeLocais(nome_da_tabela=nome_da_tabela)
            db.session.add(opnome)

    for unidade_de_tempo in op_unidade_de_tempo:
            unidade_tempo = TipoDeEventos.query.filter_by(unidade_de_tempo=unidade_de_tempo).first()
            if not unidade_tempo:
                unidade_tempo = TipoDeEventos(unidade_de_tempo=unidade_de_tempo)
                db.session.add(unidade_tempo)

    for nome_do_evento in op_nome_do_evento:
        tipo_de_eventos = TipoDeEventos.query.filter_by(
            nome_do_evento=nome_do_evento).first()
        if not tipo_de_eventos:
            tipo_de_eventos = TipoDeEventos.query.filter_by(
            nome_do_evento=nome_do_evento)
            db.session.add(tipo_de_eventos)

    for prioridade in op_prioridade:
        prioridade_eventos = PrioridadeEventos.query.filter_by(prioridade=prioridade).first() 
        if not prioridade_eventos:
            prioridade_eventos = PrioridadeEventos(prioridade=prioridade)
            db.session.add(prioridade_eventos)
        
    for nivel in opniveis:
        opnivel = OpNiveis.query.filter_by(nivel=nivel).first()
        if not opnivel:
            opnivel = OpNiveis(nivel=nivel)
            db.session.add(opnivel)

    for areaumida in tipoareaumida:
        tipo = TipoAreaUmida.query.filter_by(tipo=areaumida).first()
        if not tipo:
            tipo = TipoAreaUmida(tipo=areaumida)
            db.session.add(tipo)

    for operacao in operacaoareaumida:
        st = OperacaoAreaUmida.query.filter_by(operacao=operacao).first()

        if not st:
            st = OperacaoAreaUmida(operacao=operacao)
            db.session.add(st)

    for status in status_area_umida:
        st = StatusAreaUmida.query.filter_by(status=status).first()

        if not st:
            st = StatusAreaUmida(status=status)
            db.session.add(st)

    for hidrometro in tipohidrometro:
        hid = TipoHidrometro.query.filter_by(
            tipo_hidrometro=hidrometro).first()

        if not hid:
            hid = TipoHidrometro(tipo_hidrometro=hidrometro)
            db.session.add(hid)

    for periodo in populacao_periodos:
        operiodo = PopulacaoPeriodo.query.filter_by(periodo=periodo).first()
        if not operiodo:
            operiodo = PopulacaoPeriodo(periodo=periodo)
            db.session.add(operiodo)

    for equipamento in tipoequipamento['tipoequipamento']:
        oequipamento = TiposEquipamentos.query.filter_by(
            aparelho_sanitario=equipamento['aparelho_sanitario']).first()

        if not oequipamento:
            oequipamento = TiposEquipamentos(
                aparelho_sanitario=equipamento['aparelho_sanitario'],
                vazao=equipamento['vazao'],
                peso=equipamento['peso']
            )
            db.session.add(oequipamento)

    db.session.commit()

    for key, values in tipoareaumidaequipamento.items():
        idarea = TipoAreaUmida.query.filter_by(tipo=key).first()
        if idarea:
            idarea = idarea.id

            for value in values:
                idEquipamento = TiposEquipamentos.query.filter_by(
                    aparelho_sanitario=value).first()
                if idEquipamento:
                    idEquipamento = idEquipamento.id

                    query = TipoDeAreaUmidaTipoDeEquipamento.query.filter_by(
                        tipo_equipamento_id=idEquipamento,
                        tipo_area_umida_id=idarea
                    )

                    if not query.first():
                        areaumidaequipamento = TipoDeAreaUmidaTipoDeEquipamento(
                            tipo_equipamento_id=idEquipamento, tipo_area_umida_id=idarea)
                        db.session.add(areaumidaequipamento)

            db.session.commit()