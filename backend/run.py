from app import create_app
from flask_jwt_extended import create_access_token

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
