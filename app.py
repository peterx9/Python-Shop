from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Sample items for sale with images
items = [
    {'id': 1, 'name': 'White T-shirt', 'price': 10.0, 'image': 'item1.jpg', 'category': 'Category 1'},
    {'id': 2, 'name': 'Baggy Jeans', 'price': 20.0, 'image': 'item2.jpg', 'category': 'Category 1'},
    {'id': 3, 'name': 'Air Force nike', 'price': 30.0, 'image': 'item3.jpg', 'category': 'Category 1'},
    {'id': 4, 'name': 'Hat', 'price': 40.0, 'image': 'item4.jpg', 'category': 'Category 1'},
    {'id': 5, 'name': 'Jacket For Men', 'price': 50.0, 'image': 'item5.jpg', 'category': 'Category 1'},
    {'id': 6, 'name': 'Wide T-shirt', 'price': 60.0, 'image': 'item6.jpg', 'category': 'Category 2'},
    {'id': 7, 'name': 'Jeans', 'price': 70.0, 'image': 'item7.jpg', 'category': 'Category 2'},
    {'id': 8, 'name': 'String Bead Shoes', 'price': 80.0, 'image': 'item8.jpg', 'category': 'Category 2'},
    {'id': 9, 'name': 'Glasses', 'price': 90.0, 'image': 'item9.jpg', 'category': 'Category 2'},
    {'id': 10, 'name': 'Jacket For Women', 'price': 100.0, 'image': 'item10.jpg', 'category': 'Category 2'},
]

# Sample user data (for demonstration purposes)
users = {'admin': 'password'}

@app.route('/')
def index():
    search_query = request.args.get('search', '')
    category_filter = request.args.get('category', '')
    filtered_items = [item for item in items if search_query.lower() in item['name'].lower()]
    if category_filter:
        filtered_items = [item for item in filtered_items if item['category'] == category_filter]
    return render_template('index.html', items=filtered_items, search_query=search_query, category_filter=category_filter)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return 'Invalid credentials'
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username not in users:
            users[username] = password
            flash('Thanks for registering. Team CODEHUB', 'success')
            return redirect(url_for('register'))
        else:
            return 'Username already exists'
    return render_template('register.html')

@app.route('/cart')
def cart():
    if 'cart' not in session:
        session['cart'] = []
    total = sum(item['price'] * item['quantity'] for item in session['cart'])
    return render_template('cart.html', cart=session['cart'], total=total)

@app.route('/add_to_cart/<int:item_id>', methods=['POST'])
def add_to_cart(item_id):
    if 'username' not in session:
        return jsonify({'message': 'You need to register to add items to the cart', 'category': 'error', 'redirect': url_for('register')})
    if 'cart' not in session:
        session['cart'] = []
    item = next((item for item in items if item['id'] == item_id), None)
    if item:
        cart_item = next((i for i in session['cart'] if i['id'] == item_id), None)
        if cart_item:
            cart_item['quantity'] += 1
        else:
            item['quantity'] = 1
            session['cart'].append(item)
        session.modified = True  # Ensure the session is marked as modified
        return jsonify({'message': 'Item has been added to the cart', 'category': 'success', 'quantity': cart_item['quantity'] if cart_item else item['quantity']})
    return jsonify({'message': 'Item not found', 'category': 'error'})

@app.route('/remove_from_cart/<int:item_id>', methods=['POST'])
def remove_from_cart(item_id):
    if 'cart' in session:
        cart_item = next((i for i in session['cart'] if i['id'] == item_id), None)
        if cart_item:
            if cart_item['quantity'] > 1:
                cart_item['quantity'] -= 1
            else:
                session['cart'] = [item for item in session['cart'] if item['id'] != item_id]
            session.modified = True  # Ensure the session is marked as modified
            return jsonify({'message': 'Item has been removed from the cart', 'category': 'success', 'quantity': cart_item['quantity'] if cart_item['quantity'] > 0 else 0})
    return jsonify({'message': 'Item not found in cart', 'category': 'error'})

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        # Process the payment here
        session.pop('cart', None)
        flash('Payment was successful!', 'success')
        return redirect(url_for('checkout'))
    if 'cart' not in session:
        session['cart'] = []
    total = sum(item['price'] * item['quantity'] for item in session['cart'])
    return render_template('checkout.html', cart=session['cart'], total=total)

@app.route('/payment_success')
def payment_success():
    return "Payment was successful!"

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)