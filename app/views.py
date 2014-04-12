from app import app

@app.route('/')
def home():
    return 'What restuarant do you want?'

@app.route('/profile')
def profile():
    return 'This restuarant is pretty great. Holla'