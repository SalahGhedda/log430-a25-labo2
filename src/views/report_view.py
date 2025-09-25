"""
Report view
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""
from views.template_view import get_template, get_param
from queries.read_order import get_highest_spending_users, get_top_selling_products
from controllers.user_controller import list_users
from controllers.product_controller import list_products
from views.template_view import get_template

def show_highest_spending_users():
    """ Show report of highest spending users """
    highest_spending_users = get_highest_spending_users(5)

    users = {user.id: user for user in list_users(999)}

    rows = []
    for user_id, total in highest_spending_users:
        user = users.get(user_id)
        if user:
            rows.append(f"""
                <tr>
                    <td>{user.name}</td>
                    <td>${total:.2f}</td>
                </tr>
            """)

    return get_template(f"""
        <h2>Les plus gros acheteurs</h2>
        <table class="table">
            <tr>
                <th>Utilisateur</th>
                <th>Total dépensé</th>
            </tr>
            {" ".join(rows)}
        </table>
    """)

def show_best_sellers():
    """ Show report of best selling products """
    top_selling_products = get_top_selling_products(5)

    products = {p.id: p for p in list_products(999)}

    rows = []
    for product_id, quantity in top_selling_products:
        product = products.get(product_id)
        if product:
            rows.append(f"""
                <tr>
                    <td>{product.name}</td>
                    <td>{quantity}</td>
                </tr>
            """)

    return get_template(f"""
        <h2>Les articles les plus vendus</h2>
        <table class="table">
            <tr>
                <th>Produit</th>
                <th>Quantité vendue</th>
            </tr>
            {" ".join(rows)}
        </table>
    """)