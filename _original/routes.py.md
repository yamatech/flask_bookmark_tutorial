# routes.py

```python
from flask import Blueprint, render_template, request, redirect, url_for
from models import db, Bookmark

bp = Blueprint("bookmarks", __name__)


@bp.route("/")
def index():
    tag_filter = request.args.get("tag", "")
    search = request.args.get("search", "")

    query = Bookmark.query

    if tag_filter:
        query = query.filter(Bookmark.tag == tag_filter)
    if search:
        like = f"%{search}%"
        query = query.filter(
            db.or_(
                Bookmark.title.ilike(like),
                Bookmark.url.ilike(like),
                Bookmark.description.ilike(like),
            )
        )

    bookmarks = query.order_by(Bookmark.created_at.desc()).all()

    tags = (
        db.session.query(Bookmark.tag)
        .filter(Bookmark.tag != "")
        .distinct()
        .order_by(Bookmark.tag)
        .all()
    )

    return render_template(
        "index.html",
        bookmarks=bookmarks,
        tags=[t.tag for t in tags],
        current_tag=tag_filter,
        search=search,
    )


@bp.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        url = request.form.get("url", "").strip()
        description = request.form.get("description", "").strip()
        tag = request.form.get("tag", "").strip()

        if not title or not url:
            return redirect(url_for("bookmarks.index"))

        if not url.startswith(("http://", "https://")):
            url = "https://" + url

        bookmark = Bookmark(title=title, url=url, description=description, tag=tag)
        db.session.add(bookmark)
        db.session.commit()
        return redirect(url_for("bookmarks.index"))

    tags = (
        db.session.query(Bookmark.tag)
        .filter(Bookmark.tag != "")
        .distinct()
        .order_by(Bookmark.tag)
        .all()
    )

    return render_template("add.html", tags=[t.tag for t in tags])


@bp.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    bookmark = db.get_or_404(Bookmark, id)
    db.session.delete(bookmark)
    db.session.commit()
    return redirect(url_for("bookmarks.index"))


@bp.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    bookmark = db.get_or_404(Bookmark, id)

    if request.method == "POST":
        bookmark.title = request.form.get("title", "").strip()
        bookmark.url = request.form.get("url", "").strip()
        bookmark.description = request.form.get("description", "").strip()
        bookmark.tag = request.form.get("tag", "").strip()

        if not bookmark.url.startswith(("http://", "https://")):
            bookmark.url = "https://" + bookmark.url

        db.session.commit()
        return redirect(url_for("bookmarks.index"))

    return render_template("edit.html", bookmark=bookmark)
```
