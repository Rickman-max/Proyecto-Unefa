<?php
session_start();


require_once 'conexion.php';


if ($_SERVER['REQUEST_METHOD'] === 'POST') {
   
    $rawEmail = isset($_POST['correo']) ? trim($_POST['correo']) : '';
    $rawPassword  = isset($_POST['contrasena']) ? $_POST['contrasena'] : '';

   
    if (empty($rawEmail) || empty($rawPassword)) {
        die("Error: Todos los campos de acceso son obligatorios.");
    }

    $secureEmail = filter_var($rawEmail, FILTER_VALIDATE_EMAIL);
    if (!$secureEmail) {
        die("Error: El formato del identificador de acceso es inválido.");
    }
    
    
    $sanitizedEmail = filter_var($secureEmail, FILTER_SANITIZE_STRING);

    try {

        $sqlSelect = "SELECT id, nombre, correo, contrasena FROM usuarios WHERE correo = :email LIMIT 1";
        $stmt = $pdo->prepare($sqlSelect);
        $stmt->execute([':email' => $sanitizedEmail]);
        
        $user = $stmt->fetch();

        
        if ($user && password_verify($rawPassword, $user['contrasena'])) {
            
            
            $_SESSION['user_id']   = $user['id'];
            $_SESSION['user_name'] = $user['nombre'];
            $_SESSION['source_ip'] = $_SERVER['REMOTE_ADDR']; 
            echo "Autenticacion Correcta";
            
            
        } else {
            
            echo "Alerta de Acceso: Credenciales incorrectas";
        }

    } catch (PDOException $exception) {
        
        error_log("Fallo en el subsistema de Login: " . $exception->getMessage());
        die("Error crítico, Intente más tarde.");
    }
} else {
    
    header("HTTP/1.1 405 Method Not Allowed");
    echo "Metodología HTTP no permitida para esta transacción.";
}
?>