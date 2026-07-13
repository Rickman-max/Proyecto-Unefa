<?php
$nombre_registro = "Juan";
$cantidad_letras = strlen ( $nombre_registro);
if ($cantidad_letras < 4){
    echo "El nombre es muy corto";
}else{
    $nombre_limpio = strtoupper ( $nombre_registro);
    echo "Registrado con exito " . $nombre_limpio;
}

