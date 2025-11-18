from flask import Blueprint, request, jsonify, current_app, g
from werkzeug.security import generate_password_hash, check_password_hash
from .. import db
from ..models import User, RefreshToken, AuditLog
import jwt, datetime, os
from functools import wraps
import secrets

auth_bp = Blueprint('auth', __name__)

def create_access_token(user_id, expires_hours=3):
    payload = {'sub': user_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=expires_hours)}
    return jwt.encode(payload, current_app.config['JWT_SECRET'], algorithm='HS256')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        auth = request.headers.get('Authorization','')
        parts = auth.split()
        if len(parts)==2 and parts[0]=='Bearer':
            token = parts[1]
        if not token:
            return jsonify({'message':'Token is missing'}), 401
        try:
            data = jwt.decode(token, current_app.config['JWT_SECRET'], algorithms=['HS256'])
            user = User.query.get(data['sub'])
            g.current_user = user
        except Exception as e:
            return jsonify({'message':'Token invalid','error':str(e)}), 401
        return f(*args, **kwargs)
    return decorated

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json or {}
    email = (data.get('email') or '').lower()
    pw = data.get('password') or ''
    if not email or not pw:
        return jsonify({'message':'email and password required'}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({'message':'email exists'}), 400
    user = User(email=email, password_hash=generate_password_hash(pw), full_name=data.get('full_name'))
    db.session.add(user)
    db.session.commit()
    # audit
    db.session.add(AuditLog(user_id=user.id, action='register', meta={'email':email}, ip_address=request.remote_addr))
    db.session.commit()
    return jsonify({'message':'created','id': user.id}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json or {}
    email = (data.get('email') or '').lower()
    pw = data.get('password') or ''
    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password_hash, pw):
        return jsonify({'message':'invalid credentials'}), 401
    access = create_access_token(user.id)
    refresh = secrets.token_urlsafe(64)
    rt = RefreshToken(user_id=user.id, token=refresh, expires_at=datetime.datetime.utcnow()+datetime.timedelta(days=30))
    db.session.add(rt)
    db.session.commit()
    db.session.add(AuditLog(user_id=user.id, action='login', meta={'ip': request.remote_addr}))
    db.session.commit()
    return jsonify({'access_token': access, 'refresh_token': refresh})

@auth_bp.route('/refresh', methods=['POST'])
def refresh():
    data = request.json or {}
    token = data.get('refresh_token')
    if not token:
        return jsonify({'message':'refresh_token required'}), 400
    rt = RefreshToken.query.filter_by(token=token).first()
    if not rt or rt.expires_at < datetime.datetime.utcnow():
        return jsonify({'message':'invalid refresh token'}), 401
    access = create_access_token(rt.user_id)
    return jsonify({'access_token': access})

@auth_bp.route('/me', methods=['GET'])
@token_required
def me():
    user = g.current_user
    return jsonify({'id': user.id, 'email': user.email, 'full_name': user.full_name, 'role': user.role})
