from app import create_app
from app.services.facade import bootstrap_admin

app = create_app()
bootstrap_admin()

if __name__ == '__main__':
    app.run(debug=True)
