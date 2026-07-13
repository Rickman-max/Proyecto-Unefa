<?php
if (php_sapi_name() !== "cli") {
    die("Este script está diseñado para ejecutarse en la terminal.\n");
}

echo "====================================================\n";
echo "   CALCULADORA CIENTÍFICA NUMÉRICA (PHP CLI)        \n";
echo "====================================================\n";
echo "1. Suma / Resta / Multiplicación / División\n";
echo "2. Derivada Numérica (en un punto)\n";
echo "3. Derivada Parcial Numérica\n";
echo "4. Integral Definida (Método de Simpson)\n";
echo "5. Ecuación Diferencial (Método de Runge-Kutta 4)\n";
echo "====================================================\n";

echo "Selecciona una opción (1-5): ";
$opcion = intval(trim(fgets(STDIN)));

switch ($opcion) {
    case 1:
        echo "Introduce primer número: "; $n1 = floatval(trim(fgets(STDIN)));
        echo "Introduce segundo número: "; $n2 = floatval(trim(fgets(STDIN)));
        echo "Operación (+, -, *, /): "; $op = trim(fgets(STDIN));
        
        if ($op == '+') echo "Resultado: " . ($n1 + $n2) . "\n";
        elseif ($op == '-') echo "Resultado: " . ($n1 - $n2) . "\n";
        elseif ($op == '*') echo "Resultado: " . ($n1 * $n2) . "\n";
        elseif ($op == '/') echo $n2 == 0 ? "Error: División por cero\n" : "Resultado: " . ($n1 / $n2) . "\n";
        break;

    case 2:
        echo "Ejemplo de función programada: f(x) = x^3 + 2x\n";
        $f = function($x) { return pow($x, 3) + (2 * $x); };
        
        echo "Introduce el punto x donde evaluar la derivada: ";
        $x = floatval(trim(fgets(STDIN)));
        $h = 0.00001;
        
        $derivada = ($f($x + $h) - $f($x - $h)) / (2 * $h);
        echo "La derivada aproximada en x = $x es: " . round($derivada, 5) . "\n";
        break;

    case 3:
        echo "Ejemplo de función: f(x, y) = x^2 * y + y^3\n";
        $f_xy = function($x, $y) { return (pow($x, 2) * $y) + pow($y, 3); };
        
        echo "Introduce punto x: "; $x = floatval(trim(fgets(STDIN)));
        echo "Introduce punto y: "; $y = floatval(trim(fgets(STDIN)));
        echo "Respecto a cuál variable derivar? (x / y): "; $var = trim(fgets(STDIN));
        $h = 0.00001;

        if ($var === 'x') {
            $parcial = ($f_xy($x + $h, $y) - $f_xy($x - $h, $y)) / (2 * $h);
        } else {
            $parcial = ($f_xy($x, $y + $h) - $f_xy($x, $y - $h)) / (2 * $h);
        }
        echo "La derivada parcial respecto a $var en ($x, $y) es: " . round($parcial, 5) . "\n";
        break;

    case 4:
        
        echo "Ejemplo de función a integrar: f(x) = x^2\n";
        $f_int = function($x) { return pow($x, 2); };
        
        echo "Límite inferior (a): "; $a = floatval(trim(fgets(STDIN)));
        echo "Límite superior (b): "; $b = floatval(trim(fgets(STDIN)));
        $n = 1000;
        
        $h = ($b - $a) / $n;
        $suma = $f_int($a) + $f_int($b);
        
        for ($i = 1; $i < $n; $i++) {
            $x = $a + $i * $h;
            $suma += ($i % 2 == 0) ? 2 * $f_int($x) : 4 * $f_int($x);
        }
        $integral = ($h / 3) * $suma;
        echo "El área bajo la curva (integral definida) de $a a $b es: " . round($integral, 5) . "\n";
        break;

    case 5:
        echo "Ejemplo de EDO: dy/dx = x + y\n";
        $dydx = function($x, $y) { return $x + $y; };
        
        echo "Condición inicial x0: "; $x0 = floatval(trim(fgets(STDIN)));
        echo "Condición inicial y0 (valor de y en x0): "; $y0 = floatval(trim(fgets(STDIN)));
        echo "Punto x final donde quieres evaluar y: "; $xf = floatval(trim(fgets(STDIN)));
        
        $n = 100; // Pasos
        $h = ($xf - $x0) / $n;
        $x = $x0;
        $y = $y0;

        for ($i = 0; $i < $n; $i++) {
            $k1 = $h * $dydx($x, $y);
            $k2 = $h * $dydx($x + $h/2, $y + $k1/2);
            $k3 = $h * $dydx($x + $h/2, $y + $k2/2);
            $k4 = $h * $dydx($x + $h, $y + $k3);
            
            $y += ($k1 + 2*$k2 + 2*$k3 + $k4) / 6;
            $x += $h;
        }
        echo "El valor aproximado de y en x = $xf es: " . round($y, 5) . "\n";
        break;

    default:
        echo "Opción inválida.\n";
        break;
}
echo "\n";