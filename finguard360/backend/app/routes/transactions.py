from flask import Blueprint, jsonify, request, g, current_app
from ..models import Transaction, Account, AuditLog
from .. import db
from .auth import token_required
from datetime import datetime

transactions_bp = Blueprint('transactions', __name__)

@transactions_bp.route('', methods=['GET'])
@token_required
def list_transactions():
    user = g.current_user
    accounts = Account.query.filter_by(user_id=user.id).all()
    acc_ids = [a.id for a in accounts]
    txns = Transaction.query.filter(Transaction.account_id.in_(acc_ids)).order_by(Transaction.txn_date.desc()).limit(500).all()
    items = []
    for t in txns:
        items.append({'id': t.id, 'amount': float(t.amount), 'category': t.category, 'description': t.description, 'txn_date': t.txn_date.isoformat()})
    return jsonify(items)

@transactions_bp.route('', methods=['POST'])
@token_required
def create_transaction():
    user = g.current_user
    data = request.json or {}
    account_id = data.get('account_id')
    acc = Account.query.filter_by(id=account_id, user_id=user.id).first()
    if not acc:
        return jsonify({'message':'account not found'}), 404
    t = Transaction(account_id=acc.id, amount=data.get('amount'), category=data.get('category'), description=data.get('description'), txn_date=data.get('txn_date') or datetime.utcnow().date())
    db.session.add(t)
    db.session.commit()
    db.session.add(AuditLog(user_id=user.id, action='create_transaction', meta={'txn_id': t.id}, ip_address=request.remote_addr))
    db.session.commit()
    return jsonify({'id': t.id}), 201
