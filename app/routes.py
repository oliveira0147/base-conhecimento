from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Article, User, Role, Permission, Category, Tag
from app import db
from flask_login import login_required, current_user
from functools import wraps
from app.forms import TagForm, ArticleForm

main = Blueprint('main', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Acesso negado. Você precisa ser administrador.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@main.route('/')
def index():
    search = request.args.get('search', '')
    if search:
        articles = Article.query.filter(
            (Article.title.ilike(f'%{search}%')) |
            (Article.content.ilike(f'%{search}%'))
        ).order_by(Article.created_at.desc()).all()
    else:
        articles = Article.query.order_by(Article.created_at.desc()).all()
    
    # Removendo todas as informações de debug
    return render_template('index.html', 
                         articles=articles, 
                         search=search)

@main.route('/article/new', methods=['GET', 'POST'])
@login_required
def new_article():
    # Criar uma instância do formulário
    form = ArticleForm()
    
    if form.validate_on_submit():
        article = Article(
            title=form.title.data,
            content=form.content.data,
            user_id=current_user.id,
            category_id=form.category_id.data if form.category_id.data != 0 else None
        )
        
        # Adiciona tags
        if form.tag_ids.data:
            selected_tags = Tag.query.filter(Tag.id.in_(form.tag_ids.data)).all()
            article.tags = selected_tags
            
        db.session.add(article)
        db.session.commit()
        flash('Artigo criado com sucesso!', 'success')
        return redirect(url_for('main.index'))
    
    # Passar o formulário para o template
    return render_template('article_form.html', form=form)

@main.route('/article/<int:id>')
def view_article(id):
    article = Article.query.get_or_404(id)
    print("DEBUG - Dados do Artigo:")
    print(f"ID: {article.id}")
    print(f"Título: {article.title}")
    print(f"Categoria: {article.category_rel.name if article.category_rel else 'Sem categoria'}")
    return render_template('article.html', article=article)

@main.route('/article/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_article(id):
    article = Article.query.get_or_404(id)
    
    # Verificar se o usuário é o autor ou admin
    if article.user_id != current_user.id and not current_user.is_admin:
        flash('Você não tem permissão para editar este artigo.', 'danger')
        return redirect(url_for('main.index'))
    
    # Buscar todas as categorias e tags
    categories = Category.query.order_by(Category.name).all()
    tags = Tag.query.order_by(Tag.name).all()
    
    if request.method == 'POST':
        article.title = request.form['title']
        article.content = request.form['content']
        
        # Atualiza categoria
        category_id = request.form.get('category_id')
        if category_id:
            article.category_id = int(category_id)
        else:
            article.category_id = None
            
        # Atualiza tags
        tag_ids = request.form.getlist('tag_ids')
        if tag_ids:
            selected_tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
            article.tags = selected_tags
        else:
            article.tags = []
            
        db.session.commit()
        flash('Artigo atualizado com sucesso!', 'success')
        return redirect(url_for('main.view_article', id=article.id))
    
    # Quando for GET, passa o artigo, categorias e tags para o template
    return render_template('article_form.html', 
                         article=article,
                         categories=categories,
                         tags=tags)

@main.route('/article/<int:id>/delete', methods=['POST'])
@login_required
def delete_article(id):
    article = Article.query.get_or_404(id)
    
    # Verifica se o usuário é o autor ou admin
    if not (current_user == article.author or current_user.is_admin):
        flash('Você não tem permissão para excluir este artigo.', 'danger')
        return redirect(url_for('main.view_article', id=article.id))
    
    db.session.delete(article)
    db.session.commit()
    flash('Artigo excluído com sucesso!', 'success')
    return redirect(url_for('main.index'))

@main.route('/admin/users')
@login_required
@admin_required
def manage_users():
    users = User.query.all()
    roles = Role.query.all()
    return render_template('admin/users.html', users=users, roles=roles)

@main.route('/admin/users/<int:id>/role', methods=['POST'])
@login_required
@admin_required
def update_user_role(id):
    user = User.query.get_or_404(id)
    role_id = request.form.get('role_id')
    
    if role_id:
        role = Role.query.get(role_id)
        if role:
            user.role = role
            db.session.commit()
            flash(f'Cargo de {user.username} atualizado para {role.name}', 'success')
        else:
            flash('Cargo não encontrado', 'danger')
    else:
        user.role = None
        db.session.commit()
        flash(f'Cargo de {user.username} removido', 'success')
    
    return redirect(url_for('main.manage_users'))

@main.route('/admin/users/<int:id>/toggle-admin', methods=['POST'])
@login_required
@admin_required
def toggle_admin(id):
    if current_user.id == id:
        flash('Você não pode remover seus próprios privilégios de admin', 'danger')
        return redirect(url_for('main.manage_users'))
        
    user = User.query.get_or_404(id)
    user.is_admin = not user.is_admin
    db.session.commit()
    
    status = 'adicionado' if user.is_admin else 'removido'
    flash(f'Status de administrador {status} para {user.username}', 'success')
    return redirect(url_for('main.manage_users'))

@main.route('/admin/roles')
@login_required
@admin_required
def manage_roles():
    roles = Role.query.all()
    permissions = Permission.query.all()
    return render_template('admin/roles.html', roles=roles, permissions=permissions)

@main.route('/admin/roles/new', methods=['GET', 'POST'])
@login_required
@admin_required
def new_role():
    if request.method == 'POST':
        role = Role(
            name=request.form['name'],
            description=request.form['description']
        )
        permission_ids = request.form.getlist('permissions')
        permissions = Permission.query.filter(Permission.id.in_(permission_ids)).all()
        role.permissions = permissions
        db.session.add(role)
        db.session.commit()
        flash('Cargo criado com sucesso!', 'success')
        return redirect(url_for('main.manage_roles'))
    
    permissions = Permission.query.all()
    return render_template('admin/role_form.html', permissions=permissions)

@main.route('/admin/roles/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_role(id):
    role = Role.query.get_or_404(id)
    if request.method == 'POST':
        role.name = request.form['name']
        role.description = request.form['description']
        permission_ids = request.form.getlist('permissions')
        permissions = Permission.query.filter(Permission.id.in_(permission_ids)).all()
        role.permissions = permissions
        db.session.commit()
        flash('Cargo atualizado com sucesso!', 'success')
        return redirect(url_for('main.manage_roles'))
    
    permissions = Permission.query.all()
    return render_template('admin/role_form.html', role=role, permissions=permissions)

@main.route('/admin/roles/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_role(id):
    role = Role.query.get_or_404(id)
    
    if role.name == 'Admin':
        flash('O cargo de Admin não pode ser deletado.', 'danger')
        return redirect(url_for('main.manage_roles'))
    
    users_with_role = User.query.filter_by(role_id=role.id).all()
    for user in users_with_role:
        user.role = None
    
    db.session.delete(role)
    db.session.commit()
    flash('Cargo deletado com sucesso!', 'success')
    return redirect(url_for('main.manage_roles'))

@main.route('/admin/users/<int:id>/articles')
@login_required
@admin_required
def user_articles(id):
    user = User.query.get_or_404(id)
    articles = Article.query.filter_by(user_id=user.id).order_by(Article.created_at.desc()).all()
    return render_template('admin/user_articles.html', user=user, articles=articles)

@main.route('/admin/categories')
@login_required
@admin_required
def manage_categories():
    categories = Category.query.all()
    return render_template('admin/categories.html', categories=categories)

@main.route('/admin/categories/new', methods=['GET', 'POST'])
@login_required
@admin_required
def new_category():
    if request.method == 'POST':
        category = Category(
            name=request.form['name'],
            description=request.form['description']
        )
        db.session.add(category)
        db.session.commit()
        flash('Categoria criada com sucesso!', 'success')
        return redirect(url_for('main.manage_categories'))
    return render_template('admin/category_form.html')

@main.route('/admin/categories/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_category(id):
    category = Category.query.get_or_404(id)
    if request.method == 'POST':
        category.name = request.form['name']
        category.description = request.form['description']
        db.session.commit()
        flash('Categoria atualizada com sucesso!', 'success')
        return redirect(url_for('main.manage_categories'))
    return render_template('admin/category_form.html', category=category)

@main.route('/admin/categories/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_category(id):
    category = Category.query.get_or_404(id)
    db.session.delete(category)
    db.session.commit()
    flash('Categoria deletada com sucesso!', 'success')
    return redirect(url_for('main.manage_categories'))

@main.route('/admin/tags')
@login_required
@admin_required
def manage_tags():
    tags = Tag.query.all()
    return render_template('admin/tags.html', tags=tags)

@main.route('/admin/tags/new', methods=['GET', 'POST'])
@login_required
@admin_required
def new_tag():
    form = TagForm()
    if form.validate_on_submit():
        tag = Tag(
            name=form.name.data,
            description=form.description.data
        )
        db.session.add(tag)
        db.session.commit()
        flash('Tag criada com sucesso!', 'success')
        return redirect(url_for('main.manage_tags'))
    return render_template('admin/tag_form.html', form=form)

@main.route('/admin/tags/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_tag(id):
    tag = Tag.query.get_or_404(id)
    form = TagForm(obj=tag)
    
    if form.validate_on_submit():
        tag.name = form.name.data
        tag.description = form.description.data
        db.session.commit()
        flash('Tag atualizada com sucesso!', 'success')
        return redirect(url_for('main.manage_tags'))
    return render_template('admin/tag_form.html', form=form, tag=tag)

@main.route('/admin/tags/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_tag(id):
    tag = Tag.query.get_or_404(id)
    db.session.delete(tag)
    db.session.commit()
    flash('Tag deletada com sucesso!', 'success')
    return redirect(url_for('main.manage_tags')) 