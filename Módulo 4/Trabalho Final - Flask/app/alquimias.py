from datetime import datetime
from sqlalchemy import select, desc
from app import db
from app.models.models import User, Post
from werkzeug.security import generate_password_hash, check_password_hash

def validate_user_password(username, password):
    ''' Testa se o usuário e senha correspondem a um registro no banco '''
    # ATENÇÃO o comando utilizado é SCALAR não SCALARS, logo ele retorna só o 1° resultado
    user = db.session.scalar(select(User).where(User.username == username))
    if user and check_password_hash(user.password, password):
        return user
    else: return None

def user_existis(username):
    ''' Testa se o usuário informado corresponde a um registro no banco '''
    user = db.session.scalar(select(User).where(User.username == username))
    return user

def create_user(username, password, img_URL=None, bio=None, remember=False, last_login=None):
    ''' Cria um usuário salvando sua senha em código hash '''
    password_hash = generate_password_hash(str(password))
    new_user = User(
        username = username,
        password = password_hash,
        img_URL = img_URL,
        bio = bio,
        remember = remember,
        last_login = last_login if last_login else datetime.now()
    )

    db.session.add(new_user)
    db.session.commit()
    return new_user

def update_remember(username, remember):
    user = db.session.scalar(select(User).where(User.username == username))
    user.remember = remember

    db.session.add(user)
    db.session.commit()
    return user


def create_post(body, user_id):
    ''' Cria um post e salvano banco relacionando-o ao usuário que o escreveu '''
    new_post = Post(
        body=body, 
        timestamp=datetime.now(), 
        user_id=user_id
        )
    
    db.session.add(new_post)
    db.session.commit()
    return new_post

def get_timeline():
    ''' Retorna os 5 posts mais recentes '''
    query = select(Post).order_by(desc(Post.timestamp))
    timeline = db.session.scalars(query).fetchmany(5)

    return timeline