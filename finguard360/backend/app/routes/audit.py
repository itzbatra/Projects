from flask import Blueprint, jsonify, request, g
from ..models import AuditLog
from .. import db
from .auth import token_required

audit_bp = Blueprint('audit', __name__)

@audit_bp.route('', methods=['GET'])
@token_required
def list_my_audit():
    user = g.current_user
    logs = AuditLog.query.filter_by(user_id=user.id).order_by(AuditLog.created_at.desc()).limit(200).all()
    return jsonify([{'id':l.id,'action':l.action,'meta':l.meta,'created_at':l.created_at.isoformat()} for l in logs])
