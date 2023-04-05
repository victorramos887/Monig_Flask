from flask import Blueprint, jsonify, request, render_template, flash, render_template_string
from ..constants.http_status_codes import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_506_VARIANT_ALSO_NEGOTIATES, HTTP_409_CONFLICT, HTTP_401_UNAUTHORIZED
from ..models import Escolas, Edificios, db, AreaUmida, Equipamentos, Populacao
from sqlalchemy import exc

editar = Blueprint('editar', __name__, url_prefix='/api/v1/cadastros')

#EDITAR ESCOLA
@editar.put('/escolas')
def escolas_editar():
    return 'ok'