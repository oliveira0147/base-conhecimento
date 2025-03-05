from app import create_app, db
from app.models import User, Article, Category, Tag
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash

app = create_app()
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Article': Article,
        'Category': Category,
        'Tag': Tag
    }

if __name__ == '__main__':
    with app.app_context():
        # Primeiro, vamos remover qualquer usuário admin existente
        admin = User.query.filter_by(username='admin').first()
        if admin:
            db.session.delete(admin)
            db.session.commit()
        
        # Agora vamos criar um novo admin
        new_admin = User(
            username='admin',
            email='admin@admin.com',
            password_hash=generate_password_hash('admin'),
            is_admin=True
        )
        db.session.add(new_admin)
        db.session.commit()
        
        # Verificar se foi criado
        admin = User.query.filter_by(username='admin').first()
        if admin:
            print("Admin criado com sucesso!")
            print(f"Username: {admin.username}")
            print(f"Email: {admin.email}")
            print(f"Is Admin: {admin.is_admin}")
    app.run(debug=True) 