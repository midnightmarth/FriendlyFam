
function validation() {
    var username = document.getElementById("username");
    var username_error = document.getElementById("error_username");
    var password = document.getElementById("password");
    var password_error = document.getElementById("error_password");
    var confirm_password = document.getElementById("confirm_password");
    var confirm_error = document.getElementById("error_confirm");
    // Validate Username
    if (username.value == "") {
        username.style.border = "1px solid red";
        username.style.color = "red";
        username_error.textContent = "Username is required";
        username_error.style.color = "red";
        username.focus();
        return false;
    }
    else {
        if (username.value.length <= 4) {
            username_error.innerHTML = "Username is too short.";
            username_error.style.color = "#FF0000"; //red color
            return false;
        }
        else if (username.value.length > 15) {
            username_error.innerHTML = "Username is too long.";
            username_error.style.color = "#FF0000"; //red color
            return false;
        }
        else {
            username.style.border = "1px solid #ced4da";
            username.style.color = "#495057";
            username_error.textContent = "";
        }
    }
    // Validate Password
    if (password.value == "") {
        password.style.border = "1px solid red";
        password.style.color = "red";
        password_error.textContent = "password is required";
        password_error.style.color = "red";
        password.focus();
        return false;
    }
    else {
        if (password.value.length <= 6) {
            password_error.innerHTML = "Password is too short.";
            password_error.style.color = "#FF0000"; //red color
            return false;
        }
        else if (password.value.length > 15) {
            password_error.innerHTML = "Password is too long.";
            password_error.style.color = "#FF0000";
            return false;
        }
        else {
            password.style.border = "1px solid #ced4da";
            password.style.color = "#495057";
            password_error.textContent = "";
        }
    }
    // Validate confirm password
    if (confirm_password.value == "") {
        confirm_password.style.border = "1px solid red";
        confirm_password.style.color = "red";
        confirm_error.textContent = "confirm password is required";
        confirm_error.style.color = "red";
        confirm_password.focus();
        return false;
    }
    else {
        confirm_password.style.border = "1px solid #ced4da";
        confirm_password.style.color = "#495057";
        confirm_error.textContent = "";
    }
}