tg = Telegram.WebApp;

let art = document.getElementById('art').value;

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

function delete_product(user_id, product_id) {
    fetch('/api/delete_product', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({user_id: user_id, product_id: product_id}),
    })
}


window.addEventListener('load', async function() {
    const info = await get_info(art);

    document.getElementById('title').innerHTML = info['name'];
    document.getElementById('rating').innerHTML = '⭐ ' + info['rating'];
    document.getElementById('price').innerHTML = info['price'] + '₽';

    let preloaders = document.getElementsByClassName('preloader');
    for (let i = 0; i < preloaders.length; i++) {
        preloaders[i].classList.remove('rect');
    }
})


document.getElementById('stop').addEventListener('click', function() {
    delete_product(tg.initDataUnsafe.user.id, art);

    window.location.href = '/';
})