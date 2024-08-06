tg = Telegram.WebApp;

let art = document.getElementById('art').value;

Telegram.WebApp.onEvent('backButtonClicked', function() {
    Telegram.WebApp.BackButton.hide();
    window.location.href = '/';    
})

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
        credentials: 'include'
    })
}


window.addEventListener('load', async function() {
    const info = await get_info(art);

    document.getElementById('title').innerHTML = info['name'];
    document.getElementById('rating').innerHTML = '⭐ ' + info['rating'];
    document.getElementById('price').innerHTML = info['price'] + '₽';
    document.getElementById('wallet-price').innerHTML = info['wallet_price'] + '₽';

    let preloaders = document.getElementsByClassName('preloader');
    for (let i = 0; i < preloaders.length; i++) {
        preloaders[i].classList.remove('rect');
    }
})


document.getElementById('stop').addEventListener('click', function() {
    delete_product(tg.initDataUnsafe.user.id, art);

    window.location.href = '/';
})



let openPopupBtn = document.getElementById('neuro')
const popup = document.getElementById('popup');
const closeBtn = document.querySelector('.close-btn');

openPopupBtn.addEventListener('click', () => {
    popup.style.display = 'flex';

    fetch('/api/predict_price', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({product_id: art}),
    })
    .then(response => response.json())
    .then(data => {
        const ctx = document.getElementById('price-history').getContext('2d');
        const myChart = new Chart(ctx, {
            type: 'line', // Тип графика: линейный
            data: {
                labels: data['x'], // Подписи оси X
                datasets: [{
                    label: 'My First dataset',
                    data: data['y'], // Данные
                    fill: false, // Заполнение под графиком
                    borderColor: 'blueviolet', // Основной цвет линии
                    segment: {
                        borderColor: function(context) {
                            const { p0DataIndex, p1DataIndex } = context;
                            const length = context.chart.data.labels.length;
                            
                            // Проверяем, если текущий сегмент последний
                            if (p1DataIndex === length - 1) {
                                // Последний сегмент (между последними двумя точками)
                                if (data['y'][length - 1] < data['y'][length - 2]) {
                                    return 'lightgreen'; // Если последнее значение меньше предпоследнего
                                } else {
                                    return 'red'; // Если последнее значение не меньше предпоследнего
                                }
                            } else {
                                return 'blueviolet'; // Все остальные сегменты
                            }
                        }
                    },
                    tension: 0.1, // Напряжение линии (0 для прямых линий)
                    pointBackgroundColor: function(context) {
                        const index = context.dataIndex;
                        const length = context.chart.data.labels.length;
                        
                        // Если это последняя точка
                        if (index === length - 1) {
                            // Определяем цвет последнего сегмента
                            if (data['y'][length - 1] < data['y'][length - 2]) {
                                return 'lightgreen'; // Если последнее значение меньше предпоследнего
                            } else {
                                return 'red'; // Если последнее значение не меньше предпоследнего
                            }
                        } else {
                            return 'blueviolet'; // Цвет всех остальных точек
                        }
                    },
                    pointBorderColor: function(context) {
                        const index = context.dataIndex;
                        const length = context.chart.data.labels.length;
                        
                        // Если это последняя точка
                        if (index === length - 1) {
                            // Определяем цвет последнего сегмента
                            if (data['y'][length - 1] < data['y'][length - 2]) {
                                return 'lightgreen'; // Если последнее значение меньше предпоследнего
                            } else {
                                return 'red'; // Если последнее значение не меньше предпоследнего
                            }
                        } else {
                            return 'blueviolet'; // Цвет всех остальных точек
                        }
                    }                    
                }]
            },
            options: {
                scales: {
                    x: {
                        display: false // Убрать ось X
                    },
                    y: {
                        display: false, // Убрать ось Y
                        beginAtZero: true // Начало оси Y с нуля
                    }
                },
                plugins: {
                    legend: {
                        display: false // Убрать легенду
                    },
                    tooltip: {
                        enabled: false // Убрать подписи при наведении
                    }
                }
            }        
        });          
        if (data['y'][data['y'].length - 1] - 1 < data['y'][data['y'].length - 2]) {
            caption = 'Скорее всего цена понизится'
        } else {
            caption = 'Скорее всего цена повысится'
        }

        document.getElementById('caption').innerHTML = caption;
        document.getElementsByClassName('preloader-price')[0].classList.remove('rect');
    })

    console.log(priceHistory)
});

closeBtn.addEventListener('click', () => {
    popup.style.display = 'none';
});

window.addEventListener('click', (event) => {
    if (event.target === popup) {
        popup.style.display = 'none';
    }
});