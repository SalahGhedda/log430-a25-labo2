"""
Orders (read-only model)
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""

from db import get_sqlalchemy_session, get_redis_conn
from sqlalchemy import desc
from models.order import Order

def get_order_by_id(order_id):
    """Get order by ID from Redis"""
    r = get_redis_conn()
    return r.hgetall(order_id)

def get_orders_from_mysql(limit=9999):
    """Get last X orders"""
    session = get_sqlalchemy_session()
    return session.query(Order).order_by(desc(Order.id)).limit(limit).all()

def get_orders_from_redis(limit=9999):
    """Get last X orders"""
    r = get_redis_conn()
    keys = r.keys("order:*")

    ids = sorted([int(k.decode().split(":")[1]) for k in keys if b":items" not in k], reverse=True)
    ids = ids[:limit]

    orders = []
    for oid in ids:
        data = r.hgetall(f"order:{oid}")
        orders.append(Order(
            id=int(data[b'id']),
            user_id=int(data[b'user_id']),
            total_amount=float(data[b'total_amount'])
        ))
    return orders

def get_highest_spending_users():
    """Get report of best selling products"""
    limit=10
    r = get_redis_conn()
    keys = r.keys("order:*")
    spending = {}

    for key in keys:
        if b":items" in key:
            continue
        data = r.hgetall(key)
        if not data:
            continue
        user_id = int(data[b"user_id"])
        total = float(data[b"total_amount"])
        spending[user_id] = spending.get(user_id, 0) + total

    # Trier par montant dépensé décroissant
    top_users = sorted(spending.items(), key=lambda x: x[1], reverse=True)
    return top_users[:limit]

def get_top_selling_products():
    """Get report of best selling products"""
    limit = 10
    r = get_redis_conn()
    keys = r.keys("order:*:items")
    sales = {}

    for key in keys:
        items = r.lrange(key, 0, -1)  # ex: ["3|2", "5|1"]
        for raw in items:
            pid, qty = raw.decode().split("|")
            pid = int(pid)
            qty = int(qty)
            sales[pid] = sales.get(pid, 0) + qty

    # Trier par quantités vendues décroissantes
    top_products = sorted(sales.items(), key=lambda x: x[1], reverse=True)
    return top_products[:limit]