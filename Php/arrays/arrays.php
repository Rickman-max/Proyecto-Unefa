<?php
/* un array es un tipo de valor
donde se puede meter cualquier tipo de Arrays
#Tipos de arrays*/ 
#escalar 
$estudiantes=array("Rickman","Juan","Luis");
$estudiantes[2]= "Jose";
echo $estudiantes[2];
#asociativos 
$profesor=[
    "nombre"=>"Alonzo",
    "apellido"=>"Perez",
    "edad"=>25
];
$profesor["edad"]=19;
echo $profesor["edad"];
#multidimensionales 
$profesor_2=[
    "nombre"=>"Rickman",
    "apellido"=>"Melendez",
    "edad"=>25,
    "cursos"=>["PHP","Python","Javascript",]
];
$profesor_2["cursos"][2]="CSS";
echo $profesor_2["cursos"][2];
echo count($profesor_2, COUNT_RECURSIVE);