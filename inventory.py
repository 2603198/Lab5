"""Inventory Management System with JSON persistence and transaction history."""

import json
import os
import sys
from datetime import datetime

FILENAME = "inventory.json"

# Phase 1: sample products (list of dictionaries). Used with: python inventory.py --seed
SAMPLE_PRODUCTS = [
    {"id": "P001", "name": "Laptop", "price": 1200.00, "stock": 15},
    {"id": "P002", "name": "Mouse", "price": 25.50, "stock": 40},
    {"id": "P003", "name": "Keyboard", "price": 45.00, "stock": 25},
]


def _record(product, kind, change):
    """Append one transaction to a product's history (keeps every amount)."""
    product["history"].append({
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "type": kind,
        "change": change,
        "stock_after": product["stock"],
    })


def find_product(inventory, product_id):
    """Return the product dict with this ID, or None."""
    for product in inventory:
        if product["id"].lower() == product_id.lower():
            return product
    return None


def add_product(inventory, product_id, name, price, stock):
    """Add a new product. Returns False if the ID already exists."""
    if find_product(inventory, product_id):
        return False
    product = {"id": product_id, "name": name, "price": price,
               "stock": stock, "history": []}
    _record(product, "initial", stock)
    inventory.append(product)
    return True


def update_stock(inventory, product_id, new_stock):
    """Set a new stock quantity and log the change. Returns the product or None."""
    product = find_product(inventory, product_id)
    if product is None:
        return None
    change = new_stock - product["stock"]
    product["stock"] = new_stock
    _record(product, "update", change)
    return product


def search_product(inventory, product_id):
    """Return the product dict or None."""
    return find_product(inventory, product_id)


def display_all(inventory):
    """Print every product."""
    print("\nCurrent Inventory")
    print("-" * 48)
    if not inventory:
        print("No products in inventory.")
    for p in inventory:
        print(f"ID: {p['id']} | Name: {p['name']} | "
              f"Price: ${p['price']:.2f} | Stock: {p['stock']}")
    print("-" * 48)


def load_inventory():
    """Load inventory.json if it exists; otherwise return an empty list."""
    if os.path.exists(FILENAME):
        print(f"{FILENAME} found.")
        try:
            with open(FILENAME, "r") as f:
                inventory = json.load(f)
            for p in inventory:                      # tolerate files without history
                p.setdefault("history", [])
            print("Inventory loaded successfully.")
            return inventory
        except (json.JSONDecodeError, OSError):
            print("Could not read file. Starting with empty inventory.")
            return []
    print(f"{FILENAME} not found. Starting with empty inventory.")
    return []


def save_inventory(inventory):
    """Write the inventory (including histories) to inventory.json."""
    try:
        with open(FILENAME, "w") as f:
            json.dump(inventory, f, indent=4)
        print(f"Inventory saved successfully to {FILENAME}.")
    except OSError as e:
        print(f"Error saving inventory: {e}")


def read_number(prompt, cast):
    """Prompt until the user enters a valid non-negative number."""
    while True:
        try:
            value = cast(input(prompt))
            if value < 0:
                print("Value cannot be negative.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a number.")


def menu():
    print("\n----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("----------------------------")


def main():
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)

    if "--seed" in sys.argv:                          # optional first-run seeding
        inventory = []
        for p in SAMPLE_PRODUCTS:
            add_product(inventory, p["id"], p["name"], p["price"], p["stock"])
        print("Sample products loaded.")
    else:
        inventory = load_inventory()

    while True:
        menu()
        choice = input("Enter option: ").strip()

        if choice == "1":
            display_all(inventory)

        elif choice == "2":
            print("\nAdd New Product")
            pid = input("Product ID: ").strip()
            name = input("Product Name: ").strip()
            price = read_number("Price: ", float)
            stock = read_number("Stock Quantity: ", int)
            if add_product(inventory, pid, name, price, stock):
                print("Product added successfully!")
            else:
                print("A product with that ID already exists.")

        elif choice == "3":
            print("\nUpdate Stock")
            product = search_product(inventory, input("Enter Product ID: ").strip())
            if product is None:
                print("Product not found.")
            else:
                print("Product Found:")
                print(f"Name: {product['name']}")
                print(f"Current Stock: {product['stock']}")
                new_stock = read_number("New Stock Quantity: ", int)
                update_stock(inventory, product["id"], new_stock)
                print("Stock updated successfully!")

        elif choice == "4":
            print("\nSearch Product")
            product = search_product(inventory, input("Enter Product ID: ").strip())
            if product is None:
                print("Product not found.")
            else:
                print("Product Found")
                print("-" * 48)
                print(f"ID: {product['id']}")
                print(f"Name: {product['name']}")
                print(f"Price: ${product['price']:.2f}")
                print(f"Stock: {product['stock']}")
                print("-" * 48)

        elif choice == "5":
            print("Saving inventory...")
            save_inventory(inventory)

        elif choice == "6":
            print("Saving inventory before exit...")
            save_inventory(inventory)
            print("Thank you for using Inventory Management System.")
            print("Program terminated.")
            break

        else:
            print("Invalid option. Please choose 1-6.")


if __name__ == "__main__":
    main()
