from flask import Flask, request, redirect, render_template

from loader import app, db

import api
import time

@app.route('/')
def index():
    print(request.cookies)

    return render_template('index.html', anticache=time.time())


@app.route('/product/<art>')
def product(art):
    return render_template('product.html', art=art, anticache=time.time())


if __name__ == "__main__":
    app.run(debug=True)