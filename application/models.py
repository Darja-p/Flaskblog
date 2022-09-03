from application import db, login_manager
from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from flask_login import UserMixin
import jwt
from datetime import datetime, timezone, timedelta

# adding posts.csv to the database using pandas
# posts = pd.read_csv('posts.csv')
#
# for index, row in posts.iterrows():
#     new_post = BlogPost(id =row['id'], title =row['title'],img_url= row['img_url'], subtitle=row['subtitle'],body= row['body'], date= row['date'])
#     db.session.add(new_post)
#     db.session.commit()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

##CONFIGURE TABLE- Parent
class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250),unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    posts = relationship("BlogPost", back_populates='author')
    comments = relationship("Comment", back_populates='comment_author')

    def __repr__(self):
        return f'User({self.id}, {self.name}, {self.email})'

    def get_reset_token(self,expires_sec=1800):
        reset_token = jwt.encode({"user_id": self.id, "exp": datetime.now(timezone.utc) + timedelta(seconds =expires_sec)}, current_app.config["SECRET_KEY"], algorithm = "HS256")
        return reset_token


    def verify_reset_token(token):
        try:
            data = jwt.decode(token, current_app.config["SECRET_KEY"],leeway=timedelta(seconds=10), algorithms=['HS256'])
            user_id = data.get("user_id")
        except:
            return None
        return User.query.get(user_id)


##CONFIGURE TABLE - child
class BlogPost(db.Model):
    __tablename__ = 'blog_posts'
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, ForeignKey('users.id'))
    author = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates='post')

    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, ForeignKey('users.id'))
    post_id = db.Column(db.Integer, ForeignKey('blog_posts.id'))
    comment_author = relationship("User", back_populates="comments")
    comment = db.Column(db.Text, nullable=False)
    post = relationship("BlogPost", back_populates="comments")