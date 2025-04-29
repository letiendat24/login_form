
$(document).ready(function() {
    $('#login-btn').click(function() {
        const username = $('#username').val().trim();
        const password = $('#password').val().trim();

        if (!username || !password) {
            $('#error-msg').text('Vui lòng nhập đầy đủ thông tin.');
            return;
        }

        const hashedPassword = CryptoJS.MD5(password).toString();

        $.ajax({
            url: '/loginsys/login',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ username, password: hashedPassword }),
            success: function(response) {
                if (response.success) {
                    window.location.href = "/loginsys/dashboard";
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
// $(document).ready(function() {
//     // Ẩn/hiện form
//     $('#show-register').click(function() {
//         $('#login-form').hide();
//         $('#register-form').show();
//     });

//     $('#show-login').click(function() {
//         $('#register-form').hide();
//         $('#login-form').show();
//     });

//     // Xử lý Đăng nhập
//     $('#login-btn').click(function() {
//         const username = $('#username').val().trim();
//         const password = $('#password').val().trim();

//         if (!username || !password) {
//             $('#error-msg').text('Vui lòng nhập đầy đủ thông tin.');
//             return;
//         }

//         $.ajax({
//             url: '/login',
//             method: 'POST',
//             contentType: 'application/json',
//             data: JSON.stringify({ username, password }),
//             success: function(response) {
//                 if (response.success) {
//                     window.location.href = "/dashboard";
//                 } else {
//                     $('#error-msg').text(response.message);
//                 }
//             },
//             error: function() {
//                 $('#error-msg').text('Có lỗi kết nối server.');
//             }
//         });
//     });

//     // Xử lý Đăng ký
//     $('#register-btn').click(function() {
//         const username = $('#register-username').val().trim();
//         const password = $('#register-password').val().trim();

//         if (!username || !password) {
//             $('#error-msg-register').text('Vui lòng nhập đầy đủ thông tin.');
//             return;
//         }

//         $.ajax({
//             url: '/register',
//             method: 'POST',
//             contentType: 'application/json',
//             data: JSON.stringify({ username, password }),
//             success: function(response) {
//                 if (response.success) {
//                     alert('Đăng ký thành công! Mời bạn đăng nhập.');
//                     $('#show-login').click();  // Chuyển về form đăng nhập
//                 } else {
//                     $('#error-msg-register').text(response.message);
//                 }
//             },
//             error: function() {
//                 $('#error-msg-register').text('Có lỗi kết nối server.');
//             }
//         });
//     });
// });


