from flask import Flask, request, redirect, render_template

from loader import app, db

import api

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/product/<art>')
def product(art):
    return render_template('product.html', art=art)


if __name__ == "__main__":
    app.run(debug=False)