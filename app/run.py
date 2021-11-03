from utopia.models.base import init_db
from utopia import app


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', debug=True)