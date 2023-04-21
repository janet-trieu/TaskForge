'''
File to run the backend server
'''
from src.server import app

app.run(port=8000, debug=True)