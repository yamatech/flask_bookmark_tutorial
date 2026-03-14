from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bookmarks.db"
db = SQLAlchemy(app)


class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    url = db.Column(db.String(500), nullable=False)


@app.route("/")
def index():
    bookmark_list = Bookmark.query.all()
    return render_template("index.html", bookmark_list=bookmark_list)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        title = request.form["title"].strip()
        url = request.form["url"].strip()
        if not title or not url:
            return render_template("add.html")
        bookmark_item = Bookmark(title=title, url=url)
        db.session.add(bookmark_item)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("add.html")


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    bookmark_item = Bookmark.query.get_or_404(id)
    if request.method == "POST":
        title = request.form["title"].strip()
        url = request.form["url"].strip()
        if not title or not url:
            return render_template("edit.html", bookmark_item=bookmark_item)
        bookmark_item.title = title
        bookmark_item.url = url
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("edit.html", bookmark_item=bookmark_item)


@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    bookmark_item = Bookmark.query.get_or_404(id)
    db.session.delete(bookmark_item)
    db.session.commit()
    return redirect(url_for("index"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
