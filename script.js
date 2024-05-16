$(document).ready(function() {
    // Fade-in 效果
    $('body').fadeIn(800);

    // 提交注册表单的事件处理
    $('#signUpForm').submit(function(event) {
        event.preventDefault(); // 阻止表单默认提交

        // 清除以前的消息
        $('.error, .success').remove();

        var email = $('input[type="email"]').val();
        var password = $('input[type="password"]').val();
        var hasError = false;

        var emailRegex = /^[\w-\.]+@gmail\.com$/; // 仅验证 Gmail 地址
        var passwordRegex = /^(?=.*[A-Z])(?=.*[!@#$%^&*])[a-zA-Z\d!@#$%^&*]{6,}$/; // 密码验证

        // 邮箱验证
        if (!emailRegex.test(email)) {
            $('<span class="error">Email must be a valid Gmail address.</span>')
                .css({ color: 'red', marginLeft: '10px' })
                .insertAfter('input[type="email"]');
            hasError = true;
        }

        // 密码验证
        if (!passwordRegex.test(password)) {
            $('<span class="error">Password must be at least 6 characters, include one uppercase, and one special character.</span>')
                .css({ color: 'red', marginLeft: '10px' })
                .insertAfter('input[type="password"]');
            hasError = true;
        }

        // 如果没有错误，处理重定向
        if (!hasError) {
            let countdown = 2; // 倒计时持续时间（秒）
            $('<span class="success">✔ Signup successful! Redirecting in ' + countdown + ' seconds...</span>')
                .css({ color: 'green', marginLeft: '10px' })
                .insertAfter('#signUpForm button[type="submit"]');

            // 倒计时更新消息
            var intervalId = setInterval(function() {
                countdown--;
                if (countdown === 0) {
                    clearInterval(intervalId);
                    window.location.href = 'index.html'; // 重定向到首页
                } else {
                    $('.success').text('✔ Signup successful! Redirecting in ' + countdown + ' seconds...');
                }
            }, 1000);
        }
    });

    // 点击事件处理：注册和登录按钮
    $('#signUpBtn').click(function() {
        window.location.href = "signup"; // 使用变量跳转到注册页面
    });

    $('#signInBtn').click(function() {
        window.location.href = "signin"; // 使用变量跳转到登录页面
    });
});
