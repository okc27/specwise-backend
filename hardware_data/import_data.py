from hardware_data.models import Product
import sqlite3

def import_products():
    # Connect to the external database
    conn = sqlite3.connect('C:\\Users\\TS\\Downloads\\web_scraped_data_combined.db')
    cursor = conn.cursor()

    # Query all products from the external database
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()

    for product in products:
        store_id, name, category, price, rating, link = product[1], product[2], product[3], product[4], product[5], product[6]

        # Handle invalid rating (N/A or None)
        if rating == 'N/A' or rating is None:
            rating = None  # Set rating to None if invalid
        else:
            try:
                rating = float(rating)  # Try converting to float
            except ValueError:
                rating = None  # If conversion fails, set to None

        # Check if the product link already exists in the Django database
        if not Product.objects.filter(link=link).exists():
            # Create a new product if it does not exist
            Product.objects.create(
                store_id=store_id,
                name=name,
                category=category,
                price=price,
                rating=rating,  # This could be None if invalid
                link=link
            )

    # Close the connection
    conn.close()

