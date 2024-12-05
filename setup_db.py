from app.database import init_db

def setup_database():
    init_db()
    print("Database setup complete.")

if __name__ == "__main__":
    setup_database()
