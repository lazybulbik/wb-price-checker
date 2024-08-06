// Функция для парсинга строки параметров
function parseHashParams() {
    const hash = window.location.hash.substr(1); // Убираем #
    const params = {};
    hash.split('&').forEach(pair => {
        const [key, value] = pair.split('=');
        params[decodeURIComponent(key)] = decodeURIComponent(value);
    });
    return params;
}

// Получение параметров из URL
const params = parseHashParams();

fetch('/api/auth', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(params),
    credentials: 'include'
}).then(response => response.json())
    .then(data => {
        console.log('Success:', data);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
