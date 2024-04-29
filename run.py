from app import create_app, db  # Import db from your application package

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensure that db is imported
    app.run(debug=True)
