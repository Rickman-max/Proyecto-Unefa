<?php
function formatearPrecio($numero){
    $precioLimpio = number_format($numero, 2);
    return $precioLimpio;
}
$precioFinal = formatearPrecio(4999.5);
echo "El precio de la playera es: $" . "$precioFinal";