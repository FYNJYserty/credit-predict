from flask import Flask

app = Flask(
    __name__,
    template_folder="app/templates",
    static_folder="app/static"
)

from app.routes import bp

app.register_blueprint(bp)

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
