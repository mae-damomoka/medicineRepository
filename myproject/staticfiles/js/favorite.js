document.addEventListener('DOMContentLoaded', (event) => {
    document.querySelectorAll('.favorite-button').forEach(button => {
        button.addEventListener('click', (e) => {
            e.preventDefault();
            const hospitalId = button.dataset.hospitalId;
            fetch(`/toggle_favorite/${hospitalId}/`, { method: 'POST' })
            .then(response => {
                if (response.ok) {
                    return response.json();
                }
                throw new Error('Network response was not ok.');
            })
            .then(data => {
                // ここで病院の欄の色を変更
            })
            .catch(error => {
                console.error('There has been a problem with your fetch operation:', error);
            });
        });
    });
});
