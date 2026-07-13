<?php
$num1=67;
$num2=69;
$operacion="**";
switch($operacion){
    case "+":
        echo ($num1+$num2);
        break;
    case "-":
        echo ($num1-$num2);
        break;
    case "/":
        echo ($num2!=0)?$num1/$num2:"Error: division entre cero...";
        break;
    case "*":
        echo ($num1*$num2);
        break;
//num1 (base) num2 (exponente)        
    case "**":
        echo ($num1**$num2);
        break;
//num1 (radicando) num2 (indice)        
    case "R":
        echo (($num2!=0||$num1>0)?$num1**(1/$num2):"Error: raiz no valida...");
        break;
    default:
        echo "operacion no valida";    
}
?> 
#Patentado por victor muñoz (Dios)
#copyright todos los derechos reservados 
#No plagiar (porfi)