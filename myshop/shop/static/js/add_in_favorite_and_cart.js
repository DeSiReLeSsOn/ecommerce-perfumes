document.addEventListener('DOMContentLoaded', function() {
    const heartImgPath = '/static/images/heart.png';
    const likeImgPath = '/static/images/like.png';
    const cartImgPath = '/static/img/cart.png';
    const okImgPath = '/static/img/ok.png';
    const csrfToken = document.querySelector('script[data-csrf-token]').getAttribute('data-csrf-token');

    // Код добавления и удаления избранного
    document.querySelectorAll('.favorite-link').forEach(function(link) {
        link.addEventListener('click', function(event) {
            event.preventDefault();
            const productId = link.getAttribute('data-product-id');
            const heartIcon = link.querySelector('img');
    
            if (heartIcon.src.includes('like.png')) {
                fetch(`/remove-from-favorite/${productId}/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken'),
                        'Content-Type': 'application/json'
                    }
                })
                .then(response => response.json())
                .then(data => {
                    heartIcon.src = heartImgPath;
                })
                .catch(error => console.error('Произошла ошибка при удалении товара из избранного:', error));
            } else {
                fetch(`/add-to-favorite/${productId}/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken'),
                        'Content-Type': 'application/json'
                    }
                })
                .then(response => response.json())
                .then(data => {
                    heartIcon.src = likeImgPath;
                    if (!data.authenticated) {
                        window.location.href = data.redirect;
                    }
                })
                .catch(error => console.error('Произошла ошибка:', error));
            }
        });
    });
    // Код добавления и удаления из корзины
    document.querySelectorAll('.add-to-cart-link').forEach(function(link) {
        link.addEventListener('click', function(event) {
            event.preventDefault();
            const productId = link.getAttribute('data-product-id');

            if (link.dataset.added === 'true') { // Удаление товара из корзины
                fetch(`/cart/ajax/remove/${productId}/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken'),
                        'Content-Type': 'application/json'
                    }
                })
                .then(response => response.json())
                .then(data => {
                    link.querySelector('img').setAttribute('src', cartImgPath);
                    link.dataset.added = 'false';
                    updateCartData();
                })
                .catch(error => console.error('Произошла ошибка при удалении товара из корзины:', error));
            } else {
                fetch(`/cart/ajax/add/${productId}/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken'),
                        'Content-Type': 'application/json'
                    }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        link.querySelector('img').setAttribute('src', okImgPath);
                        link.dataset.added = 'true';
                        updateCartData();
                    }
                })
                .catch(error => console.error('Произошла ошибка:', error));
            }
        });
    });

    function getCookie(name) {
        return document.cookie.split('; ').find(c => c.startsWith(name + '=')).split('=')[1];
    }

    function updateCartData() {
        fetch('/cart/count/', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            const cartCountElement = document.querySelector('#cart-count-element');
            cartCountElement.textContent = data.total_items;
        })
        .catch(error => console.error('Произошла ошибка при обновлении количества товаров в корзине:', error));
    }
});