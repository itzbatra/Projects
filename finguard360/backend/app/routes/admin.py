from flask import Blueprint, jsonify, request
from ..models import User, AuditLog
from .. import db
from .auth import token_required
from flask import g

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/users', methods=['GET'])
@token_required
def list_users():
    user = g.current_user
    if user.role != 'admin':
        return jsonify({'message':'forbidden'}), 403
    users = User.query.limit(200).all()
    return jsonify([{'id':u.id,'email':u.email,'role':u.role,'created_at':u.created_at.isoformat()} for u in users])

@admin_bp.route('/audit', methods=['GET'])
@token_required
def view_audit():
    user = g.current_user
    if user.role != 'admin':
        return jsonify({'message':'forbidden'}), 403
    logs = AuditLog.query.order_by(AuditLog.created_at.desc()).limit(500).all()
    return jsonify([{'id':l.id,'user_id':l.user_id,'action':l.action,'meta':l.meta,'ip':l.ip_address,'created_at':l.created_at.isoformat()} for l in logs])
