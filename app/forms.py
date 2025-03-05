from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from app.models import Category, Tag

class LoginForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Entrar')

class RegistrationForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired()])
    password2 = PasswordField('Confirmar Senha', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrar')

class CategoryForm(FlaskForm):
    name = StringField('Nome', validators=[DataRequired()])
    description = TextAreaField('Descrição')
    submit = SubmitField('Salvar')

class TagForm(FlaskForm):
    name = StringField('Nome', validators=[DataRequired()])
    description = TextAreaField('Descrição')
    submit = SubmitField('Salvar')

class ArticleForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired()])
    content = TextAreaField('Conteúdo', validators=[DataRequired()])
    category_id = SelectField('Categoria', coerce=int)
    tag_ids = SelectMultipleField('Tags', coerce=int)
    submit = SubmitField('Salvar')

    def __init__(self, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
        self.category_id.choices = [(0, 'Selecione uma categoria')] + [
            (c.id, c.name) for c in Category.query.order_by('name')
        ]
        self.tag_ids.choices = [(t.id, t.name) for t in Tag.query.order_by('name')] 