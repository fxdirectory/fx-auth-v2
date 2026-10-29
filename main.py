from flask import Flask
from conf.config import Config
from routes.auth_routes import auth_bp
from routes.user_routes import user_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)

    @app.get("/")
    def index():
        return {
            "service": "auth-microservice",
            "endpoints": [
                "POST /api/auth/login",
                "POST /api/auth/logout",
                "POST /api/users/register",
                "GET  /api/users/me (perlu token)",
                "GET  /api/users/ (admin saja)",
            ],
        }
    return app

app = create_app()
if __name__ == "__main__":
    app.run(host=Config.APP_HOST, port=Config.APP_PORT, debug=True)
