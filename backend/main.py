from src.server import app
# from waitress import serve

app.run(port=8000, debug=True)

# mode = "dev"

# if mode == "dev":
#     app.run(port=8000, debug=True)
# else:
    # serve(app, host="0.0.0.0", port=8000, url_prefix="/my-app")
