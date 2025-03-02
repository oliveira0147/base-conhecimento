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
        article = Article(
            title=request.form['title'],
            content=request.form['content'],
            category=request.form['category'],
            tags=request.form['tags']
        )
        db.session.add(article)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('article_form.html')

@main.route('/article/<int:id>')
def view_article(id):
    article = Article.query.get_or_404(id)
    return render_template('article.html', article=article) 