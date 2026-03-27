import mysql.connector
from mysql.connector import Error

# --- Restaurant Management System---
def create_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",      # replace with your MySQL username
            password="password",  # replace with your MySQL password
            database="restaurant"
        )
        return conn
    except Error as e:
        print("Error connecting to MySQL:", e)
        return None

# --- Create database and tables if they don't exist ---
def setup_database():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password"
    )
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS restaurant")
    conn.commit()
    conn.close()

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Menu (
            MenuID INT AUTO_INCREMENT PRIMARY KEY,
            Name VARCHAR(50),
            Description VARCHAR(255),
            Price DECIMAL(10,2)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Orders (
            OrderID INT AUTO_INCREMENT PRIMARY KEY,
            CustomerName VARCHAR(50),
            TableNumber INT,
            MenuID INT,
            Quantity INT,
            FOREIGN KEY (MenuID) REFERENCES Menu(MenuID)
        )
    """)
    conn.commit()
    return conn, cursor

# --- Display Menu ---
def view_menu(cursor):
    cursor.execute("SELECT * FROM Menu")
    menu = cursor.fetchall()
    print("\n--- MENU ---")
    print(f"{'ID':<4} {'Name':<20} {'Description':<40} {'Price (€)':>10}")
    print("-" * 80)
    for m in menu:
        print(f"{m[0]:<4} {m[1]:<20} {m[2]:<40} €{m[3]:>7.2f}")
    print("-" * 80)

# --- Add Menu Item ---
def add_menu_item(cursor, conn):
    while True:
        name = input("Enter item name: ")
        desc = input("Enter item description: ")
        price = float(input("Enter price (€): "))
        cursor.execute("INSERT INTO Menu (Name, Description, Price) VALUES (%s, %s, %s)", (name, desc, price))
        conn.commit()
        print(f"Item '{name}' added successfully.")
        more = input("Add more items? (Y/N): ").strip().upper()
        if more == "N":
            break

# --- Place Order ---
def place_order(cursor, conn):
    customer = input("Customer name: ")
    table = int(input("Table number: "))
    while True:
        view_menu(cursor)
        menu_id = int(input("Enter MenuID of ordered item: "))
        quantity = int(input("Quantity: "))
        cursor.execute("INSERT INTO Orders (CustomerName, TableNumber, MenuID, Quantity) VALUES (%s,%s,%s,%s)",
                       (customer, table, menu_id, quantity))
        conn.commit()
        more = input("Add more items to this order? (Y/N): ").strip().upper()
        if more == "N":
            break
    print(f"Order placed for {customer} at table {table}.")

# --- View Orders ---
def view_orders(cursor):
    try:
        cursor.execute("""
            SELECT o.OrderID, o.CustomerName, o.TableNumber, m.Name, o.Quantity, m.Price, (o.Quantity*m.Price) AS Total
            FROM Orders o
            JOIN Menu m ON o.MenuID = m.MenuID
        """)
        orders = cursor.fetchall()
        print("\n--- ORDERS ---")
        print(f"{'ID':<4} {'Customer':<15} {'Table':<6} {'Item':<20} {'Qty':<5} {'Price (€)':>10} {'Total (€)':>10}")
        print("-" * 90)
        for o in orders:
            print(f"{o[0]:<4} {o[1]:<15} {o[2]:<6} {o[3]:<20} {o[4]:<5} €{o[5]:>7.2f} €{o[6]:>8.2f}")
        print("-" * 90)
    except Error as e:
        print("Error fetching orders:", e)

# --- Update Menu Item ---
def update_menu(cursor, conn):
    view_menu(cursor)
    menu_id = int(input("Enter MenuID to update: "))
    name = input("New name (blank to skip): ")
    desc = input("New description (blank to skip): ")
    price = input("New price (€) (blank to skip): ")
    query = "UPDATE Menu SET "
    updates = []
    params = []
    if name: 
        updates.append("Name=%s")
        params.append(name)
    if desc: 
        updates.append("Description=%s")
        params.append(desc)
    if price:
        updates.append("Price=%s")
        params.append(float(price))
    if updates:
        query += ", ".join(updates) + " WHERE MenuID=%s"
        params.append(menu_id)
        cursor.execute(query, tuple(params))
        conn.commit()
        print("Menu updated.")
    else:
        print("Nothing to update.")

# --- Update Order ---
def update_order(cursor, conn):
    view_orders(cursor)
    order_id = int(input("Enter OrderID to update: "))
    menu_id = input("New MenuID (blank to skip): ")
    quantity = input("New quantity (blank to skip): ")
    query = "UPDATE Orders SET "
    updates = []
    params = []
    if menu_id:
        updates.append("MenuID=%s")
        params.append(int(menu_id))
    if quantity:
        updates.append("Quantity=%s")
        params.append(int(quantity))
    if updates:
        query += ", ".join(updates) + " WHERE OrderID=%s"
        params.append(order_id)
        cursor.execute(query, tuple(params))
        conn.commit()
        print("Order updated.")
    else:
        print("Nothing to update.")

# --- Delete Order ---
def delete_order(cursor, conn):
    view_orders(cursor)
    order_id = int(input("Enter OrderID to delete: "))
    cursor.execute("DELETE FROM Orders WHERE OrderID=%s", (order_id,))
    conn.commit()
    print("Order deleted successfully.")

# --- Total Bill ---
def total_bill(cursor):
    try:
        cursor.execute("""
            SELECT CustomerName, TableNumber, SUM(o.Quantity*m.Price) AS Total
            FROM Orders o
            JOIN Menu m ON o.MenuID = m.MenuID
            GROUP BY CustomerName, TableNumber
        """)
        bills = cursor.fetchall()
        print("\n--- TOTAL BILLS ---")
        print(f"{'Customer':<15} {'Table':<6} {'Total (€)':>10}")
        print("-" * 40)
        for b in bills:
            print(f"{b[0]:<15} {b[1]:<6} €{b[2]:>8.2f}")
        print("-" * 40)
    except Error as e:
        print("Error calculating total:", e)

# --- Main App ---
def restaurant_app():
    setup_database()
    conn, cursor = setup_database()
    while True:
        print("\n1. Add Menu Item")
        print("2. View Menu")
        print("3. Place Order")
        print("4. View Orders")
        print("5. Update Menu Item")
        print("6. Update Order")
        print("7. Delete Order")
        print("8. Total Bill")
        print("9. Exit")
        choice = input("Enter choice: ").strip()
        if choice == "1":
            add_menu_item(cursor, conn)
        elif choice == "2":
            view_menu(cursor)
        elif choice == "3":
            place_order(cursor, conn)
        elif choice == "4":
            view_orders(cursor)
        elif choice == "5":
            update_menu(cursor, conn)
        elif choice == "6":
            update_order(cursor, conn)
        elif choice == "7":
            delete_order(cursor, conn)
        elif choice == "8":
            total_bill(cursor)
        elif choice == "9":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Try again.")
    cursor.close()
    conn.close()

# --- Run ---
if __name__ == "__main__":
    restaurant_app()
