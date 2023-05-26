from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, UniqueConstraint, Index
from datetime import datetime


db = SQLAlchemy()


class Escolas(db.Model):

    __table_args__ = {'schema':'main'}
    __tablename__ = 'escolas'

    id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    nome = db.Column(db.String, nullable = False) #255
    cnpj = db.Column(db.String, unique=True, nullable=False) #18
    nivel = db.Column(db.JSON(db.String))
    email = db.Column(db.String, unique=True, nullable=False) #55
    telefone = db.Column(db.String(16)) #16
    status_do_registro = db.Column(db.Boolean, default=True)
    edificios = db.relationship('Edificios', backref = 'edificios')
    escolas_historico =  db.relationship('EscolasHistorico', backref = 'escolas_historico')
    data_criacao = db.Column(db.DateTime, server_default=func.now())

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __init__(self, nome, cnpj, nivel, email, telefone):
        self.nome = nome
        self.cnpj = cnpj
        self.nivel = nivel
        self.email = email
        self.telefone = telefone


    def to_json(self):
        return {attr.name: getattr(self, attr.name) for attr in self.__table__.columns}

   # def to_dict(self):
    #    d = {}
     #   for column in self.__table__.columns:
     #       if isinstance(column.type, db.DateTime):
     #           d[column.name] = getattr(self, column.name).strftime("%Y-%m-%dT%H:%M:%S")
      #      else:
       #         d[column.name] = getattr(self, column.name)
       # return d


class EscolasHistorico(db.Model):
    __table_args__ = {'schema':'main'}
    __tablename__ = 'escolas_historico'

    id = db.Column(db.Integer, primary_key=True)
    fk_escola = db.Column(db.Integer, db.ForeignKey('main.escolas.id'))
    cnpj = db.Column(db.String) #18
    nivel = db.Column(db.JSON(db.String))
    data_alteracao = db.Column(db.DateTime, default=datetime.now)


class Edificios(db.Model):

    __table_args__ = (db.UniqueConstraint('nome_do_edificio', 'fk_escola', name='nome_edifico_unico'),
                      db.Index('ix_edificio_nome_escola', 'nome_do_edificio', 'fk_escola', unique=True), #cria unicidade das combinações chave e coluna
                     {'schema': 'main'})
    __tablename__ = 'edificios'


    id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    fk_escola = db.Column(db.Integer, db.ForeignKey('main.escolas.id'))
    numero_edificio = db.Column(db.String)
    nome_do_edificio = db.Column(db.String, nullable=False)
    principal = db.Column(db.Boolean)
    cep_edificio = db.Column(db.String)
    bairro = db.Column(db.String)
    cidade_edificio = db.Column(db.String)
    estado_edificio = db.Column(db.String)
    cnpj_edificio = db.Column(db.String)
    logradouro_edificio = db.Column(db.String)
    #complemento = db.Column(db.String)
    pavimentos_edificio = db.Column(db.Integer)
    area_total_edificio = db.Column(db.Float)
    reservatorio = db.Column(db.Boolean)#padrao é False
    capacidade_m3_edificio = db.Column(db.Float) 
    agua_de_reuso = db.Column(db.Boolean)
    capacidade_reuso_m3_edificio= db.Column(db.Float)
    status_do_registro = db.Column(db.Boolean, default=True)
    data_criacao = db.Column(db.DateTime, server_default=func.now())
    area_umida = db.relationship('AreaUmida', backref = 'area_umida')
    populacao = db.relationship('Populacao', backref = 'populacao')
    hidrometros = db.relationship('Hidrometros', backref = 'hidrometros')

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __init__(self, fk_escola, numero_edificio, bairro, nome_do_edificio, cep_edificio, cnpj_edificio, logradouro_edificio, cidade_edificio, estado_edificio, pavimentos_edificio, area_total_edificio, capacidade_m3_edificio=0.0 , capacidade_reuso_m3_edificio=0.0, reservatorio=False, agua_de_reuso=False, principal=False):

        self.fk_escola = fk_escola
        self.numero_edificio = numero_edificio
        self.bairro = bairro
        self.nome_do_edificio = nome_do_edificio
        self.principal = principal
        self.cep_edificio = cep_edificio
        self.cnpj_edificio = cnpj_edificio
        self.logradouro_edificio = logradouro_edificio
        self.estado_edificio = estado_edificio
        self.cidade_edificio = cidade_edificio
        self.pavimentos_edificio = pavimentos_edificio
        self.area_total_edificio = area_total_edificio
        self.reservatorio = reservatorio
        self.capacidade_m3_edificio = capacidade_m3_edificio if reservatorio else None
        self.agua_de_reuso = agua_de_reuso
        self.capacidade_reuso_m3_edificio = capacidade_reuso_m3_edificio if agua_de_reuso else None

    def to_json(self):
        return {attr.name: getattr(self, attr.name) for attr in self.__table__.columns}

class Populacao(db.Model):
        __table_args__ = {'schema': 'main'}
        __tablename__ = 'populacao'

        id = db.Column(db.Integer, autoincrement=True, primary_key=True)
        fk_edificios = db.Column(db.Integer, db.ForeignKey('main.edificios.id'))
        nivel = db.Column(db.JSON(db.String))  # Mudança aqui
        periodo = db.Column(db.String)
        funcionarios = db.Column(db.Integer)
        alunos = db.Column(db.Integer)
        status_do_registro = db.Column(db.Boolean, default=True)
        data_criacao = db.Column(db.DateTime, server_default=func.now())


        def update(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)


        def __init__(self, fk_edificios, nivel, periodo, funcionarios, alunos):
            self.fk_edificios = fk_edificios
            self.nivel = nivel if isinstance(nivel, list) else [nivel]
            self.periodo = periodo
            self.funcionarios = funcionarios
            self.alunos = alunos

        def to_json(self):
            return {attr.name: getattr(self, attr.name) for attr in self.__table__.columns}


class Hidrometros(db.Model):
        __table_args__ = {'schema': 'main'}
        __tablename__ = 'hidrometros'

        id = db.Column(db.Integer, autoincrement=True, primary_key=True)
        fk_edificios = db.Column(db.Integer, db.ForeignKey('main.edificios.id'))
        hidrometro = db.Column(db.String)
        status_do_registro = db.Column(db.Boolean, default=True)
        data_criacao = db.Column(db.DateTime, server_default=func.now())


        def update(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)


        def __init__(self, fk_edificios, hidrometro ):
            self.fk_edificios = fk_edificios
            self.hidrometro = hidrometro

        def to_json(self):
            return {attr.name: getattr(self, attr.name) for attr in self.__table__.columns}


class AreaUmida(db.Model):

        __table_args__ = {'schema':'main'}
        __tablename__ = 'area_umida'

        id = db.Column(db.Integer, autoincrement = True, primary_key = True)
        fk_edificios = db.Column(db.Integer, db.ForeignKey('main.edificios.id'))
        tipo_area_umida = db.Column(db.String)
        nome_area_umida = db.Column(db.String)
        localizacao_area_umida = db.Column(db.String)
        status_do_registro = db.Column(db.Boolean, default=True)
        status_area_umida  = db.Column(db.String)
        data_criacao = db.Column(db.DateTime, server_default=func.now())
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
            return {attr.name: getattr(self, attr.name) for attr in self.__table__.columns}


class Equipamentos(db.Model):

    __table_args__ = {'schema':'main'}
    __tablename__ = 'equipamentos'

    id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    fk_area_umida= db.Column(db.Integer, db.ForeignKey('main.area_umida.id'))
    tipo_equipamento = db.Column(db.String)
    descricao_equipamento = db.Column(db.String)
    quantTotal = db.Column(db.Integer)
    quantProblema = db.Column(db.Integer)
    # vazamentos = db.Column(db.Integer)
    quantInutil = db.Column(db.Integer)
    status_do_registro = db.Column(db.Boolean, default=True)
    data_criacao = db.Column(db.DateTime, server_default=func.now())

    def update(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)

    def __init__(self, fk_area_umida, descricao_equipamento, tipo_equipamento, quantTotal, quantProblema, quantInutil):

        self.fk_area_umida = fk_area_umida
        self.descricao_equipamento = descricao_equipamento
        self.tipo_equipamento = tipo_equipamento
        self.quantTotal = int(quantTotal)
        self.quantProblema = int(quantProblema) if quantProblema != '' and quantProblema is not None else 0
        self.quantInutil = int(quantInutil) if quantInutil != '' and quantInutil is not None else 0

    def to_json(self):
        return {attr.name: getattr(self, attr.name) for attr in self.__table__.columns}
    

class Tabela(db.Model):
    __table_args__ = {'schema':'main'}
    __tablename__ = 'testando'

    id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    nome = db.Column(db.String)

    def __init__(self, nome):
        self.nome = nome
    def to_json(self):
        return {
            "id":self.id,
            "nome":self.nome
        }
    
#Tabela auxiliar
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


        def __init__(self, nivel_escola, tipo_area_umida, status_area_umida, tipo_equipamento, descricao_equipamento, periodo_populacao ):
            self.nivel_escola = nivel_escola
            self.tipo_area_umida = tipo_area_umida
            self.status_area_umida = status_area_umida
            self.tipo_equipamento = tipo_equipamento
            self.descricao_equipamento = descricao_equipamento
            self.periodo_populacao = periodo_populacao
            

        def to_json(self):
            return {attr.name: getattr(self, attr.name) for attr in self.__table__.columns}