from sqlalchemy.orm import Session
from config.database import get_db
from api.category import category_model
from api.product import product_model

db: Session = next(get_db())

# Sample categories
categories = [
    {
        "name": "Iced Coffee", 
        "description": "Refreshing cold coffee beverages, perfect for a hot day.",
        "image_url": "/static/images/categories/iced_coffee.svg"
    },
    {
        "name": "Hot Coffee", 
        "description": "Warm, aromatic coffee to start your day or cozy up.",
        "image_url": "/static/images/categories/hot_coffee.svg"
    },
    {
        "name": "Iced Drink", 
        "description": "Chilled beverages and juices to cool you down.",
        "image_url": "/static/images/categories/iced_drink.svg"
    },
    {
        "name": "Hot Drink", 
        "description": "Comforting warm drinks like tea, cocoa, or lattes.",
        "image_url": "/static/images/categories/hot_drink.svg"
    },
    {
        "name": "Frappuccino", 
        "description": "Blended icy coffee treats with flavors and toppings.",
        "image_url": "/static/images/categories/frappuccino.svg"
    },
    {
        "name": "Food & Snacks", 
        "description": "Tasty bites, pastries, and light snacks for anytime.",
        "image_url": "/static/images/categories/food_snacks.svg"
    },
]

for c in categories:
    exists = db.query(category_model.Category).filter_by(name=c["name"]).first()
    if not exists:
        category = category_model.Category(
            name=c["name"],
            description=c["description"],
            image_url=c["image_url"]
        )
        db.add(category)

products = [
    # Iced Coffee
    {
        "name": "Iced Americano", 
        "description": "Strong espresso over ice", 
        "price": 2.5,
        "image_url": "/static/images/products/Iced_Americano.jpg", 
        "category_id": 1},
    {   
        "name": "Iced Latte", 
        "description": "Espresso with milk served cold", 
        "price": 3.0, 
        "image_url": "/static/images/products/Iced_Latte.jpg", 
        "category_id": 1
    },
    {   "name": "Iced Cappuccino", 
        "description": "Creamy foam over chilled espresso", 
        "price": 3.2, 
        "image_url": "/static/images/products/Iced_Cappuccino.png", 
        "category_id": 1
    },
    {
        "name": "Iced Mocha", 
        "description": "Chocolate and espresso over ice",
        "price": 3.5, 
        "image_url": "/static/images/products/Iced_Mocha.jpg", 
        "category_id": 1
    },
    {
        "name": "Iced Caramel Macchiato", 
        "description": "Sweet caramel with espresso and milk",
        "image_url": "/static/images/products/Iced_Caramel_Macchiato.jpg", 
        "price": 3.7, 
        "category_id": 1
    },

    # Hot Coffee
    {
        "name": "Espresso", 
        "description": "Classic strong coffee shot", 
        "price": 2.0,
        "image_url": "/static/images/products/Espresso.jpg",
        "category_id": 2
    },
    {
        "name": "Hot Latte", 
        "description": "Smooth espresso with steamed milk", 
        "price": 2.8, 
        "image_url": "/static/images/products/Hot_Latte.jpg",
        "category_id": 2},
    {
        "name": "Cappuccino", 
        "description": "Espresso with milk foam", 
        "price": 3.0, 
        "image_url": "/static/images/products/Cappuccino.jpg",
        "category_id": 2},
    {
        "name": "Hot Mocha", 
        "description": "Chocolate-infused hot coffee", 
        "price": 3.3, 
        "image_url": "/static/images/products/Hot_Mocha.jpg",
        "category_id": 2},
    {
        "name": "Flat White", 
        "description": "Espresso with velvety milk", 
        "price": 3.2, 
        "image_url": "/static/images/products/Flat_White.jpg",
        "category_id": 2
    },

    # Iced Drink
    {
        "name": "Iced Lemon Tea", 
        "description": "Refreshing lemon-flavored iced tea", 
        "price": 1.5, 
        "image_url": "/static/images/products/Iced_Lemon_Tea.jpg",
        "category_id": 3
    },
    {
        "name": "Iced Peach Tea", 
        "description": "Sweet peach iced tea", 
        "price": 1.7,
        "image_url": "/static/images/products/Iced_Peach_Tea.jpg", 
        "category_id": 3
        },
    {
        "name": "Iced Green Tea", 
        "description": "Chilled green tea with mint", 
        "price": 1.8,
        "image_url": "/static/images/products/Iced_Green_Tea.jpg", 
        "category_id": 3
    },
    {
        "name": "Iced Mango Tea", 
        "description": "Tropical mango iced tea", 
        "price": 2.0, 
        "image_url": "/static/images/products/Iced_Mango_Tea.jpg",
        "category_id": 3
    },
    {
        "name": "Iced Passionfruit Tea", 
        "description": "Tangy passionfruit over ice", 
        "price": 2.1, 
        "image_url": "/static/images/products/Iced_Passionfruit_Tea.jpg",
        "category_id": 3
    },

    # Hot Drink
    {
        "name": "Hot Chocolate", 
        "description": "Rich chocolate drink", 
        "price": 2.5, 
        "image_url": "/static/images/products/Hot_Chocolate.jpg",
        "category_id": 4
    },
    {
        "name": "Hot Green Tea", 
        "description": "Traditional warm green tea", 
        "price": 2.0, 
        "image_url": "/static/images/products/Hot_Green_Tea.jpg",
        "category_id": 4
    },
    {
        "name": "Chai Latte", 
        "description": "Spiced tea with milk", 
        "price": 2.8, 
        "image_url": "/static/images/products/Chai_Latte.jpg",
        "category_id": 4
    },
    {
        "name": "Herbal Tea", 
        "description": "Calming herbal infusion", 
        "price": 2.2, 
        "image_url": "/static/images/products/Herbal_Tea.jpg",
        "category_id": 4
    },
    {
        "name": "Hot Lemon Honey", 
        "description": "Lemon and honey warm drink", 
        "price": 2.3, 
        "image_url": "/static/images/products/Hot_Lemon_Honey.jpg",
        "category_id": 4
    },

    # Frappuccino
    {
        "name": "Mocha Frappuccino", 
        "description": "Blended chocolate and coffee", 
        "price": 3.5, 
        "image_url": "/static/images/products/Mocha_Frappuccino.jpg",
        "category_id": 5},
    {
        "name": "Caramel Frappuccino", 
        "description": "Sweet caramel blended drink", 
        "price": 3.7, 
        "image_url": "/static/images/products/Caramel_Frappuccino.jpg",
        "category_id": 5},
    {
        "name": "Vanilla Frappuccino", 
        "description": "Smooth vanilla iced blend", 
        "price": 3.3, 
        "image_url": "/static/images/products/Vanilla_Frappuccino.jpg",
        "category_id": 5},
    {
        "name": "Matcha Frappuccino", 
        "description": "Green tea blended with milk", 
        "price": 3.6, 
        "image_url": "/static/images/products/Matcha_Frappuccino.jpg",
        "category_id": 5},
    {
        "name": "Strawberry Frappuccino", 
        "description": "Sweet strawberry blended drink", 
        "price": 3.8, 
        "image_url": "/static/images/products/Strawberry_Frappuccino.jpg",
        "category_id": 5},

    # Food & Snack
    {
        "name": "Chocolate Muffin", 
        "description": "Soft and chocolaty muffin", 
        "price": 2.0, 
        "image_url": "/static/images/products/Chocolate_Muffin.jpg",
        "category_id": 6
    },
    {
        "name": "Croissant", 
        "description": "Buttery flaky pastry", 
        "price": 2.5, 
        "image_url": "/static/images/products/Croissant.jpg",
        "category_id": 6
    },
    {
        "name": "Blueberry Tart", 
        "description": "Sweet tart with fresh blueberries", 
        "price": 3.0,
        "image_url": "/static/images/products/Blueberry_Tart.jpg", 
        "category_id": 6
    },
    {
        "name": "Chicken Sandwich", 
        "description": "Grilled chicken with veggies", 
        "price": 4.5, 
        "image_url": "/static/images/products/Chicken_Sandwich.jpg",
        "category_id": 6
    },
    {
        "name": "Potato Chips", 
        "description": "Crispy salted chips", 
        "price": 1.5, 
        "image_url": "/static/images/products/Potato_Chips.jpg",
        "category_id": 6
    },
]

for p in products:
    exists = db.query(product_model.Product).filter_by(name=c["name"]).first()
    if not exists:
        product = product_model.Product(
            name=c["name"],
            description=c["description"],
            price=c["price"],
            image_url=c["image_url"],
            category_id=c["category_id"]
        )
        db.add(product)


db.commit()
print("Seeded categories and products successfully!")