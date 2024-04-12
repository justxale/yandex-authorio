from flask import Flask, render_template, redirect
from flask_login import LoginManager, logout_user, login_required, current_user, login_user

from data.models.features import Post, SubLevel
from data.models.users import User, Role, Author
from data import db_session, consts
from forms.loginform import LoginForm
from forms.posts import AddPostForm
from forms.user import RegisterForm, ChangeSettingsForm, BecomeAuthorForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tkLhOynXewZuVQmJIpVJOUlhqNwVxHnI'

login_manager = LoginManager()
login_manager.init_app(app)


class FreshPost:
    def __init__(self, title, content, author_name, created_date):
        self.title = title
        self.content = content
        self.author = author_name
        self.created_date = created_date


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.get(User, user_id)


@app.route('/')
@app.route('/index')
def index():
    db_sess = db_session.create_session()
    posts = db_sess.query(Post).all()
    new_posts = []
    print(current_user.is_author())
    for post in posts:
        try:
            new_posts.append(FreshPost(post.title, post.content, post.author.display_name, post.created_date.date()))
        except AttributeError as e:
            print(f'An error occured: {e}')

    #if current_user.is_authenticated:
    #    return render_template("posts_view.html", posts=new_posts)
    # return render_template("welcome_page.html", posts=new_posts)
    return render_template("posts_view.html", posts=new_posts)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    print('Boo!')
    return redirect("/")


@app.route("/settings_page")
@login_required
def settings_page():
    return render_template("settings_page.html")


@app.route('/change_settings', methods=['GET', 'POST'])
@login_required
def change_settings():
    form = ChangeSettingsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == current_user.email).first()
        user.name = form.name.data
        user.about = form.about.data
        db_sess.commit()
        return redirect('/settings_page')
    return render_template('change_settings.html', form=form)


@app.route('/<string:username>')
def author_page(username: str):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.name == username).first()
    print('boo', user)

    posts = db_sess.query(Post).filter(Post.author_id == user.author_id)
    levels = db_sess.query(SubLevel).filter(SubLevel.author_id == user.author_id)
    return render_template(
        'profile_page.html', title=f'Страница {user.name}',
        user=user, has_admin_permissions=(user == current_user),
        posts=posts, levels=levels
    )


@app.route('/addpost', methods=['GET', 'POST'])
@login_required
def add_post():
    form = AddPostForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        post = Post(
            title=form.title.data, content=form.about.data, author_id=current_user.id
        )
        db_sess.add(post)
        db_sess.commit()
        return redirect(f"/{current_user.name}")
    return render_template(
        'forms/add_post.html', title='Создание поста', form=form
    )


@app.route('/becomecreator', methods=['GET', 'POST'])
@login_required
def become_creator():
    form = BecomeAuthorForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        author = Author(
            display_name=form.display_name.data, about=form.about.data
        )
        db_sess.add(author)
        db_sess.query(User).filter(User.id == current_user.id).update({"author": author})
        db_sess.commit()

        return redirect(f"/{current_user.name}")
    return render_template(
        'forms/become_creator.html', title='Регистрация нового автора', form=form
    )


def main():
    db_session.global_init("db/users.sqlite")

    session = db_session.create_session()

    for role_name in consts.ALL_ROLES:
        role = Role(
            name=role_name
        )
        session.add(role)
    user = User(name=consts.AUTO_USER['name'])
    user.set_password(consts.AUTO_USER['password'])
    session.add(user)
    author = Author(display_name=user.name, about='Boo!')
    session.add(author)

    try:
        session.commit()
    except:
        pass


if __name__ == '__main__':
    main()
    app.run(port=8080, host='127.0.0.1', debug=True)
