$(document).ready(function() {
    $('#register-btn').click(function() {
        const username = $('#reg-username').val().trim();
        const password = $('#reg-password').val().trim();

        if (!username || !password) {
            $('#error-msg').text('Vui lòng nhập đầy đủ thông tin.');
            return;
        }

        $.ajax({
            url: '/api/register',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ username, password }),
            success: function(response) {
                if (response.success) {
                    alert('Đăng ký thành công! Mời bạn đăng nhập.');
                    window.location.href = "/";
                } else {
                    $('#error-msg').text(response.message);
                }
            },
            error: function() {
                $('#error-msg').text('Có lỗi xảy ra khi kết nối đến máy chủ.');
            }
        });
    });
});
