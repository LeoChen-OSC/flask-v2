from flask import Flask, render_template,request,redirect,url_for,session,flash
import json,math,random
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management
def load_data():
    with open('data/flowers.json','r') as f:
        flower=json.load(f)
    with open('data/addons.json','r') as f:
        addons=json.load(f)
    return flower,addons

@app.route('/')
def index():
    a12=(math.sin(random.random())+1)*100
    flowers,addons=load_data()
    flash(a12)
    return render_template('index.html', flowers=flowers, addons=addons)
@app.route('/index1', methods=[ 'POST'])
def index1():
    flowers,addons=load_data()
    return render_template('index1.html', flowers=flowers,addons=addons)
@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    flower=request.form['flower'] # get the flower data in this form
    quantity=int(request.form['quantity']) # Convert quantity to an int
    flowers,addons=load_data()
    cart=session.get('cart',{})
    if flower not in flowers:
        flash("Flower not found!")
        return redirect(url_for('checkout'))
    if flower in cart:    
        cart[flower]['quantity']+=quantity
        print("hello world")
    else:
        cart[flower]={
            'price': flowers[flower]['price'],
            'quantity': quantity
        }


        
    session['cart'] = cart
    session.modified = True 
    print(f'{flower} added to cart with quantity {quantity}. Current: {session["cart"]}')
    flash(f'{quantity} {flower}(s) added to cart!')
    return redirect(url_for('checkout'))
@app.route('/select_addon', methods=['POST'])
def select_addon():
    selected_addons={}
    _, addons = load_data()
    selected_keys = request.form.getlist('addons')
    for addon in selected_keys:
        if addon in addons:
            selected_addons[addon] = float(addons[addon]['price'])
    session['selected_addons'] = selected_addons
    session.modified = True
    flash(f'you have addedaddons: {", ".join(selected_addons.keys())}')
    return redirect(url_for('checkout'))
@app.route('/checkout')
def checkout():
    cart=session.get('cart',{})
    flower,addons=load_data()
    selected_addons=session.get('selected_addons',{})
    return render_template('checkout.html', cart=cart, flowers=flower, addons=addons, selected_addons=selected_addons,)
@app.route('/remove_from_cart/<items>')
def remove_from_cart(items):
    cart=session.get('cart',{})
    selected_addons=session.get('selected_addons',{})
    if items in cart:
        del cart[items]
        session['cart'] = cart
        session.modified = True
        flash(f'{items} removed from cart!')
    else:
        flash(f'{items} not found in cart!')
    return redirect(url_for('checkout'))
if __name__ == '__main__':
    
    app.run(debug=True)
#     #runs the program with debugging mode on.