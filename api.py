from flask import Flask, request, redirect, render_template

from loader import app, db
import utils


@app.route('/api/info', methods=['POST'])
def info():
    json = request.get_json()
    art = json['art']

    if art.isdigit():
        art = art
    elif 'https://' in art:
        art = art.split('/')[-2]
    else:
        print(art)
        return {'error': True}

    info = utils.get_product_info(art)
    info['art'] = art

    print(info)

    if info:
        return info
    else:
        return {'error': True}
    

@app.route('/api/new', methods=['POST'])
def new():
    json = request.get_json()
    user_id = json['user_id']
    product_id = json['product_id']

    price = utils.get_product_info(product_id)['price']

    write_data = {
        'id': product_id,
        'price': price,
        'owner': user_id,
    }
    db.new_write(write_data, 'products')

    return {'status': 'ok'}


@app.route('/api/delete_product', methods=['POST'])
def delete():
    json = request.get_json()
    product_id = json['product_id']

    db.delete('products', {'id': product_id})

    return {'status': 'ok'}


@app.route('/api/get_products', methods=['POST'])
def get_products():
    json = request.get_json()
    user_id = json['user_id']

    return db.get_data({'owner': user_id}, 'products')