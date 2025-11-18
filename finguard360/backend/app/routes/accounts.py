from flask import Blueprint, jsonify, request, g
from ..models import Account, AuditLog
from .. import db
from .auth import token_required

accounts_bp = Blueprint('accounts', __name__)

@accounts_bp.route('', methods=['GET'])
@token_required
def list_accounts():
    user = g.current_user
    accs = Account.query.filter_by(user_id=user.id).all()
    return jsonify([{'id':a.id,'name':a.name,'currency':a.currency} for a in accs])

@accounts_bp.route('', methods=['POST'])
@token_required
def create_account():
    user = g.current_user
    data = request.json or {}
    a = Account(user_id=user.id, name=data.get('name','Checking'), currency=data.get('currency','CAD'))
    db.session.add(a)
    db.session.commit()
    db.session.add(AuditLog(user_id=user.id, action='create_account', meta={'account_id': a.id}, ip_address=request.remote_addr))
    db.session.commit()
    return jsonify({'id': a.id}), 201
