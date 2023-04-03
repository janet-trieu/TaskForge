from src.server import app
from waitress import serve

mode = "prod"

if mode == "dev":
    app.run(port=8000, debug=True)
else:
    serve(app, host="0.0.0.0", port=8000)
