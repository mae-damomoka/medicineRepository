document.addEventListener('DOMContentLoaded', (event) => {
    // '.toggle-favorite' クラスを持つ全てのお気に入りボタンに対してイベントリスナーを設定
    document.querySelectorAll('.toggle-favorite').forEach(button => {
        button.addEventListener('click', (e) => {
            e.preventDefault(); // デフォルトのフォーム送信を防止
            const hospitalId = button.dataset.hospitalId; // 'data-hospital-id' 属性から病院IDを取得

            // サーバーに対してお気に入りトグルリクエストを送信するためのフェッチリクエストを実行
            fetch(`/toggle_favorite/${hospitalId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ 'hospital_id': hospitalId })
            })
            .then(response => {
                if (response.ok) {
                    return response.json(); // JSONレスポンスをパース
                } else {
                    throw new Error('Something went wrong on api server!');
                }
            })
            .then(data => {
                // 応答に基づいてDOMの操作を行う
                if (data.is_favorite !== undefined) {
                    // お気に入りスタイルを切り替える
                    const hospitalRow = document.querySelector(`#hospital-${hospitalId}`);
                    if (data.is_favorite) {
                        hospitalRow.classList.add('favorite');
                    } else {
                        hospitalRow.classList.remove('favorite');
                    }
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    });
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // クッキーの名前が一致するかをチェック
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
