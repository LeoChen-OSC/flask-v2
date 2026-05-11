from ast import Try

from flask import Flask, render_template,request,redirect,url_for,session,flash
import json
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management
def load_data():
    with open('data/flowers.json','r') as f:
        data=json.load(f)
    return data

@app.route('/')
def index():
    flowers=load_data()
    return render_template('index.html', flowers=flowers)
@app.route('/index1', methods=[ 'POST'])
def index1():
    flowers=load_data()
    return render_template('index1.html', flowers=flowers)
@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    flower=request.form.get('flower')
    quantity=int(request.form['quantity'])
    flowers,addons,addons1,addons2=load_data()
    cart=session.get('cart',{})
    if flower not in flowers:
        flash('Flower not found!')
        return redirect(url_for('index1'))
    if flower in cart:
        
        cart[flower]['quantity']+=quantity
        print("hello world")
    else:
        try:
            cart[flower] = {
                'price': flowers[flower]['price'],
                'quantity': quantity
            }
        except TypeError:
            flash("something went wrong")
        
    session['cart'] = cart
    session.modified = True 
    print(f'{flower} added to cart with quantity {quantity}. Current: {session["cart"]}')
    flash(f'{flower} added to cart!')
    return redirect(url_for('index1'))
if __name__ == '__main__':
    
    app.run(debug=True)
#     #runs the program with debugging mode on.