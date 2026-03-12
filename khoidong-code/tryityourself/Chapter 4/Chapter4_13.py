menu = ("steak", "salad", "pizza", "pasta", "soup")

print("Original Menu:")
for item in menu:
    print(item)

# Intentional Error:
# menu[0] = "burger" # Raises a TypeError!

# Rewriting the entire tuple:
menu = ("steak", "salad", "burger", "fries", "soup")

print("\nRevised Menu:")
for item in menu:
    print(item)