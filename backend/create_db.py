from app import create_app, db
from datetime import datetime, date
from app.models import User

def create_default_admin():
    admin = User.query.filter_by(role='admin').first()
    if not admin:
        admin = User(
            username='admin',
            email='admin@example.com',
            gender='Male',
            dob=date(2003, 11, 20),
            joiningDate=date.today(),
            qualification='Admin',
            college='System',
            last_login=datetime.now(),
            role='admin'
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()

def create_all():
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()
        print("Tables created.")
        create_default_admin()

if __name__ == '__main__':
    create_all()
