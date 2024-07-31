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

function shake(object) {
    object.classList.add('shake-animation');

    setTimeout(function() {
        object.classList.remove('shake-animation');
    }, 800);
    window.navigator.vibrate(500);
}

document.getElementById('check').addEventListener('click', async function() {
    let art = document.getElementById('art').value;

    if (art) {
        const info = await get_info(art);        
        if (info['error']) {
            shake(document.getElementById('art'));
            document.getElementById('art').value = '';
        }
        else {
            const art = info['art'];
            
            add_product(tg.initDataUnsafe.user.id, art);
            window.location.href = `/product/${art}`;
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
        if (data.length > 0) {
            window.location.href = `/product/${data[0]['id']}`
        }
    })

    this.setTimeout(function() {
        this.document.getElementsByClassName('screen')[0].classList.remove('hidden');
    }, 3000)
})
