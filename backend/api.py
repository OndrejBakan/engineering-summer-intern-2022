from datetime import datetime
from math import ceil
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/api/fee', methods=('POST',))
def fee():
    MIN_ORDER = 100 * 10
    DELIVERY_FEE_CAP = 100 * 15
    FREE_DELIVERY_VALUE = 100 * 100
    RUSH_HOUR_MULTIPLIER = 1.1
    
    data = request.json
    delivery_fee = 0

    cart_value, delivery_distance, number_of_items, order_time = [data.get('cart_value'), data.get('delivery_distance'), data.get('number_of_items'), data.get('time')]

    # If cart value is equal to or higher than 100 €, delivery is free
    if cart_value >= FREE_DELIVERY_VALUE:
        return jsonify({'delivery_fee': 0})

    # Surcharge: min. cart value
    if cart_value < MIN_ORDER:
        delivery_fee += MIN_ORDER - cart_value
    
    # Surcharge: distance
    delivery_fee += 2 * 100
    if delivery_distance > 1000:
        delivery_fee += ceil((delivery_distance - 1000) / 500) * 100
    
    # Surcharge: number of items >= 5
    if number_of_items >= 5:
        delivery_fee += (number_of_items - 4) * 50
    
    # Friday rush
    if _is_it_rush_hour(order_time):
        delivery_fee *= RUSH_HOUR_MULTIPLIER

    # Apply delivery fee cap
    if delivery_fee > DELIVERY_FEE_CAP:
        return jsonify({'delivery_fee': DELIVERY_FEE_CAP})

    return jsonify({'delivery_fee': delivery_fee})

def _is_it_rush_hour(order_time):
    order_time = datetime.strptime(order_time, '%Y-%m-%dT%H:%M:%S%z')

    # Friday, between 3 PM and 7 PM
    if order_time.weekday() == 4 and order_time.hour >= 15 and order_time.hour <= 19:
        return True