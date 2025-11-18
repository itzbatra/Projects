# Run: flask init-db  (inside container) then python scripts/seed_mock_data.py
from faker import Faker
from app import create_app, db
from app.models import User, Account, Transaction
from datetime import date, timedelta
app = create_app()
fake = Faker()

def seed(n_users=10):
    with app.app_context():
        for _ in range(n_users):
            email = fake.unique.email()
            u = User(email=email, password_hash='pbkdf2:sha256:150000$dev$devhash', full_name=fake.name())
            db.session.add(u)
            db.session.commit()
            acc = Account(user_id=u.id, name='Checking')
            db.session.add(acc)
            db.session.commit()
            for i in range(30):
                txn = Transaction(account_id=acc.id, amount=round(float(fake.pydecimal(left_digits=3, right_digits=2, positive=True)),2),
                                  category=fake.word(), description=fake.sentence(), txn_date=date.today()-timedelta(days=i))
                db.session.add(txn)
            db.session.commit()
    print('seed complete')

if __name__ == '__main__':
    seed(5)
