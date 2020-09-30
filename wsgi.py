
from dash_app import server
# gunicorn -c gunicorn.config.py dash_app:server

if __name__ == "__main__":
    server.run(host='0.0.0.0')
