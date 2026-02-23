# app.py

```python
import os
from flask import Flask
from models import db
from routes import bp


def create_app():
    app = Flask(__name__)

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DB_DIR = os.path.join(BASE_DIR, 'db')
    os.makedirs(DB_DIR, exist_ok=True)

    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(DB_DIR, 'bookmarks.db')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    app.register_blueprint(bp)

    with app.app_context():
        db.create_all()

    return app


if __name__ == '__main__':
    app = create_app()
    # host='0.0.0.0' で同じLAN内の他のデバイスからもアクセス可能
    app.run(debug=True, host='0.0.0.0', port=5000)
```
