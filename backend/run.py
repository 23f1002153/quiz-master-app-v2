from app import create_app

# This is where the Flask app object is actually created.
app = create_app()

# This block allows you to run the Flask development server
# by executing "python run.py" in your terminal.
if __name__ == '__main__':
    # The host='0.0.0.0' makes the server accessible on your local network,
    # which is often useful for development.
    app.run(host='0.0.0.0', port=5000, debug=True)

