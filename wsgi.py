from app import create_app, db
from app.models import User, Role, Permission

app = create_app()

# Criar tabelas do banco de dados e usuário admin inicial
with app.app_context():
    db.create_all()
    
    # Criar usuário admin se não existir
    if not User.query.filter_by(username='admin').first():
        admin = User(
            username='admin',
            email='admin@example.com',
            is_admin=True
        )
        admin.set_password('admin123')  # Mude esta senha!
        db.session.add(admin)
        db.session.commit()

if __name__ == "__main__":
    app.run() 