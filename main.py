from app import initialize_app
import config

flask_app = initialize_app()
conf = config.Config()

if __name__ == "__main__":
    flask_app.run(host=conf.HOST, port=conf.PORT)
