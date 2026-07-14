<?php
class Conexion {
    private $servidor = "localhost";
    private $basedatos = "proyecto_unefa"; 
    private $usuario   = "root";        
    private $contrasena = "";            
    
    public $conexion;
    public function conectar() {
        $this->conexion = null;
        
        try {
            
            $this->conexion = new PDO("mysql:host=" . $this->servidor . ";dbname=" . $this->basedatos, $this->usuario, $this->contrasena);
            
            
            $this->conexion->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
            
            
            $this->conexion->exec("set names utf8");
            
        } catch(PDOException $excepcion) {
            
            echo "Error de conexión: " . $excepcion->getMessage();
        }
        
        
        return $this->conexion;
    }
}
?>