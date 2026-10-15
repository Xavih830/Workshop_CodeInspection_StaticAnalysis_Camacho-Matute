"""Order processing logic."""
import sqlite3

import database
import auth

TAX = 0.15
SEPARATOR = "=============================="


<<<<<<< HEAD
def _process_item(item):
    book = database.get_book(item["book_id"])
    if book is None:
        print("Book not found")
        return 0
    quantity = item["qty"]
    if quantity <= 0:
        print("Invalid quantity")
        return 0
    if book[3] < quantity:
=======
def _process_cart_item(item):
    book = database.get_book(item["book_id"])
    if not book:
        print("Book not found")
        return 0
    if book[3] < item["qty"]:
>>>>>>> 88b7d7185d97ab20338c554b377809362f119a79
        if book[3] > 0:
            print("Only " + str(book[3]) + " units available for " + book[1])
        else:
            print("Book out of stock: " + book[1])
        return 0
<<<<<<< HEAD
    database.update_stock(book[0], book[3] - quantity)
    return book[2] * quantity


def _apply_coupon(token, coupon, total):
=======
    if item["qty"] <= 0:
        print("Invalid quantity")
        return 0
    database.update_stock(book[0], book[3] - item["qty"])
    return book[2] * item["qty"]


def _apply_coupon(total, coupon, token):
>>>>>>> 88b7d7185d97ab20338c554b377809362f119a79
    if coupon == "WELCOME10":
        return total * 0.9
    if coupon == "BLACKFRIDAY":
        return total * 0.5
<<<<<<< HEAD
    if coupon == "STAFF" and auth.is_admin(token):
        return total * 0.7
    return total


def _next_order_id():
    conn = database.get_connection()
    try:
        return conn.execute("SELECT COALESCE(MAX(id), 0) + 1 FROM orders").fetchone()[0]
    finally:
        conn.close()


def process_order(token, items, coupon=None, shipping="standard", log=None):
    if log is None:
        log = []
    username = auth.sessions.get(token)
    if username is None:
        print("Invalid session")
        return None
    if not items:
        print("Empty order")
        return None
    total = sum(_process_item(item) for item in items)
    total = _apply_coupon(token, coupon, total)
    total += {"express": 10, "standard": 3}.get(shipping, 0)
    total += total * TAX
    order_id = _next_order_id()
    database.save_order(order_id, username, total, "PENDING")
    log.append(order_id)
    return round(total, 2)


def _print_document(username, items, title, footer=None):
    print(SEPARATOR)
    print(title)
    print("Customer: " + username)
    print(SEPARATOR)
    subtotal = 0
    for item in items:
        book = database.get_book(item["book_id"])
        line_total = book[2] * item["qty"]
        subtotal = subtotal + line_total
        print(book[1] + " x" + str(item["qty"]) + " = " + str(line_total))
    tax = subtotal * TAX
    print("Subtotal: " + str(round(subtotal, 2)))
    print("Tax: " + str(round(tax, 2)))
    print("Total: " + str(round(subtotal + tax, 2)))
    if footer is not None:
        print(footer)
    print(SEPARATOR)
=======
    if coupon == "STAFF":
        if auth.is_admin(token):
            return total * 0.7
    return total


def _apply_shipping(total, shipping):
    if shipping == "express":
        return total + 10
    if shipping == "standard":
        return total + 3
    return total


def process_order(token, items, coupon=None, shipping="standard", log=[]):
    username = auth.sessions.get(token)
    if username == None:
        print("Invalid session")
        return None
    if items == []:
        print("Empty order")
        return None

    total = 0
    for item in items:
        total += _process_cart_item(item)

    if coupon:
        total = _apply_coupon(total, coupon, token)

    total = _apply_shipping(total, shipping)
    total = total + total * TAX

    order_id = len(log) + 1
    database.save_order(order_id, username, total, "PENDING")
    log.append(order_id)
    return round(total, 2)
>>>>>>> 88b7d7185d97ab20338c554b377809362f119a79


def print_invoice(username, items):
    _print_document(username, items, "BOOKSTORE INVOICE")


def print_quote(username, items):
    _print_document(
        username, items, "BOOKSTORE QUOTE", "This quote is valid for 7 days."
    )


def cancel_order(order_id):
    conn = database.get_connection()
    try:
        conn.execute("UPDATE orders SET status = ? WHERE id = ?", ("CANCELLED", order_id))
        conn.commit()
    except sqlite3.Error:
        conn.rollback()
        raise
    finally:
        conn.close()
