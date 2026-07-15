biryani_order = {
    "restaurant_name": "Biryani Paglu",
    "dish_type": "Biryani",
    "price": 199.99,
    "requires_private_cabin": True,
}

 # Applying a 10% discount
after_discount_price = biryani_order["price"] * 0.9 

print(biryani_order)
print(f"Price after discount: {after_discount_price}")