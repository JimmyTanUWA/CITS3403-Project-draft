$('#signUpBtn').click(function() {
    window.location.href = 'signup.html'; // Redirect to the signup page
});

$('#signInBtn').click(function() {
    window.location.href = 'signin.html'; // Redirect to the signin page
});
//this part should remain unchanged

$(document).ready(function() {
    $('body').fadeIn(800); // Fade-in effect for the body

    $('#signUpForm').submit(function(event) {
        event.preventDefault(); // Prevent the default form submission

        // Clear previous messages
        $('.error, .success').remove();

        var email = $('input[type="email"]').val();
        var password = $('input[type="password"]').val();
        var hasError = false;

        var emailRegex = /^[\w-\.]+@gmail\.com$/; // Regex for Gmail address validation
        var passwordRegex = /^(?=.*[A-Z])(?=.*[!@#$%^&*])[a-zA-Z\d!@#$%^&*]{6,}$/; // Regex for password validation

        if (!emailRegex.test(email)) {
            $('<span class="error">Email must be a valid Gmail address.</span>')
                .css({ color: 'red', marginLeft: '10px' })
                .insertAfter('input[type="email"]');
            hasError = true;
        }

        if (!passwordRegex.test(password)) {
            $('<span class="error">Password must be at least 6 characters, include one uppercase, and one special character.</span>')
                .css({ color: 'red', marginLeft: '10px' })
                .insertAfter('input[type="password"]');
            hasError = true;
        }

        if (!hasError) {
            let countdown = 2; // Set the countdown duration in seconds
            $('<span class="success">✔ Signup successful! Redirecting in ' + countdown + ' seconds...</span>')
                .css({ color: 'green', marginLeft: '10px' })
                .insertAfter('#signUpForm button[type="submit"]');

            // Countdown function to update the message each second
            var intervalId = setInterval(function() {
                countdown--;
                if (countdown === 0) {
                    clearInterval(intervalId);
                    window.location.href = 'index.html'; // Redirect to the home page
                } else {
                    $('.success').text('✔ Signup successful! Redirecting in ' + countdown + ' seconds...');
                }
            }, 1000); // Update every second
        }
    });
});
