from src import create_app

app = create_app()

if __name__ == 'apilogin.app':
    app.run(host="0.0.0.0", port=5000)