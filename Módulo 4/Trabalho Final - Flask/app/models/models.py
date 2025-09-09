
from typing import Optional
from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from flask_login import UserMixin
from flask import url_for
from app import db, login

# Link para a imagem padrão caso a pessoa não coloque o link da foto de perfil
default_img = "https://i.pinimg.com/236x/31/ec/2c/31ec2ce212492e600b8de27f38846ed7.jpg"

class User(UserMixin, db.Model):
    ''' Classe de dados para o armazenamento das informações dos usuários no banco

    -------------------- Atributos --------------------

        --> id: Número de identificação do usuário

        --> username: Nome de usuário que é único para cada um

        --> password: Senha de usuário

        --> img_URL: URL da imagem de perfil

        --> bio: Biografia do usuário

        --> remember: Se o navegador deve manter o login

        --> last_login: Última vez que o usuário fez login
    '''
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    img_URL: Mapped[str] = mapped_column(nullable=False, default=default_img)
    bio: Mapped[str] = mapped_column()
    remember: Mapped[bool] = mapped_column(default=False)
    last_login: Mapped[datetime] = mapped_column()
    posts: Mapped[list["Post"]] = relationship(back_populates="author")
    

    @login.user_loader
    def load_user(id):
        return db.session.get(User, int(id))
    

class Post(db.Model):
    ''' Classe de dados para os posts dos usuários

    -------------------- Atributos --------------------

        --> id: Número de identificação do post

        --> body: Texto contido no post

        --> timestamp: Momento em que foi feito o post

        --> user_id: Referência ao usuário que escreveu o post
    '''

    __tablename__ = "posts"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    body: Mapped[str] = mapped_column(nullable=False)
    timestamp: Mapped[datetime] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    author: Mapped["User"] = relationship(back_populates="posts")

    def get_strDate(self):
        ''' Função que retorna o timestamp do post em formato de string formatada '''
        date= self.timestamp
        str_date = date.strftime("%d/%m/%Y – %H:%M")
        return str_date