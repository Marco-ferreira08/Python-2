''' Módulo contendo as rotas da página

-------------------- Rotas --------------------

    --> "/" = index: Página Inicial
    --> "/login" = login: Página de Login
    --> "/cadastro" = cadastro: Página de cadastro de usuário
    --> "/logout" = logout: Rota para Logout
    --> "/post" = post: Página para escrever posts
'''
from flask import (
    render_template, 
    request, redirect, 
    url_for, 
    flash #! Tem como usar mas não sei como usar
    )
from flask_login import (
    current_user,
    login_user,
    logout_user,
    login_required
)
from werkzeug.security import generate_password_hash, check_password_hash
# Sim, é só esse import para disparar o __init__.py
# e recuperar a referência do objeto Flask
from app import app
from app import alquimias
from app.models.models import Post, User

@app.route("/")
@login_required
def index():
    ''' Página incial que exibe dados do usuário e timeline de posts (requer login) '''
    if current_user.is_authenticated:
        user = current_user

    timeline = alquimias.get_timeline()

    if type(timeline) == list:
        for post in timeline:
            if type(post) != Post:
                timeline.remove(post)
    else: timeline = []

    return render_template(
        "index.html", # página existente na pasta
        title="Página Inicial", # atributo dinâmico
        user=user, # atributo dinâmico user
        timeline=timeline, # timeline com os 5 posts mais recentes
    )

@app.route("/login", methods=["GET", "POST"])
def login():
    ''' Página com formulário de login '''
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        remember = True if request.form.get("remember") == "on" else False
        

        user = alquimias.validate_user_password(username, password)

        if user:
            flash("Login bem sucedido!", category="success_message")
            ########## Efetivando Login ##########
            login_user(user, remember=user.remember)
            ######################################
            
            if user.remember != remember:
                alquimias.update_remember(username, remember)
            return redirect(url_for("index"))
        else:
            flash("Usuário ou senha inválidos!", category="error")
            return render_template("login.html", title="Login")

    else:
        # request.method == "GET"
        return render_template("login.html", title="Login")
    
@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    ''' Página com formulário para criação de conta de usuário '''
    if current_user.is_authenticated:
        return redirect(url_for("index"))


    if request.method == "POST":
        username = request.form["username"]
        password = str(request.form["password"])
        confirm_password = str(request.form["confirm_password"])

        if alquimias.user_existis(username):
            flash("Usuário já existe!", category="error")
            return render_template("cadastro.html", title="Cadastro")
        
        elif len(password) < 5:
            flash("A senha deve ter pelo menos 5 caracteres.", category="error")
            return render_template("cadastro.html", title="Cadastro")

        elif password != confirm_password:
            flash("A senha e a confirmação estão diferentes.", category="error")
            return render_template("cadastro.html", title="Cadastro")

        else:
            username = username
            password = password
            img_URL = request.form.get("img_URL")
            bio = request.form.get("bio")
            remember = True if request.form.get("remember") == "on" else False
            user = alquimias.create_user(
                username=username,
                password=password,
                img_URL=img_URL if img_URL != "" else url_for("static", filename="images/no_profile_img.jpg"),
                bio=bio,
                remember=remember,
                )
            flash("Conta criada com sucesso!", category="success_message")
            ########### Efetivando Login ###########
            login_user(user, remember=user.remember)
            ########################################
            return redirect(url_for("index"))
    
    else:
        return render_template("cadastro.html", title="Cadastro")
    
@app.route("/logout")
def logout():
    ''' Desconecta o usuário de sua conta '''
    logout_user()
    return redirect(url_for(f"login"))

@app.route("/post", methods=["GET", "POST"])
@login_required
def post():
    ''' Página com formulário para escrever posts (requer login) '''
    if current_user.is_authenticated:
        if request.method == "POST":
                post_body = request.form.get("post_body")
                user_id = current_user.id

                post = alquimias.create_post(
                    body=post_body,
                    user_id=user_id 
                )

                if post:
                    flash("Post criado com sucesso!", category="success_message")
                else:
                    flash("Erro ao criar post.", category="error")
                
                return redirect(url_for(f"index"))

        else:
            return render_template("post.html", title="Post",)