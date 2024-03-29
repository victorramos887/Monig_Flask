"""empty message

Revision ID: 278bb67bad71
Revises: 
Create Date: 2023-11-16 18:58:37.326715

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '278bb67bad71'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('aux_customizado_cliente',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('nivel_escola', sa.String(), nullable=True),
    sa.Column('tipo_area_umida', sa.String(), nullable=True),
    sa.Column('status_area_umida', sa.String(), nullable=True),
    sa.Column('tipo_equipamento', sa.String(), nullable=True),
    sa.Column('descricao_equipamento', sa.String(), nullable=True),
    sa.Column('periodo_populacao', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    schema='main'
    )
    op.create_table('aux_de_locais',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('nome_da_tabela', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    schema='main'
    )
    op.create_table('aux_operacao_area_umida',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('operacao', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('operacao'),
    schema='main'
    )
    op.create_table('aux_opniveis',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('nivel', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('nivel'),
    schema='main'
    )
    op.create_table('aux_populacao_periodos',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('periodo', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    schema='main'
    )
    op.create_table('aux_tipo_area_umida',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('tipo', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('tipo'),
    schema='main'
    )
    op.create_table('aux_tipo_equipamentos',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('aparelho_sanitario', sa.String(), nullable=False),
    sa.Column('vazao', sa.Float(), nullable=True),
    sa.Column('peso', sa.Float(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    schema='main'
    )
    op.create_table('aux_tipo_hidrometros',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('tipo_hidrometro', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    schema='main'
    )
    op.create_table('cliente',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('nome', sa.String(length=255), nullable=False),
    sa.Column('email', sa.String(length=55), nullable=False),
    sa.Column('cnpj', sa.String(length=18), nullable=False),
    sa.Column('telefone', sa.String(length=12), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('cnpj'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('nome'),
    schema='main'
    )
    op.create_table('escola_niveis_version_custom',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('escola_id', sa.Integer(), nullable=True),
    sa.Column('nivel_ensino_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('transacao', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    schema='main'
    )
    op.create_table('escolas',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('nome', sa.String(), nullable=True),
    sa.Column('cnpj', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('telefone', sa.String(length=25), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('nome'),
    schema='main'
    )
    op.create_table('reservatorio_edificio_version_custom',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('edificio_id', sa.Integer(), nullable=True),
    sa.Column('reservatorio_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('transacao', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    schema='main'
    )
    op.create_table('aux_area_umida_equipamento',
    sa.Column('tipo_equipamento_id', sa.Integer(), nullable=False),
    sa.Column('tipo_area_umida_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['tipo_area_umida_id'], ['main.aux_tipo_area_umida.id'], ),
    sa.ForeignKeyConstraint(['tipo_equipamento_id'], ['main.aux_tipo_equipamentos.id'], ),
    sa.PrimaryKeyConstraint('tipo_equipamento_id', 'tipo_area_umida_id'),
    schema='main'
    )
    op.create_table('edificios',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('fk_escola', sa.Integer(), nullable=True),
    sa.Column('numero_edificio', sa.String(), nullable=True),
    sa.Column('nome_do_edificio', sa.String(), nullable=False),
    sa.Column('principal', sa.Boolean(), nullable=True),
    sa.Column('cep_edificio', sa.String(), nullable=True),
    sa.Column('bairro_edificio', sa.String(), nullable=True),
    sa.Column('cidade_edificio', sa.String(), nullable=True),
    sa.Column('estado_edificio', sa.String(), nullable=True),
    sa.Column('cnpj_edificio', sa.String(), nullable=True),
    sa.Column('logradouro_edificio', sa.String(), nullable=True),
    sa.Column('complemento_edificio', sa.String(), nullable=True),
    sa.Column('pavimentos_edificio', sa.Integer(), nullable=True),
    sa.Column('area_total_edificio', sa.Float(), nullable=True),
    sa.Column('capacidade_reuso_m3_edificio', sa.Float(), nullable=True),
    sa.Column('agua_de_reuso', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['fk_escola'], ['main.escolas.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='main'
    )
    op.create_table('escola_niveis',
    sa.Column('escola_id', sa.Integer(), nullable=False),
    sa.Column('nivel_ensino_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['escola_id'], ['main.escolas.id'], ),
    sa.ForeignKeyConstraint(['nivel_ensino_id'], ['main.aux_opniveis.id'], ),
    sa.PrimaryKeyConstraint('escola_id', 'nivel_ensino_id'),
    schema='main'
    )
    op.create_table('reservatorios',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('fk_escola', sa.Integer(), nullable=True),
    sa.Column('nome_do_reservatorio', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['fk_escola'], ['main.escolas.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='main'
    )
    op.create_table('usuarios',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('escola', sa.Integer(), nullable=True),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('senha', sa.String(length=126), nullable=False),
    sa.Column('cod_cliente', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['cod_cliente'], ['main.cliente.id'], ),
    sa.ForeignKeyConstraint(['escola'], ['main.escolas.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    schema='main'
    )
    op.create_table('area_umida',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('fk_edificios', sa.Integer(), nullable=True),
    sa.Column('tipo_area_umida', sa.Integer(), nullable=True),
    sa.Column('status_area_umida', sa.Boolean(), nullable=True),
    sa.Column('operacao_area_umida', sa.Integer(), nullable=True),
    sa.Column('nome_area_umida', sa.String(), nullable=True),
    sa.Column('localizacao_area_umida', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['fk_edificios'], ['main.edificios.id'], ),
    sa.ForeignKeyConstraint(['operacao_area_umida'], ['main.aux_operacao_area_umida.id'], ),
    sa.ForeignKeyConstraint(['tipo_area_umida'], ['main.aux_tipo_area_umida.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='main'
    )
    op.create_table('aux_tipo_de_eventos',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('fk_cliente', sa.Integer(), nullable=True),
    sa.Column('nome_do_tipo_de_evento', sa.String(), nullable=True),
    sa.Column('recorrente', sa.Boolean(), nullable=True),
    sa.Column('dia', sa.Integer(), nullable=True),
    sa.Column('mes', sa.Integer(), nullable=True),
    sa.Column('requer_acao', sa.Boolean(), nullable=True),
    sa.Column('tempo', sa.Integer(), nullable=True),
    sa.Column('unidade', sa.String(), nullable=True),
    sa.Column('usuario', sa.Integer(), nullable=True),
    sa.Column('color', sa.String(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['fk_cliente'], ['main.cliente.id'], ),
    sa.ForeignKeyConstraint(['usuario'], ['main.usuarios.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='main'
    )
    op.create_table('hidrometros',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('fk_edificios', sa.Integer(), nullable=True),
    sa.Column('fk_hidrometro', sa.Integer(), nullable=True),
    sa.Column('hidrometro', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['fk_edificios'], ['main.edificios.id'], ),
    sa.ForeignKeyConstraint(['fk_hidrometro'], ['main.aux_tipo_hidrometros.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='main'
    )
    op.create_table('populacao',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('fk_edificios', sa.Integer(), nullable=True),
    sa.Column('fk_niveis', sa.Integer(), nullable=True),
    sa.Column('fk_periodo', sa.Integer(), nullable=True),
    sa.Column('funcionarios', sa.Integer(), nullable=True),
    sa.Column('alunos', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['fk_edificios'], ['main.edificios.id'], ),
    sa.ForeignKeyConstraint(['fk_niveis'], ['main.aux_opniveis.id'], ),
    sa.ForeignKeyConstraint(['fk_periodo'], ['main.aux_populacao_periodos.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='main'
    )
    op.create_table('reservatorio_edificio',
    sa.Column('edificio_id', sa.Integer(), nullable=False),
    sa.Column('reservatorio_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['edificio_id'], ['main.edificios.id'], ),
    sa.ForeignKeyConstraint(['reservatorio_id'], ['main.reservatorios.id'], ),
    sa.PrimaryKeyConstraint('edificio_id', 'reservatorio_id'),
    schema='main'
    )
    op.create_table('consumo_agua',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('consumo', sa.Integer(), nullable=False),
    sa.Column('data', sa.DateTime(), nullable=True),
    sa.Column('dataFimPeriodo', sa.DateTime(), nullable=True),
    sa.Column('dataInicioPeriodo', sa.DateTime(), nullable=True),
    sa.Column('valor', sa.Float(), nullable=True),
    sa.Column('fk_hidrometro', sa.Integer(), nullable=True),
    sa.Column('fk_escola', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['fk_escola'], ['main.escolas.id'], ),
    sa.ForeignKeyConstraint(['fk_hidrometro'], ['main.hidrometros.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='main'
    )
    op.create_table('equipamentos',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('fk_area_umida', sa.Integer(), nullable=True),
    sa.Column('tipo_equipamento', sa.Integer(), nullable=True),
    sa.Column('quantTotal', sa.Integer(), nullable=True),
    sa.Column('quantProblema', sa.Integer(), nullable=True),
    sa.Column('quantInutil', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['fk_area_umida'], ['main.area_umida.id'], ),
    sa.ForeignKeyConstraint(['tipo_equipamento'], ['main.aux_tipo_equipamentos.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='main'
    )
    op.create_table('eventos',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('fk_tipo', sa.Integer(), nullable=True),
    sa.Column('fk_escola', sa.Integer(), nullable=True),
    sa.Column('nome', sa.String(), nullable=True),
    sa.Column('datainicio', sa.DateTime(), nullable=True),
    sa.Column('datafim', sa.DateTime(), nullable=True),
    sa.Column('local', sa.Integer(), nullable=True),
    sa.Column('tipo_de_local', sa.Integer(), nullable=True),
    sa.Column('encerramento', sa.Boolean(), nullable=True),
    sa.Column('data_encerramento', sa.DateTime(), nullable=True),
    sa.Column('observacao', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['fk_escola'], ['main.escolas.id'], ),
    sa.ForeignKeyConstraint(['fk_tipo'], ['main.aux_tipo_de_eventos.id'], ),
    sa.ForeignKeyConstraint(['tipo_de_local'], ['main.aux_de_locais.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='main'
    )
    op.create_table('monitoramento',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('datahora', sa.DateTime(), nullable=True),
    sa.Column('fk_escola', sa.Integer(), nullable=True),
    sa.Column('hidrometro', sa.Integer(), nullable=True),
    sa.Column('leitura', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['fk_escola'], ['main.escolas.id'], ),
    sa.ForeignKeyConstraint(['hidrometro'], ['main.hidrometros.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='main'
    )
    op.create_table('populacao_niveis',
    sa.Column('populacao_id', sa.Integer(), nullable=False),
    sa.Column('nivel_escola_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['nivel_escola_id'], ['main.aux_opniveis.id'], ),
    sa.ForeignKeyConstraint(['populacao_id'], ['main.populacao.id'], ),
    sa.PrimaryKeyConstraint('populacao_id', 'nivel_escola_id'),
    schema='main'
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('populacao_niveis', schema='main')
    op.drop_table('monitoramento', schema='main')
    op.drop_table('eventos', schema='main')
    op.drop_table('equipamentos', schema='main')
    op.drop_table('consumo_agua', schema='main')
    op.drop_table('reservatorio_edificio', schema='main')
    op.drop_table('populacao', schema='main')
    op.drop_table('hidrometros', schema='main')
    op.drop_table('aux_tipo_de_eventos', schema='main')
    op.drop_table('area_umida', schema='main')
    op.drop_table('usuarios', schema='main')
    op.drop_table('reservatorios', schema='main')
    op.drop_table('escola_niveis', schema='main')
    op.drop_table('edificios', schema='main')
    op.drop_table('aux_area_umida_equipamento', schema='main')
    op.drop_table('reservatorio_edificio_version_custom', schema='main')
    op.drop_table('escolas', schema='main')
    op.drop_table('escola_niveis_version_custom', schema='main')
    op.drop_table('cliente', schema='main')
    op.drop_table('aux_tipo_hidrometros', schema='main')
    op.drop_table('aux_tipo_equipamentos', schema='main')
    op.drop_table('aux_tipo_area_umida', schema='main')
    op.drop_table('aux_populacao_periodos', schema='main')
    op.drop_table('aux_opniveis', schema='main')
    op.drop_table('aux_operacao_area_umida', schema='main')
    op.drop_table('aux_de_locais', schema='main')
    op.drop_table('aux_customizado_cliente', schema='main')
    # ### end Alembic commands ###
