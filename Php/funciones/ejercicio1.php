<?php
function calcularDescuento($totalCompra){
    if ($totalCompra >= 100){
        return $totalCompra*0.10;
    }else {
        return 0;
    }
}
$miDescuento = calcularDescuento(150);
echo "Tu descuento es de..." . $miDescuento;