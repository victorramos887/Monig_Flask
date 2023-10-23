from flask import Blueprint, json, jsonify, request, render_template, flash, render_template_string
from ..constants.http_status_codes import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_506_VARIANT_ALSO_NEGOTIATES, HTTP_409_CONFLICT, HTTP_401_UNAUTHORIZED
from ..models import Escolas, EscolaNiveis, AuxTipoDeEventos, Eventos, Edificios, Reservatorios, db, AreaUmida, Equipamentos, Populacao, Hidrometros, ReservatorioEdificio, ReservatorioEdificiosVersion
from sqlalchemy import exc, text, func


remover = Blueprint('remover', __name__, url_prefix='/api/v1/remover')


# testar rota para reverter
@remover.get('/restaurar-escola/<id>')
def reverter_escola(id):
    escola = db.session.query(Escolas).filter_by(id=id).all()
    if escola and escola.prev():
        escola.prev().revert()
        db.session.commit()  # salva as mudanças no banco de dados
        return jsonify({"status": True, 'mensagem': 'Escola restaurada'}), HTTP_200_OK



@remover.put('/escolas/<id>')
def escolas_remover(id):

    try:

        escola = Escolas.query.filter_by(id=id).first()
        if not escola:
            return jsonify({'status': False, 'mensagem': 'Escola não encontrado'}), 404

        niveis = EscolaNiveis.query.filter_by(escola_id=id).all()
        if niveis:
            for nivel in niveis:
                db.session.delete(nivel)
        
        reservatorios = Reservatorios.query.filter_by(fk_escola=id).all()
        if reservatorios:
            for reservatorio in reservatorios:
                db.session.delete(reservatorio)

        edificios =  Edificios.query.filter_by(fk_escola=id).all()
        if edificios:
            for edificio in edificios:

                area_umidas =  AreaUmida.query.filter_by(fk_edificios=edificio.id).all()
                if area_umidas:
                    for area_umida in area_umidas:

                        equipamentos = Equipamentos.query.filter_by(
                            fk_area_umida=area_umida.id)
                        if equipamentos:
                            for equipamento in equipamentos:
                                db.session.delete(equipamento)

                    db.session.delete(area_umida)

                hidrometros = Hidrometros.query.filter_by(fk_edificios=edificio.id)
                if hidrometros:
                    for hidrometro in hidrometros:
                        db.session.delete(hidrometro)

                populacao = Populacao.query.filter_by(fk_edificios=edificio.id)
                if populacao:
                    for populacao_ in populacao :
                        db.session.delete(populacao_)

        db.session.delete(edificio)

        db.session.delete(escola)
        db.session.commit()
        return jsonify({"status": True, 'mensagem': 'Escola removida'}), HTTP_200_OK

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "status": False, 'mensagem': "Erro não tratado", "codigo": str(e)
        }), 400


# edificios
@remover.put('/edificios/<id>')
def edificios_remover(id):

    try:
        edificio = Edificios.query.filter_by(id=id).first()
        if not edificio:
            return jsonify({'status':False,'mensagem': 'Edificio não encontrado'}), 404 
       
        area_umidas =  AreaUmida.query.filter_by(fk_edificios=edificio.id).all()
        if area_umidas:
            for area_umida in area_umidas:

                equipamentos = Equipamentos.query.filter_by(
                    fk_area_umida=area_umida.id)
                if equipamentos:
                    for equipamento in equipamentos:
                        db.session.delete(equipamento)

            db.session.delete(area_umida)

        hidrometros = Hidrometros.query.filter_by(fk_edificios=edificio.id)
        if hidrometros:
            for hidrometro in hidrometros:
                db.session.delete(hidrometro)

        populacao = Populacao.query.filter_by(fk_edificios=edificio.id)
        if populacao:
            for populacao_ in populacao :
                db.session.delete(populacao_)

        db.session.delete(edificio)
        db.session.commit()

        reservatorio_edificio = ReservatorioEdificio.query.filter_by(
            edificio_id=edificio.id)
        if reservatorio_edificio:
            for reservatorio_ in reservatorio_edificio:
                db.session.delete(reservatorio_)

                edificios_reservatorio_version = ReservatorioEdificiosVersion(
                    edificio_id=edificio.id,
                    reservatorio_id=reservatorio_.id,
                    transacao=3,
                    created_at=datetime.now()
                )
                db.session.add(edificios_reservatorio_version)
        return jsonify({"status": True, 'mensagem': 'Edificio removido'}), HTTP_200_OK

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "status": False, 'mensagem': "Erro não tratado", "codigo": str(e)
        }), 400

    
#hidrometro
@remover.put('/hidrometros/<id>')
def hidrometro_remover(id):

    try:
        hidrometro = Hidrometros.query.filter_by(id=id).first()

        if not hidrometro:
            return jsonify({'status': False, 'mensagem': 'hidrometro não encontrado'}), 404

        db.session.delete(hidrometro)
        db.session.commit()

        return jsonify({"status": True, 'mensagem': 'hidrometo removido'}), HTTP_200_OK

    except Exception as e:

        db.session.rollback()
        return jsonify({
            "status": False,
            "mensagem": "Erro não tratado!",
            "codigo": str(e)
        }), 400


# populacao
@remover.put('/populacao/<id>')
def populacao_remover(id):
    try:
        populacao = Populacao.query.filter_by(id=id).first()

        if not populacao:
            return jsonify({'status': False, 'mensagem': 'População não encontrado'}), 404

        db.session.delete(populacao)
        db.session.commit()

        return jsonify({"status": True, 'mensagem': 'População removida'}), HTTP_200_OK

    except Exception as e:

        db.session.rollback()
        return jsonify({
            "status": False,
            "mensagem": "Erro não tratado!",
            "codigo": str(e)
        }), 400


# area-umida
@remover.put('/area-umida/<id>')
def area_umida_remover(id):
    try:
        area_umida = AreaUmida.query.filter_by(id=id).first()

        if not area_umida:
            return jsonify({'status': False, 'mensagem': 'Área Úmida não encontrado'}), 404

        if area_umida:
            equipamentos = Equipamentos.query.filter_by(
                fk_area_umida=area_umida.id)
            if equipamentos:
                for equipamento in equipamentos:
                    db.session.delete(equipamento)

        db.session.delete(area_umida)
        db.session.commit()

        return jsonify({"status": True, 'mensagem': 'Área Úmida removida'}), HTTP_200_OK

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "status": False,
            "mensagem": "Erro não tratado!",
            "codigo": str(e)
        }), 400


# equipamentos
@remover.put('/equipamentos/<id>')
def equipamentos_remover(id):
    try:
        equipamento = Equipamentos.query.filter_by(id=id).first()

        if not equipamento:
            return jsonify({'status': False, 'mensagem': 'Equipamento não encontrado'}), 404

        db.session.delete(equipamento)
        db.session.commit()

        return jsonify({"status": True, 'mensagem': 'Equipamento removido'}), HTTP_200_OK

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "status": False,
            "mensagem": "Erro não tratado!",
            "codigo": str(e)
        }), 400

# reservatorios


@remover.put('/reservatorios/<id>')
def reservatorio_remover(id):
    try:
        reservatorio = Reservatorios.query.filter_by(id=id).first()

        if not reservatorio:
            return jsonify({'status': False, 'mensagem': 'Reservatório não encontrado'}), 404

        db.session.delete(reservatorio)
        db.session.commit()

        return jsonify({"status": True, 'mensagem': 'Reservatório removido'}), HTTP_200_OK

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "status": False,
            "mensagem": "Erro não tratado!",
            "codigo": str(e)
        }), 400

# tipo-evento


@remover.put('/tipo-evento/<id>')
def tipo_evento_remover(id):
    tipo_evento = AuxTipoDeEventos.query.filter_by(id=id).first()

    if not tipo_evento:
        return jsonify({'status': False, 'mensagem': 'Tipo de Evento não encontrado'}), 404

    db.session.delete(tipo_evento)
    db.session.commit()

    return jsonify({"status": True, 'mensagem': 'Tipo de Evento removido'}), HTTP_200_OK


# eventos
@remover.put('/evento/<id>')
def evento_remover(id):
    evento = Eventos.query.filter_by(id=id).first()

    if not evento:
        return jsonify({'status': False, 'mensagem': 'Evento não encontrado'}), 404

    db.session.delete(evento)
    db.session.commit()

    return jsonify({"status": True, 'mensagem': 'Evento removido'}), HTTP_200_OK
