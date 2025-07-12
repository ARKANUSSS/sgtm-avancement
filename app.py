from flask import Flask, render_template, redirect, url_for, flash, request, abort
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from models import db, User, Post
from forms import LoginForm, PostForm
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Connexion réussie!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Identifiants incorrects.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
@login_required
def home():
    form = PostForm()
    can_write = not current_user.is_admin
    
    posts = []
    if current_user.is_admin:
        posts = Post.query.order_by(Post.timestamp.desc()).all()
    else:
        posts = Post.query.filter_by(user_id=current_user.id).order_by(Post.timestamp.desc()).all()
    
    if form.validate_on_submit() and can_write:
        post = Post(content=form.content.data, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        flash('Message publié.', 'success')
        return redirect(url_for('home'))
    
    return render_template('index.html', posts=posts, form=form, can_write=can_write)

@app.route('/delete_post/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if not current_user.is_admin:
        abort(403)  # ممنوع على غير الادمن
    db.session.delete(post)
    db.session.commit()
    flash('Message supprimé avec succès.', 'success')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
