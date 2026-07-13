<?php
function calcularEnvio($totalCarrito){
    if ($totalCarrito >= 50 ){
        return 0;
    }else{
    return 5;
    }
}
echo "Cliente A (Gasta 65$). Coste de envio: " . calcularEnvio(65) . "$<br>";
echo "Cliente B (Gasta 35$). Coste de envio: " . calcularEnvio(35) . "$<br>";
