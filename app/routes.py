from flask import Blueprint, render_template, request, redirect, url_for
from app.models import Article
from app import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    search = request.args.get('search', '')
    if search:
        articles = Article.query.filter(
            (Article.title.contains(search)) | 
            (Article.content.contains(search))
        ).all()
    else:
        articles = Article.query.all()
    return render_template('index.html', articles=articles)

@main.route('/article/new', methods=['GET', 'POST'])
def new_article():
    if request.method == 'POST':
        content = request.form['content'].strip()
        print("DEBUG - Novo Artigo:")
        print(f"Título: {request.form['title']}")
        print(f"Conteúdo recebido: {content}")
        
        article = Article(
            title=request.form['title'],
            content=content,
            category=request.form['category'],
            tags=request.form['tags']
        )
        
        db.session.add(article)
        db.session.commit()
        
        # Verificar se foi salvo corretamente
        saved_article = Article.query.get(article.id)
        print(f"Conteúdo salvo no banco: {saved_article.content}")
        
        return redirect(url_for('main.index'))
    return render_template('article_form.html')

@main.route('/article/<int:id>')
def view_article(id):
    article = Article.query.get_or_404(id)
    print("DEBUG - Dados do Artigo:")
    print(f"ID: {article.id}")
    print(f"Título: {article.title}")
    print(f"Categoria: {article.category}")
    print(f"Conteúdo: {article.content}")
    return render_template('article.html', article=article)

@main.route('/article/<int:id>/edit', methods=['GET', 'POST'])
def edit_article(id):
    article = Article.query.get_or_404(id)
    
    if request.method == 'POST':
        article.title = request.form['title']
        article.content = request.form['content']
        article.category = request.form['category']
        article.tags = request.form['tags']
        
        db.session.commit()
        return redirect(url_for('main.view_article', id=article.id))
    
    return render_template('article_edit.html', article=article)

@main.route('/article/<int:id>/delete', methods=['POST'])
def delete_article(id):
    article = Article.query.get_or_404(id)
    db.session.delete(article)
    db.session.commit()
    return redirect(url_for('main.index')) 