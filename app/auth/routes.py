from flask import render_template, redirect, url_for, flash, request, Blueprint
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models import User, Role
from app.forms import RegistrationForm

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('main.index'))
            
        flash('Usuário ou senha inválidos', 'danger')
    return render_template('auth/login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        # Verifica se o usuário já existe
        if User.query.filter_by(username=form.username.data).first():
            flash('Este nome de usuário já está em uso.', 'danger')
            return render_template('auth/register.html', title='Registro', form=form)
        
        # Verifica se o email já existe
        if User.query.filter_by(email=form.email.data).first():
            flash('Este email já está em uso.', 'danger')
            return render_template('auth/register.html', title='Registro', form=form)
        
        # Cria novo usuário
        user = User(
            username=form.username.data,
            email=form.email.data,  # Adicionado email
            password_hash=generate_password_hash(form.password.data)
        )
        db.session.add(user)
        db.session.commit()
        
        flash('Registro realizado com sucesso!', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', title='Registro', form=form) 