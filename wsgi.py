import os

from main import app

if __name__ == '__main__':
    PORT = os.environ.get('PORT') if os.environ.get('PORT') else 3000
    print("PORT: " + str(PORT))
    if os.environ.get('ENV') == "development":
        app.run(host='0.0.0.0', port=PORT, debug=True)
    else:
        app.run()