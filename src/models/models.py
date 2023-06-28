from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from datetime import datetime
from sqlalchemy import inspect

db = SQLAlchemy()


class Escolas(db.Model):

    __table_args__ = {'schema': 'main'}
    __tablename__ = 'escolas'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    nome = db.Column(db.String, unique=True, nullable=False)  # 255
    cnpj = db.Column(db.String, unique=True, nullable=False)  # 18
    email = db.Column(db.String, unique=True, nullable=False)  # 55
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


class Edificios(db.Model):

    __table_args__ = (db.UniqueConstraint('nome_do_edificio', 'fk_escola', name='nome_edifico_unico'),
                      # cria unicidade das combinações chave e coluna
                      db.Index('ix_edificio_nome_escola',
                               'nome_do_edificio', 'fk_escola', unique=True),
                      {'schema': 'main'})
    __tablename__ = 'edificios'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
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
    reservatorio = db.Column(db.Boolean)  # padrao é False
    capacidade_m3_edificio = db.Column(db.Float)
    agua_de_reuso = db.Column(db.Boolean)
    capacidade_reuso_m3_edificio = db.Column(db.Float)
    status_do_registro = db.Column(db.Boolean, default=True)
    data_criacao = db.Column(db.DateTime, server_default=func.now())
    area_umida = db.relationship('AreaUmida', backref='area_umida')
    populacao = db.relationship('Populacao', backref='populacao')
    hidrometros = db.relationship('Hidrometros', backref='hidrometros')

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __init__(self, fk_escola, numero_edificio, bairro_edificio, nome_do_edificio, cep_edificio, cnpj_edificio, logradouro_edificio, complemento_edificio, cidade_edificio, estado_edificio, pavimentos_edificio=None, area_total_edificio=None, capacidade_m3_edificio=0.0, capacidade_reuso_m3_edificio=0.0, reservatorio=False, agua_de_reuso=False, principal=False):

        self.fk_escola = fk_escola
        self.numero_edificio = numero_edificio
        self.bairro_edificio = bairro_edificio
        self.nome_do_edificio = nome_do_edificio
        self.principal = principal
        self.cep_edificio = cep_edificio
        self.cnpj_edificio = cnpj_edificio
        self.logradouro_edificio = logradouro_edificio
        self.bairro_edificio = bairro_edificio
        self.estado_edificio = estado_edificio
        self.cidade_edificio = cidade_edificio
        self.complemento_edificio = complemento_edificio
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
    fk_niveis = db.Column(db.Integer, db.ForeignKey('main.opniveis.id'))
    fk_periodo = db.Column(db.Integer, db.ForeignKey('main.populacao_periodos.id'))
    funcionarios = db.Column(db.Integer)
    alunos = db.Column(db.Integer)
    status_do_registro = db.Column(db.Boolean, default=True)
    data_criacao = db.Column(db.DateTime, server_default=func.now())

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
        return {attr.name: getattr(self, attr.name) for attr in self.__table__.columns}


class Hidrometros(db.Model):
    __table_args__ = {'schema': 'main'}
    __tablename__ = 'hidrometros'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fk_edificios = db.Column(db.Integer, db.ForeignKey('main.edificios.id'))
    fk_hidrometro = db.Column(db.Integer, db.ForeignKey('main.tipo_hidrometros.id'))
    status_do_registro = db.Column(db.Boolean, default=True)
    data_criacao = db.Column(db.DateTime, server_default=func.now())
    tipo_hidrometros = db.relationship('TipoHidrometro', backref='tipo_hidrometros')

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
    status_area_umida = db.Column(
        db.Integer, db.ForeignKey('main.aux_status_area_umida.id'))
    nome_area_umida = db.Column(db.String)
    localizacao_area_umida = db.Column(db.String)
    status_do_registro = db.Column(db.Boolean, default=True)
    data_criacao = db.Column(db.DateTime, server_default=func.now())
    equipamentos = db.relationship('Equipamentos', backref='equipamentos')
    tipo_area_umida_rel = db.relationship(
        'TipoAreaUmida', backref='aux_tipo_area_umida')
    status_area_umida_rel = db.relationship(
        'StatusAreaUmida', backref='aux_status_area_umida')

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __init__(self, fk_edificios, tipo_area_umida, nome_area_umida, localizacao_area_umida, status_area_umida):

        self.fk_edificios = fk_edificios
        self.tipo_area_umida = tipo_area_umida
        self.nome_area_umida = nome_area_umida
        self.localizacao_area_umida = localizacao_area_umida
        self.status_area_umida = status_area_umida

    def to_json(self):
        area_umida_descricao = self.tipo_area_umida_rel.tipo if self.tipo_area_umida_rel else None
        status_descricao = self.status_area_umida_rel.status if self.status_area_umida_rel else None

        jsonRetorno = {attr.name: getattr(self, attr.name) for attr in self.__table__.columns}
        jsonRetorno['tipo_area_umida'] = area_umida_descricao
        jsonRetorno['status_area_umida'] = status_descricao
        return jsonRetorno

class Equipamentos(db.Model):

    __table_args__ = {'schema': 'main'}
    __tablename__ = 'equipamentos'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fk_area_umida = db.Column(db.Integer, db.ForeignKey('main.area_umida.id'))
    tipo_equipamento = db.Column(
        db.Integer, db.ForeignKey('main.tipo_equipamentos.id'))
    descricao_equipamento = db.Column(
        db.Integer, db.ForeignKey('main.descricao_equipamentos.id'))
    quantTotal = db.Column(db.Integer)
    quantProblema = db.Column(db.Integer)
    quantInutil = db.Column(db.Integer)
    status_do_registro = db.Column(db.Boolean, default=True)
    data_criacao = db.Column(db.DateTime, server_default=func.now())
    tipo_equipamento_rel = db.relationship(
        'TiposEquipamentos', backref='main.tipo_equipamentos.id')
    descricao_equipamento_rel = db.relationship(
        'DescricaoEquipamentos', backref='main.descricao_equipamentos.id')

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __init__(self, fk_area_umida, descricao_equipamento, tipo_equipamento, quantTotal, quantProblema, quantInutil):

        self.fk_area_umida = fk_area_umida
        self.descricao_equipamento = descricao_equipamento
        self.tipo_equipamento = tipo_equipamento
        self.quantTotal = int(quantTotal)
        self.quantProblema = int(
            quantProblema) if quantProblema != '' and quantProblema is not None else 0
        self.quantInutil = int(
            quantInutil) if quantInutil != '' and quantInutil is not None else 0

    def to_json(self):
        tipo_equipamento = self.tipo_equipamento_rel.equipamento if self.tipo_equipamento_rel else None
        descricao = self.descricao_equipamento_rel.descricao if self.descricao_equipamento_rel else None

        jsonRetorno = {attr.name: getattr(self, attr.name) for attr in self.__table__.columns}
        jsonRetorno['tipo_equipamento'] = tipo_equipamento
        jsonRetorno['status_descricao'] = descricao
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


# TABELAS DE OPÇÕES


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


class Opcoes(db.Model):

    __table_args__ = {'schema': 'main'}
    __tablename__ = 'opcoes'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    opcao = db.Column(db.String, nullable=False, unique=True)
    funcao = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __init__(self, opcao, funcao):
        self.opcao = opcao
        self.funcao = funcao

    def to_json(self):
        return {attr.name: getattr(self, attr.name) for attr in self.__table__.columns}


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
    equipamento = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __init__(self, equipamento):
        self.equipamento = equipamento

    def to_json(self):
        return {attr.name: getattr(self, attr.name) for attr in self.__table__.columns}


class DescricaoEquipamentos(db.Model):

    __table_args__ = {'schema': 'main'}
    __tablename__ = 'descricao_equipamentos'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    tipo_equipamento = db.Column(
        db.Integer, db.ForeignKey('main.tipo_equipamentos.id'))
    descricao = db.Column(db.String)
    vazao = db.Column(db.Float)
    peso = db.Column(db.Float)
    tipo_equipamento_rel = db.relationship(
        'TiposEquipamentos', backref='tipo_equipamentos')
    

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __init__(self, tipo_equipamento, descricao):
        self.tipo_equipamento = tipo_equipamento
        self.descricao = descricao

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

class TipoDeAreaUmidaTipoDeEquipamento(db.Model):
    __table_args__ = {'schema': 'main'}
    __tablename__ = 'area_umida_equipamento'

    tipo_equipamento_id = db.Column(db.Integer, db.ForeignKey(
        'main.tipo_equipamentos.id'), primary_key=True)
    tipo_area_umida_id = db.Column(db.Integer, db.ForeignKey(
        'main.aux_tipo_area_umida.id'), primary_key=True)


def add_opniveis():
    opniveis = ['Médio', 'Superior', 'Fundamental', 'CEU', 'Berçario', 'EJA']
    tipoareaumida = ['Banheiro', 'Cozinha', 'Bebedouro', 'Jardim']
    statusareaumida = ['Aberto', 'Fechado', 'Em Manutenção', 'Ativo']
    tipohidrometro = ['Tipo A', 'Tipo B', 'Tipo C']

    descricaoequipamentos = [
        {"Chuveiro": [
            {
                "descricao": "Chuveiro Elétrico"
            },
            {
                "descricao": "Chuveiro Eletrônico"
            },
            {
                "descricao": "Chuveiro Gás"
            }],
         "Torneira": [
            {
                "descricao": "Acionador por botão"
            },
            {
                "descricao": "Acionador por sensor de proximidade"
            },
            {
                "descricao": "Acionador presencial"
            },
            {
                "descricao": "Acionador eletrônico"
            },
            {
                "descricao": "Acionador por alavanca"
            },
            {
                "descricao": "Acionador por registro giratório"
            }
        ],
            "Hidrante": [
            {
                "descricao": "Enterrado"
            },
            {
                "descricao": "Coluna"
            }
        ],
            "Sanitário": [
            {
                "descricao": "Caixa a coplada"
            },
            {
                "descricao": "Válvula de Descarga de Pressão"
            }
        ]
        }
    ]

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

    for status in statusareaumida:
        st = StatusAreaUmida.query.filter_by(status=status).first()

        if not st:
            st = StatusAreaUmida(status=status)
            db.session.add(st)

    for hidrometro in tipohidrometro:
        hid = TipoHidrometro.query.filter_by(tipo_hidrometro=hidrometro).first()

        if not hid:
            hid = TipoHidrometro(tipo_hidrometro=hidrometro)
            db.session.add(hid)

    db.session.commit()

    for equipamento in descricaoequipamentos:
        for key, values in equipamento.items():
            tequi = TiposEquipamentos.query.filter_by(equipamento=key).first()
            if not tequi:
                tequi = TiposEquipamentos(equipamento=key)
                db.session.add(tequi)
                db.session.commit()

            for desc in values:
                descricao_str = desc['descricao']
                descricao = DescricaoEquipamentos.query.filter_by(
                    descricao=descricao_str).first()

                if not descricao:
                    descricao = DescricaoEquipamentos(
                        tipo_equipamento=tequi.id, descricao=descricao_str
                    )
                    db.session.add(descricao)
                    db.session.commit()
