from flask import render_template, request, Blueprint
from application.models import BlogPost
from application.users.utils import sent_contact_email


main = Blueprint('main', __name__)



@main.route('/', methods=['GET'])
def home():
    print(request.url)
    page_next = request.args.get('page', 1, type=int)
    print("next", page_next)
    #order by date is not working as currently date is a string, needs to bechanged to the DateTime field(re-do the table)
    blogs = BlogPost.query.order_by(BlogPost.date.desc()).paginate(page=page_next, per_page=3)
    print(blogs.page)
    return render_template("index.html", posts=blogs)

@main.route('/about')
def about_me():
    return render_template("about.html")

@main.route('/contacts',methods=['GET','POST'])
def contacts():
    if request.method == "POST":
        data = [request.form['username'],request.form['email'],request.form['phone'], request.form['message']]
        sent_contact_email(data)
        return render_template("contact.html", message="Successfully sent your message")
    return render_template("contact.html", message="Contact Me")