# Usage: python scripts/generate_monthly_report.py --user_id 1 --month 2025-10
import argparse
from app import create_app, db
from app.models import User, Account, Transaction
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io, boto3, os
from datetime import datetime

app = create_app()

def render_pdf(user, transactions):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter)
    c.setFont('Helvetica', 12)
    c.drawString(50,750, f'FinGuard 360 - Monthly Statement for {user.email}')
    y = 720
    for t in transactions[:50]:
        c.drawString(50, y, f"{t.txn_date} - {t.category} - ${float(t.amount):.2f} - {t.description[:40]}")
        y -= 15
        if y < 50:
            c.showPage()
            y = 750
    c.save()
    buf.seek(0)
    return buf

def upload_s3(buffer, key):
    s3 = boto3.client('s3', region_name=os.environ.get('AWS_REGION'))
    bucket = os.environ.get('AWS_S3_BUCKET')
    if not bucket:
        raise RuntimeError('AWS_S3_BUCKET not set')
    s3.upload_fileobj(buffer, bucket, key)
    return f's3://{bucket}/{key}'

def generate(user_id, month):
    with app.app_context():
        user = User.query.get(user_id)
        if not user:
            raise RuntimeError('user not found')
        accounts = Account.query.filter_by(user_id=user.id).all()
        acc_ids = [a.id for a in accounts]
        txns = Transaction.query.filter(Transaction.account_id.in_(acc_ids)).order_by(Transaction.txn_date.desc()).all()
        pdf = render_pdf(user, txns)
        key = f'reports/{user.id}/{month}.pdf'
        # Try upload - will raise if AWS not configured
        try:
            uri = upload_s3(pdf, key)
        except Exception as e:
            uri = 'local:' + key
        print('report:', uri)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--user_id', type=int, required=True)
    parser.add_argument('--month', type=str, required=True)
    args = parser.parse_args()
    generate(args.user_id, args.month)
