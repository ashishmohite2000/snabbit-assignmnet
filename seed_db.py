# seed_db.py
from app.database import SessionLocal
from app.models import Product

db = SessionLocal()

# Create products
product1 = Product(name="product1", price=100.0)
product2 = Product(name="product2", price=200.0)

# Add to the session and commit
db.add(product1)
db.add(product2)
db.commit()  # This commits to the database
db.close()
