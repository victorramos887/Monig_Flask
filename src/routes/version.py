from flask import Blueprint, jsonify
from sqlalchemy_continuum import version_class
from ..models import Escolas, Edificios, AreaUmida, Equipamentos, Hidrometros, Populacao,db

version = Blueprint('version', __name__, url_prefix='/api/v1/version')


@version.get('/escolas/<int:id>')
def escolas(id):

    EscolaVersion = version_class(Escolas)
    queryescolaVersion = EscolaVersion.query.filter_by(id = id).all()

    json = []
    for query in queryescolaVersion:
       
        json.append({
            "nome": query.nome,
            "cnpj":query.cnpj,
            "email":query.email,
            "telefone":query.telefone,
            "create_at":query.created_at,
            "updated_at":query.updated_at,
            "id_version":query.transaction_id,
            "Current":True if query.end_transaction_id is None else False,
            "Operacao":["Insert", "Update", "Delete"][query.operation_type]
        })

    return jsonify(json)


@version.get('/escolas-removidas')
def escolas_removidas():
    
    EscolaVersion = version_class(Escolas)
    queryEscolaVersionRemovidas = EscolaVersion.query.filter_by(operation_type = 2).all()
    
    json = []
    
    for query in queryEscolaVersionRemovidas:
        
        json.append({
            "nome": query.nome,
            "cnpj":query.cnpj,
            "email":query.email,
            "telefone":query.telefone,
            "create_at":query.created_at,
            "updated_at":query.updated_at,
            "id_version":query.transaction_id,
            "Current":True if query.end_transaction_id is None else False,
            "Operacao": "Delete"
        })
    
    return jsonify(json)

@version.get('/escolas-editadas')
def escola_editadas():
    
    EscolaVersion = version_class(Escolas)
    queryEscolaVersionEditada = EscolaVersion.query.filter_by(operation_type=1).all()
    
    json = []
    
    for query in queryEscolaVersionEditada:
        
        json.append({
            "nome": query.nome,
            "cnpj":query.cnpj,
            "email":query.email,
            "telefone":query.telefone,
            "create_at":query.created_at,
            "updated_at":query.updated_at,
            "id_version":query.transaction_id,
            "Current":True if query.end_transaction_id is None else False,
            "Operacao": "Update"
        })
        
    return jsonify(json)
    
@version.get('/escola-deletada/<int:id>')
def escola_removida(id):
    
    EscolaVersion = version_class(Escolas)
    queryEscolaVersionRemovida = EscolaVersion.query.filter_by(operation_type=2, id = id).first()
    
    
    if queryEscolaVersionRemovida:
        json = {
            "nome": queryEscolaVersionRemovida.nome,
                "cnpj":queryEscolaVersionRemovida.cnpj,
                "email":queryEscolaVersionRemovida.email,
                "telefone":queryEscolaVersionRemovida.telefone,
                "create_at":queryEscolaVersionRemovida.created_at,
                "updated_at":queryEscolaVersionRemovida.updated_at,
                "id_version":queryEscolaVersionRemovida.transaction_id,
                "Current":True if queryEscolaVersionRemovida.end_transaction_id is None else False,
                "Operacao": "Delete"
        }
        
        return jsonify(json), 200

    return jsonify({
        "mensagem":"Escola não encontrada!"
    }), 400

@version.get('/edificio-deletado/<int:id>')
def edificio_version_removido(id):
    
    EdificioVersion = version_class(Edificios)
    queryEdificiosVersionRemovido = EdificioVersion.query.filter_by(operation_type=2, id=id).first()
    
    if queryEdificiosVersionRemovido:
        
        json = {
            "fk_escola":queryEdificiosVersionRemovido.fk_escola,
            "nome":queryEdificiosVersionRemovido.nome_do_edificio,
            "numero":queryEdificiosVersionRemovido.numero_edificio,
            "cep_edificio":queryEdificiosVersionRemovido.cep_edificio,
            "bairro":queryEdificiosVersionRemovido.bairro_edificio,
            "cidade":queryEdificiosVersionRemovido.cidade_edificio,
            "estado":queryEdificiosVersionRemovido.estado_edificio,
            "cnpj":queryEdificiosVersionRemovido.cnpj_edificio,
            "logradouro":queryEdificiosVersionRemovido.logradouro_edificio,
            "complemento":queryEdificiosVersionRemovido.complemento_edificio,
            "pavimentos":queryEdificiosVersionRemovido.pavimentos_edificio,
            "area_total":queryEdificiosVersionRemovido.area_total_edificio,
            "capacidade_reuso":queryEdificiosVersionRemovido.capacidade_reuso_m3_edificio,
            "agua_de_reuso":queryEdificiosVersionRemovido.agua_de_reuso
        }
        
        return jsonify(json), 200
    
    return jsonify({
        "mensagem":"Edificio não encontrado!"
    }), 400

@version.get('/edificio-editados')
def edificio_version_editado():
    
    EdificioVersion = version_class(Edificios)
    queryEdificiosVersionEditado = EdificioVersion.query.filter_by(operation_type=1).all()
    
    json = []
    if queryEdificiosVersionEditado:
        for query in queryEdificiosVersionEditado: 
            print(query)   
            json.append({
                "fk_escola":query.fk_escola,
                "nome":query.nome_do_edificio,
                "numero":query.numero_edificio,
                "cep_edificio":query.cep_edificio,
                "bairro":query.bairro_edificio,
                "cidade":query.cidade_edificio,
                "estado":query.estado_edificio,
                "cnpj":query.cnpj_edificio,
                "logradouro":query.logradouro_edificio,
                "complemento":query.complemento_edificio,
                "pavimentos":query.pavimentos_edificio,
                "area_total":query.area_total_edificio,
                "capacidade_reuso":query.capacidade_reuso_m3_edificio,
                "agua_de_reuso":query.agua_de_reuso
            })
            
            return jsonify(json), 200
        
        
    
    return jsonify({
        "mensagem":"Edificio não encontrado!"
    }), 400

    
@version.get('/area-umida-deletada/<int:id>')
def area_umida_version_removida(id):
    
    AreaUmidaVersion = version_class(AreaUmida)
    queryAreaUmidaVersionRemovida = AreaUmidaVersion.query.filter_by(operation_type=2, id=id).first()
    
    if queryAreaUmidaVersionRemovida:
        
        json = {
            "fk_edificios":queryAreaUmidaVersionRemovida.fk_edificios,
            "tipo_area_umida":queryAreaUmidaVersionRemovida.tipo_area_umida,
            "status_area_umida":queryAreaUmidaVersionRemovida.status_area_umida,
            "operacao_area_umida":queryAreaUmidaVersionRemovida.operacao_area_umida,
            "nome":queryAreaUmidaVersionRemovida.nome_area_umida,
            "localização":queryAreaUmidaVersionRemovida.localizacao_area_umida
        }
        
        return jsonify(json), 200
    
    
    return jsonify({
        "mensagem":"Area Umida não encontrada!"
    }), 400
        


@version.get('/equipamento-deletado/<int:id>')
def equipamento_deletado(id):
    
    EquipamentoVersion = version_class(Equipamentos)
    queryEquipamentoVersionRemovido = EquipamentoVersion.query.filter_by(operation_type=2, id=id).first()
    
    if queryEquipamentoVersionRemovido:
        
        json = {
            "fk_area_umida":queryEquipamentoVersionRemovido.fk_area_umida,
            "tipo_equipamento":queryEquipamentoVersionRemovido.tipo_equipamento,
            "Quantidade Total":queryEquipamentoVersionRemovido.quantTotal,
            "Quantidade com Problema":queryEquipamentoVersionRemovido.quantProblema,
            "Quantidade inutilizada":queryEquipamentoVersionRemovido.quantInutil
        }
    
        return jsonify(json), 200

    return jsonify({
        "mensagem":"Equipamento não encontrado!"
    }), 400
    

@version.get('/populacao-deletada/<int:id>')
def populacao_deletado(id):
    
    PopulacaoVersion = version_class(Populacao)
    queryPopulacaoVersionRemovido = PopulacaoVersion.query.filter_by(operation_type=2, id=id).first()
    
    if queryPopulacaoVersionRemovido:
        
        json = {
            "fk_edificios":queryPopulacaoVersionRemovido.fk_edificios,
            "fk_niveis":queryPopulacaoVersionRemovido.fk_niveis,
            "fk_periodo":queryPopulacaoVersionRemovido.fk_periodo,
            "Funcionários":queryPopulacaoVersionRemovido.funcionarios,
            "Alunos":queryPopulacaoVersionRemovido.alunos
        }
    
        return jsonify(json), 200

    return jsonify({
        "mensagem":"População não encontrada!"
    }), 400

@version.get('/hidrometro-deletada/<int:id>')
def hidrometro_deletado(id):
    
    HidrometroVersion = version_class(Hidrometros)
    queryHidrometroVersionRemovido = HidrometroVersion.query.filter_by(operation_type=2, id=id).first()
    
    if queryHidrometroVersionRemovido:
        
        json = {
            "fk_edificios":queryHidrometroVersionRemovido.fk_edificios,
            "Nome":queryHidrometroVersionRemovido.hidrometro
        }
    
        return jsonify(json), 200

    return jsonify({
        "mensagem":"Hidrometro não encontrado!"
    }), 400