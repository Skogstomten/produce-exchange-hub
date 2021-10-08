from flask import Blueprint, request

bp = Blueprint('producers', __name__, url_prefix='/producers')


@bp.route('/', methods=('GET', 'POST', 'PUT', 'DELETE'))
def producers():
    pass
