from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Mock database to store orders
orders_db = []

# Mock database to store ratings and reviews with some sample reviews
ratings_db = [
    {"name": "Ramesh Kumar", "product": "Raw Cow Milk", "rating": 5, "comment": "Very fresh and pure milk delivered daily!"},
    {"name": "Sunita Patil", "product": "Pure Butter", "rating": 4, "comment": "Authentic taste, reminds me of traditional village butter."}
]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        name = request.form.get('name')
        product = request.form.get('product')
        quantity = request.form.get('quantity')
        payment_mode = request.form.get('payment_mode')
        
        order_id = len(orders_db) + 1
        
        orders_db.append({
            "id": order_id,
            "name": name,
            "product": product,
            "quantity": quantity,
            "payment_mode": payment_mode,
            "status": "Confirmed"
        })
        
        return render_template('order_success.html', 
                               order_id=order_id, 
                               name=name, 
                               product=product, 
                               quantity=quantity, 
                               payment_mode=payment_mode)
    
    return render_template('checkout.html')

@app.route('/cancel', methods=['GET', 'POST'])
def cancel_order():
    message = None
    if request.method == 'POST':
        try:
            order_id = int(request.form.get('order_id'))
            order = next((o for o in orders_db if o["id"] == order_id), None)
            if order:
                order["status"] = "Cancelled"
                message = f"Order #{order_id} has been successfully cancelled."
            else:
                message = f"Order #{order_id} not found."
        except ValueError:
            message = "Please enter a valid numeric Order ID."
            
    return render_template('cancel.html', message=message, orders=orders_db)

@app.route('/ratings', methods=['GET', 'POST'])
def ratings_page():
    if request.method == 'POST':
        name = request.form.get('name')
        product = request.form.get('product')
        rating = request.form.get('rating')
        comment = request.form.get('comment')
        
        # Add new review to the top of the list
        ratings_db.insert(0, {
            "name": name,
            "product": product,
            "rating": int(rating),
            "comment": comment
        })
        return redirect(url_for('ratings_page'))
        
    return render_template('ratings.html', ratings=ratings_db)

if __name__ == '__main__':
    app.run(debug=True)