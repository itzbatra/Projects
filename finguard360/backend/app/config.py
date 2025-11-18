import os
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://postgres:postgres@db:5432/postgres')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET = os.environ.get('JWT_SECRET', 'jwt-secret-dev')
    AWS_S3_BUCKET = os.environ.get('AWS_S3_BUCKET', 'my-finguard-bucket')
    AWS_REGION = os.environ.get('AWS_REGION', 'us-east-1')
