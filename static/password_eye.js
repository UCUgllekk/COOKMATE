const togglePassword = document.querySelector('#togglePassword');
const password = document.querySelector('#password');

togglePassword.addEventListener('click', function (e) {
    // toggle the type attribute
    const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
    const eyeStyle = password.getAttribute('type') === 'password' ? 'fa fa-eye' : 'fa fa-eye-slash';
    password.setAttribute('type', type);
    // toggle the eye icon
    console.log(this)
    console.log(this.getElementsByTagName("i")[0])
    this.getElementsByTagName("i")[0].classList = eyeStyle;
    password.focus()
});
