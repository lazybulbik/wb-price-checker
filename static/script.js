tg = Telegram.WebApp;
tg.expand();

async function get_info(art) {
    const response = await fetch ('/api/info', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({art: art}),
    })

    if (response.ok) {
        const info = await response.json();
        return info;
    }

}

function add_product(user_id, product_id) {
    fetch('/api/new', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({user_id: user_id, product_id: product_id}),
    })
}

function add_product_to_list(data) {
    let productDiv = document.createElement('div');
    productDiv.className = 'product';

    if ('art' in data) {
        productDiv.id = data['art'];
    }
    else {
        productDiv.id = data['id'];
    }
    productDiv.addEventListener('click', function() {
        Telegram.WebApp.BackButton.show();
        window.location.href = `/product/${productDiv.id}`;
    });

    let productTitle = document.createElement('h5');
    productTitle.className = 'product-title';
    productTitle.textContent = data['name'];

    let productPrice = document.createElement('h6');
    productPrice.className = 'product-price';
    productPrice.textContent = `${data['price']}₽`;        

    productDiv.appendChild(productTitle);
    productDiv.appendChild(productPrice);

    document.getElementById('list').appendChild(productDiv);
    
    let list = document.getElementsByClassName('product');
    document.getElementById('counter').innerHTML = `${list.length}/5`;
}

function shake(object) {
    object.classList.add('shake-animation');

    setTimeout(function() {
        object.classList.remove('shake-animation');
    }, 800);
    window.navigator.vibrate(500);
}

document.getElementById('check').addEventListener('click', async function() {
    let art = document.getElementById('art').value;

    products = document.getElementsByClassName('product');

    if (products.length >= 5) {
        shake(document.getElementById('counter'));
        return;
    }

    if (art) {
        const info = await get_info(art);        
        if (info['error']) {
            shake(document.getElementById('art'));
            document.getElementById('art').value = '';
        }
        else {
            const art = info['art'];

            add_product(tg.initDataUnsafe.user.id, art);
            
            add_product_to_list(info);
            
            document.getElementById('art').value = '';
        }
    
    }
    else {
        shake(document.getElementById('art'));
    }
})

window.addEventListener('DOMContentLoaded', function() {
    fetch('/api/get_products', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({user_id: tg.initDataUnsafe.user.id}),
    })
    .then(response => response.json())
    .then(data => {
        // this.document.getElementById('counter').innerHTML = `${data.length}/5`;        

        for (let i = 0; i < data.length; i++) {
            add_product_to_list(data[i]);

            // this.document.getElementById('list').innerHTML += `
            //     <div class="product" id="${data[i]['art']}">
            //         <h5 class="product-title">${data[i]['name']}</h5>
            //         <h6 class="product-price">${data[i]['price']}₽</h6>
            //     </div>
            // `;
        }
    })

    preloaders = document.getElementsByClassName('preloader');
    for (let i = 0; i < preloaders.length; i++) {
        preloaders[i].classList.remove('rect');
    }
})