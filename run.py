# Import the function to initialize the Flask app and the SQLAlchemy database object
from app import create_app, db

# Create the Flask application
app = create_app()

# Entry point of the application
if __name__ == '__main__':
    with app.app_context():
        # Create all database tables
        db.create_all()
        
    # Run the Flask server
    app.run(debug=True)