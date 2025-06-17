from app import app
from datetime import datetime

# Add current year to all templates
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

if __name__ == '__main__':
    app.run(debug=True, port=5001) 