var dominiosPermitidos = ['gmail.com', 'hotmail.com', 'outlook.com', 'yahoo.com'];

function validarEmailTiempoReal(input) {
    var email = input.value.trim();
    var feedback = document.getElementById('emailFeedback');
    
    if (!email) {
        if (feedback) feedback.style.display = 'none';
        return {valid: false, message: ''};
    }
    
    var partes = email.split('@');
    var isValid = false;
    var message = '';
    
    if (partes.length !== 2) {
        message = '✗ Formato de email inválido';
    } else {
        var dominio = partes[1].toLowerCase();
        if (!dominiosPermitidos.includes(dominio)) {
            message = '✗ Dominio no permitido. Use: ' + dominiosPermitidos.join(', ');
        } else {
            isValid = true;
            message = '✓ Email válido';
        }
    }
    
    if (feedback) {
        feedback.innerHTML = message;
        feedback.className = 'feedback-message ' + (isValid ? 'feedback-success' : 'feedback-error');
        feedback.style.display = 'block';
    }
    
    return {valid: isValid, message: message};
}

function validarPasswordTiempoReal(input) {
    var password = input.value;
    var feedback = document.getElementById('passwordFeedback');
    
    if (!password) {
        if (feedback) feedback.style.display = 'none';
        return {valid: false};
    }
    
    var hasLength = password.length >= 8;
    var hasLetter = /[A-Za-z]/.test(password);
    var hasNumber = /\d/.test(password);
    var hasSymbol = /[@$!%*#?&]/.test(password);
    
    var isValid = hasLength && hasLetter && hasNumber && hasSymbol;
    
    if (feedback) {
        feedback.innerHTML = isValid ? '✓ Contraseña válida' : '✗ La contraseña debe tener 8+ caracteres con letras, números y un símbolo';
        feedback.className = 'feedback-message ' + (isValid ? 'feedback-success' : 'feedback-error');
        feedback.style.display = 'block';
    }
    
    return {valid: isValid};
}

function validarConfirmacionPassword() {
    // NOTA: Como prependId="false", usamos solo 'password' y 'confirmPassword' no 'registerForm:password'
    var password = document.getElementById('password').value;
    var confirmacion = document.getElementById('confirmPassword').value;
    var feedback = document.getElementById('confirmFeedback');
    
    if (!confirmacion) {
        if (feedback) feedback.style.display = 'none';
        return {valid: false};
    }
    
    var isValid = password === confirmacion;
    
    if (feedback) {
        feedback.innerHTML = isValid ? '✓ Las contraseñas coinciden' : '✗ Las contraseñas no coinciden';
        feedback.className = 'feedback-message ' + (isValid ? 'feedback-success' : 'feedback-error');
        feedback.style.display = 'block';
    }
    
    return {valid: isValid};
}

function validarFormularioCompleto() {
    // NOTA: Como prependId="false", usamos solo los IDs simples
    var emailInput = document.getElementById('email');
    var passwordInput = document.getElementById('password');
    
    var emailValid = validarEmailTiempoReal(emailInput);
    var passwordValid = validarPasswordTiempoReal(passwordInput);
    var confirmValid = validarConfirmacionPassword();
    
    var allValid = emailValid.valid && passwordValid.valid && confirmValid.valid;
    
    if (!allValid) {
        var mensaje = 'Por favor corrige los siguientes errores:\n\n';
        if (!emailValid.valid) mensaje += '- ' + emailValid.message.replace('✗ ', '') + '\n';
        if (!passwordValid.valid) mensaje += '- La contraseña no cumple los requisitos\n';
        if (!confirmValid.valid) mensaje += '- Las contraseñas no coinciden\n';
        
        if (typeof PF !== 'undefined') {
            PF('growl').show([
                {
                    summary: 'Error de validación',
                    detail: 'Por favor corrige los errores en el formulario.',
                    severity: 'error'
                }
            ]);
        }
        
        return false;
    }
    
    return true;
}

document.addEventListener('DOMContentLoaded', function() {
    // NOTA: Como prependId="false", usamos solo los IDs simples
    var emailInput = document.getElementById('email');
    var passwordInput = document.getElementById('password');
    var confirmInput = document.getElementById('confirmPassword');
    
    if (emailInput) {
        emailInput.addEventListener('input', function() { validarEmailTiempoReal(this); });
        emailInput.addEventListener('blur', function() { validarEmailTiempoReal(this); });
    }
    
    if (passwordInput) {
        passwordInput.addEventListener('input', function() { validarPasswordTiempoReal(this); });
        passwordInput.addEventListener('blur', function() { validarPasswordTiempoReal(this); });
    }
    
    if (confirmInput) {
        confirmInput.addEventListener('input', validarConfirmacionPassword);
        confirmInput.addEventListener('blur', validarConfirmacionPassword);
    }
});