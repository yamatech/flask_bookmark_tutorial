# models.py

```python
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Bookmark(db.Model):
    __tablename__ = "bookmarks"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    url = db.Column(db.String(2048), nullable=False)
    description = db.Column(db.Text, default="")
    tag = db.Column(db.String(100), default="")
    created_at = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f"<Bookmark {self.title}>"
```
