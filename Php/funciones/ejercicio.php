<?php
$precio = 10.5; 
$cantidad = 3;
function calcularTotal($precio, $cantidad){
    return $precio * $cantidad;
}
echo "El total es..." . calcularTotal($precio,$cantidad)."$";
