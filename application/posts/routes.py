from flask import render_template, request, redirect, url_for, flash, Blueprint
from flask_login import current_user
from datetime import datetime
from application import db
from application.models import BlogPost, Comment
from application.posts.forms import AddComment, CreatePostForm
from application.users.utils import admin_only


posts = Blueprint('posts', __name__)

@posts.route('/posts/<num>', methods = ["GET", "POST"])
def get_post(num):
    blog = BlogPost.query.get(int(num))
    form = AddComment()

    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("You need to login or register to comment.")
            return redirect(url_for("users.login"))
        comment_to_add = Comment(comment = request.form['comment'], author_id = current_user.id, post_id = blog.id)
        db.session.add(comment_to_add)
        db.session.commit()
    return render_template("post.html", post=blog, form=form)


@posts.route('/new-post', methods=["GET", "POST"])
@admin_only
def create_post():
    form = CreatePostForm(author=current_user.id)
    if form.validate_on_submit():
        new_post = BlogPost(title = request.form['title'], subtitle = request.form['subtitle'],
                            date =datetime.today().strftime('%Y-%m-%d'),body=request.form['body'],
                            author= current_user, img_url =request.form['img_url'])
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('main.home'))
    return render_template("make-post.html", form=form, edit="new")

@posts.route('/edit-post/<num>', methods=["GET", "POST"])
@admin_only
def edit_post(num):
    post_to_edit = BlogPost.query.get(num)
    form = CreatePostForm(title=post_to_edit.title,  subtitle=post_to_edit.subtitle,img_url=post_to_edit.img_url,
                        body=post_to_edit.body)
    if request.method == "POST" and form.validate_on_submit():
        post_to_edit.title = request.form['title']
        post_to_edit.subtitle = request.form['subtitle']
        post_to_edit.body=request.form['body']
        post_to_edit.img_url=request.form['img_url']
        db.session.commit()
        return redirect(url_for('posts.get_post', num=post_to_edit.id))
    return render_template("make-post.html", form=form, edit="not new", post_id=post_to_edit.id)

@posts.route('/delete-post/<num>', methods=["GET", "POST"])
def delete_post(num):
    post_to_delete = BlogPost.query.get(num)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('main.home'))
