from flask import Flask, request, redirect,render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://build_a_blog:123@localhost:8889/build_a_blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(120))
    body = db.Column(db.Text)
    
    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route("/", methods = ["POST", "GET"])
def index():
    blogs = Blog.query.order_by(Blog.id.desc()).all()
    return render_template("blog.html", blogs = blogs)

@app.route("/blog", methods = ["POST", "GET"])
def blog():
    blogid = request.args.get("id")
    if blogid:
        blog = Blog.query.filter_by(id=blogid).first()
        return render_template("singleblog.html", blog=blog)
    else:
        blogs = Blog.query.order_by(Blog.id.desc()).all()
        return render_template("blog.html", blogs = blogs)

@app.route("/newpost", methods = ["POST", "GET"])
def newpost():
    return render_template("newpost.html")

@app.route("/todos", methods=["POST", "GET"])
def todos():
    title = request.form["title"]
    title_error = ""
    body = request.form["body"]
    body_error = ""

    if title == "":
        title_error = "Why don't you write something?"
        return render_template("newpost.html", title=title, title_error = title_error)
    if body == "":
        body_error = "Why don't you write something?"
        return render_template("newpost.html", body=body, body_error = body_error)
    elif request.method == "POST":
        blogpost = Blog(title, body)
        db.session.add(blogpost)
 #       db.session.flush()
        db.session.commit()

    idnum = blogpost.id
    return redirect("/blog?id={0}".format(idnum))


if __name__ == '__main__':
    app.run()