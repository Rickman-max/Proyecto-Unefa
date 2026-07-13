<?php
function contarAprobados($listaNotas){
        $aprobados = 0;
    foreach($listaNotas as $notas){
        if($notas >= 5){
$aprobados++;
}   
} 
return $aprobados;
}
$misNotas= [1,5,7,6,9,4];
$totalAprobados= contarAprobados($misNotas);
echo "El numero de aprobados es..." . "$totalAprobados";