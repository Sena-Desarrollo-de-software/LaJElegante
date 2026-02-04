package beans;

import dao.ClienteDAO;
import models.Cliente;
import models.TipoCliente;
import models.enums.Estado;
import models.enums.Saludo;
import utils.MessageUtil;
import utils.Utils;
import javax.faces.bean.ManagedBean;
import javax.faces.bean.RequestScoped;
import java.io.Serializable;
import java.util.regex.Pattern;

@ManagedBean
@RequestScoped
public class RegistroBean implements Serializable {
    private static final long serialVersionUID = 1L;
    
    private String nombre;
    private String apellido;
    private String email;
    private String saludo = "MX";
    private String prefijoTelefono = "+57";
    private String numeroTelefono;
    private String password;
    private String confirmPassword;
    
    // Getters y Setters
    public String getNombre() { return nombre; }
    public void setNombre(String nombre) { this.nombre = nombre; }
    
    public String getApellido() { return apellido; }
    public void setApellido(String apellido) { this.apellido = apellido; }
    
    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }
    
    public String getSaludo() { return saludo; }
    public void setSaludo(String saludo) { this.saludo = saludo; }
    
    public String getPrefijoTelefono() { return prefijoTelefono; }
    public void setPrefijoTelefono(String prefijoTelefono) { this.prefijoTelefono = prefijoTelefono; }
    
    public String getNumeroTelefono() { return numeroTelefono; }
    public void setNumeroTelefono(String numeroTelefono) { this.numeroTelefono = numeroTelefono; }
    
    public String getPassword() { return password; }
    public void setPassword(String password) { this.password = password; }
    
    public String getConfirmPassword() { return confirmPassword; }
    public void setConfirmPassword(String confirmPassword) { this.confirmPassword = confirmPassword; }
    
    // Métodos de validación
    public boolean validarDominioEmail(String email) {
        if (email == null || email.trim().isEmpty()) {
            return false;
        }
        
        String[] dominiosPermitidos = {"gmail.com", "lje.com", "hotmail.com", "outlook.com", "yahoo.com"};
        String[] partes = email.split("@");
        
        if (partes.length != 2) {
            return false;
        }
        
        String dominio = partes[1].toLowerCase();
        
        for (String dominioPermitido : dominiosPermitidos) {
            if (dominio.equals(dominioPermitido)) {
                return true;
            }
        }
        
        return false;
    }
    
    public boolean validarPassword(String password) {
        if (password == null || password.length() < 8) {
            return false;
        }
        String regex = "^(?=.*[A-Za-z])(?=.*\\d)(?=.*[@$!%*#?&\\-])[A-Za-z\\d@$!%*#?&\\-]{8,}$";
        return Pattern.matches(regex, password);
    }

    public String registrar() {
        try {
            if (!validarCamposCompletos()) {
                MessageUtil.requiredFieldsWarning();
                return null;
            }
            
            if (!validarDominioEmail(email)) {
                MessageUtil.error("Dominio no permitido", 
                    "Por favor usa un dominio válido: gmail.com, lje.com, hotmail.com, outlook.com o yahoo.com");
                return null;
            }

            if (!validarPassword(password)) {
                MessageUtil.error("Contraseña inválida",
                    "La contraseña debe tener al menos 8 caracteres, una letra, un número y un símbolo (@$!%*#?&)");
                return null;
            }

            if (!password.equals(confirmPassword)) {
                MessageUtil.validationError("Las contraseñas no coinciden");
                return null;
            }
            
            ClienteDAO clienteDAO = new ClienteDAO();
            Cliente clienteExistente = clienteDAO.buscarPorEmail(email);
            
            if (clienteExistente != null) {
                MessageUtil.duplicateError("email", email);
                return null;
            }
           
            String passwordHash = Utils.hashPassword(password);
            if (passwordHash == null) {
                MessageUtil.error("Error de seguridad", 
                    "No se pudo procesar la contraseña. Intenta nuevamente.");
                return null;
            }
            Cliente nuevoCliente = new Cliente();
            
            TipoCliente tipoCliente = new TipoCliente();
            tipoCliente.setIdTipoCliente(1);
            nuevoCliente.setTipoCliente(tipoCliente);
            nuevoCliente.setNombre(nombre.trim());
            nuevoCliente.setApellido(apellido.trim());
            nuevoCliente.setEmail(email.trim().toLowerCase());
            
            try {
                nuevoCliente.setSaludo(Saludo.valueOf(saludo));
            } catch (IllegalArgumentException e) {
                nuevoCliente.setSaludo(Saludo.MX);
            }
     
            nuevoCliente.setPrefijo(prefijoTelefono != null ? prefijoTelefono.trim() : "+57");
            nuevoCliente.setNumTel(numeroTelefono.trim());
            nuevoCliente.setContraseña(passwordHash);
            nuevoCliente.setEstado(Estado.ACTIVO);
            clienteDAO.crear(nuevoCliente);
            limpiarFormularioSeguro();
            MessageUtil.success("¡Registro exitoso! Tu cuenta ha sido creada correctamente.");
            return "/views/hotel/login.xhtml?faces-redirect=true&registro=exitoso";
            
        } catch (Exception e) {
            MessageUtil.error("Error del sistema", 
                "Ocurrió un error inesperado. Por favor intenta nuevamente.");
            return null;
        }
    }
    
    private boolean validarCamposCompletos() {
        return nombre != null && !nombre.trim().isEmpty() &&
               apellido != null && !apellido.trim().isEmpty() &&
               email != null && !email.trim().isEmpty() &&
               numeroTelefono != null && !numeroTelefono.trim().isEmpty() &&
               password != null && !password.trim().isEmpty() &&
               confirmPassword != null && !confirmPassword.trim().isEmpty();
    }
    
    private void limpiarFormularioSeguro() {
        this.nombre = null;
        this.apellido = null;
        this.email = null;
        this.saludo = "MR";
        this.prefijoTelefono = "+57";
        this.numeroTelefono = null;
        this.password = null;
        this.confirmPassword = null;
    }
    
    public void limpiarTodo() {
        this.nombre = null;
        this.apellido = null;
        this.email = null;
        this.saludo = "MR";
        this.prefijoTelefono = "+57";
        this.numeroTelefono = null;
        this.password = null;
        this.confirmPassword = null;
    }
    
    public String irALogin() {
        return "/views/hotel/login.xhtml?faces-redirect=true";
    }
}