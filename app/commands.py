import click
from flask.cli import with_appcontext
from app import db
from app.models import User, Permission, Role

@click.command('init-admin')
@with_appcontext
def init_admin():
    """Initialize admin user and basic roles."""
    
    # Criar permissões básicas
    permissions = [
        ('manage_roles', 'Gerenciar cargos e permissões'),
        ('create_article', 'Criar artigos'),
        ('edit_article', 'Editar artigos'),
        ('delete_article', 'Excluir artigos'),
        ('view_article', 'Visualizar artigos'),
    ]
    
    for name, description in permissions:
        if not Permission.query.filter_by(name=name).first():
            permission = Permission(name=name, description=description)
            db.session.add(permission)
    
    # Criar roles básicas
    roles = [
        ('Admin', 'Administrador do sistema', True),
        ('Editor', 'Editor de conteúdo', ['create_article', 'edit_article', 'view_article']),
        ('Autor', 'Autor de artigos', ['create_article', 'view_article']),
        ('Leitor', 'Leitor de artigos', ['view_article']),
    ]
    
    for name, description, permissions_list in roles:
        role = Role.query.filter_by(name=name).first()
        if not role:
            role = Role(name=name, description=description)
            if permissions_list is True:  # Admin recebe todas as permissões
                role.permissions = Permission.query.all()
            else:
                role.permissions = Permission.query.filter(
                    Permission.name.in_(permissions_list)
                ).all()
            db.session.add(role)
    
    # Criar usuário admin
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(
            username='admin',
            email='admin@example.com',
            is_admin=True
        )
        admin.set_password('admin')
        admin.role = Role.query.filter_by(name='Admin').first()
        db.session.add(admin)
    
    db.session.commit()
    click.echo('Admin user and roles created successfully!')
    click.echo('Username: admin')
    click.echo('Password: admin')

@click.command('check-admin')
@with_appcontext
def check_admin():
    """Check admin user status."""
    admin = User.query.filter_by(username='admin').first()
    if admin:
        click.echo(f'Admin exists:')
        click.echo(f'Username: {admin.username}')
        click.echo(f'Is admin: {admin.is_admin}')
        click.echo(f'Role: {admin.role.name if admin.role else "No role"}')
    else:
        click.echo('Admin user not found!')

@click.command('fix-admin')
@with_appcontext
def fix_admin():
    """Fix admin user permissions."""
    admin = User.query.filter_by(username='admin').first()
    if admin:
        admin.is_admin = True
        admin_role = Role.query.filter_by(name='Admin').first()
        if admin_role:
            admin.role = admin_role
        db.session.commit()
        click.echo('Admin permissions fixed!')
    else:
        click.echo('Admin user not found!')

# Adicione o comando no create_app
def create_app():
    
    from app.commands import init_admin, check_admin, fix_admin
    app.cli.add_command(init_admin)
    app.cli.add_command(check_admin)
    app.cli.add_command(fix_admin) 