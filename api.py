from flask import Flask, request, redirect, render_template, jsonify, make_response

from loader import app, db, db_url, BUFFER
import utils

import requests
import jwt
import time

KEY = 'key'


@app.route('/api/info', methods=['POST'])
def info():
    json = request.get_json()
    art = json['art']

    if art.isdigit():
        art = art
    elif 'https://' in art:
        # art = art.split('/')[-2]
        return {'error': True}
    else:
        print(art)
        return {'error': True}

    info = utils.get_product_info(art)
    info['art'] = art
    info['wallet_price'] = int(info['price'] - info['price'] * 0.04)

    print(info)

    if info:
        return info
    else:
        return {'error': True}
    

@app.route('/api/new', methods=['POST'])
def new():
    token = request.cookies.get('auth_token')

    token = jwt.decode(token, KEY, algorithms='HS256')

    if token['exp'] < time.time():
        return {'status': 'error'}

    json = request.get_json()
    user_id = json['user_id']

    if str(user_id) != str(token['user']):
        return {'status': 'error'}
        
    json = request.get_json()
    user_id = json['user_id']
    product_id = json['product_id']

    info = utils.get_product_info(product_id)
    price = info['price']
    name = info['name']

    write_data = {
        'id': product_id,
        'price': price,
        'owner': user_id,
        'name': name
    }
    db.new_write(write_data, 'products')

    return {'status': 'ok'}


@app.route('/api/delete_product', methods=['POST'])
def delete():
    token = request.cookies.get('auth_token')

    token = jwt.decode(token, KEY, algorithms='HS256')

    if token['exp'] < time.time():
        return {'status': 'error'}

    json = request.get_json()
    user_id = json['user_id']

    if str(user_id) != str(token['user']):
        return {'status': 'error'}

    json = request.get_json()
    product_id = json['product_id']

    db.delete('products', {'id': product_id})

    return {'status': 'ok'}


@app.route('/api/get_products', methods=['POST'])
def get_products():
    token = request.cookies.get('auth_token')

    token = jwt.decode(token, KEY, algorithms='HS256')

    if token['exp'] < time.time():
        return {'status': 'Token expired'}

    json = request.get_json()
    user_id = json['user_id']

    if str(user_id) != str(token['user']):
        return {'status': 'Token invalid'}

    return db.get_data({'owner': user_id}, 'products')


@app.route('/api/auth', methods=['POST'])
def auth():
    expected_keys = ['query', 'exp', 'user']
    # try:
    #     token = request.cookies.get('auth_token')
    #     token_data = jwt.decode(token, KEY, algorithms='HS256')

    #     print(token_data)

    #     if token_data['exp'] > time.time():
    #         return {'status': 'ok'}  
        
    #     for key in expected_keys:
    #         if key not in token_data:
    #             break
    #     else:
    #         return {'status': 'ok'}
    # except:
    #     pass

    print('new token')

    json = request.get_json()

    if 'tgWebAppData' not in json:
        return {'status': 'Have not required parameters'}

    query_string = json['tgWebAppData']

    payload = {
        'query': query_string,
        'exp': time.time() + 3600,
        'user': utils.get_user_id(query_string)
    }

    token = jwt.encode(payload, KEY, algorithm='HS256')

    print(payload)

    response = make_response(jsonify({'message': 'Token set in cookies!'}))
    response.set_cookie('auth_token', token, httponly=True, secure=True)

    return response


@app.route('/api/predict_price', methods=['POST'])
# @cache.cached(timeout=60, query_string=True)
def predict_price():
    json = request.get_json()
    product_id = json['product_id']

    response = requests.post(f"{db_url}/api/predict_price", json={'product_id': product_id}).json()
    
    return response