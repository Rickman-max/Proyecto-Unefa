<?php
// Forzamos al servidor local a responder únicamente datos JSON planos
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *'); // Por si decides conectar esta API a una app externa

// Capturamos el tipo de operación de la URL (ej: ?tipo=derivada)
$tipo = isset($_GET['tipo']) ? $_GET['tipo'] : 'basica';

$respuesta = [
    'success' => false,
    'resultado' => null,
    'error' => null
];

switch ($tipo) {
    case 'basica':
        // Parámetros: ?tipo=basica&n1=10&n2=5&op=suma
        $n1  = isset($_GET['n1']) ? floatval($_GET['n1']) : 0;
        $n2  = isset($_GET['n2']) ? floatval($_GET['n2']) : 0;
        $op  = isset($_GET['op']) ? $_GET['op'] : 'suma';

        if ($op === 'suma') $respuesta['resultado'] = $n1 + $n2;
        elseif ($op === 'resta') $respuesta['resultado'] = $n1 - $n2;
        elseif ($op === 'mult') $respuesta['resultado'] = $n1 * $n2;
        elseif ($op === 'div') {
            if ($n2 == 0) $respuesta['error'] = "División por cero";
            else $respuesta['resultado'] = $n1 / $n2;
        } else {
            $respuesta['error'] = "Operación básica no soportada (usa: suma, resta, mult, div)";
        }
        break;

    case 'derivada':
        // Parámetros: ?tipo=derivada&x=2
        // Función fija: f(x) = x^3 + 2x
        $x = isset($_GET['x']) ? floatval($_GET['x']) : 0;
        $f = function($x) { return pow($x, 3) + (2 * $x); };
        $h = 0.00001; 

        $derivada = ($f($x + $h) - $f($x - $h)) / (2 * $h);
        $respuesta['resultado'] = round($derivada, 5);
        $respuesta['info'] = "Derivada de f(x) = x^3 + 2x evaluada en x = $x";
        break;

    case 'parcial':
        // Parámetros: ?tipo=parcial&x=3&y=2&respecto=x
        // Función fija: f(x, y) = (x^2 * y) + y^3
        $x = isset($_GET['x']) ? floatval($_GET['x']) : 0;
        $y = isset($_GET['y']) ? floatval($_GET['y']) : 0;
        $respecto = isset($_GET['respecto']) ? $_GET['respecto'] : 'x';
        $f_xy = function($x, $y) { return (pow($x, 2) * $y) + pow($y, 3); };
        $h = 0.00001;

        if ($respecto === 'x') {
            $parcial = ($f_xy($x + $h, $y) - $f_xy($x - $h, $y)) / (2 * $h);
        } else {
            $parcial = ($f_xy($x, $y + $h) - $f_xy($x, $y - $h)) / (2 * $h);
        }
        $respuesta['resultado'] = round($parcial, 5);
        $respuesta['info'] = "Derivada parcial respecto a '$respecto' de f(x,y) = x^2*y + y^3 en ($x, $y)";
        break;

    case 'integral':
        // Parámetros: ?tipo=integral&a=0&b=2
        // Función fija: f(x) = x^2
        $a = isset($_GET['a']) ? floatval($_GET['a']) : 0;
        $b = isset($_GET['b']) ? floatval($_GET['b']) : 0;
        $f_int = function($x) { return pow($x, 2); };
        $n = 1000; 
        
        $h = ($b - $a) / $n;
        $suma = $f_int($a) + $f_int($b);
        for ($i = 1; $i < $n; $i++) {
            $x_val = $a + $i * $h;
            $suma += ($i % 2 == 0) ? 2 * $f_int($x_val) : 4 * $f_int($x_val);
        }
        $respuesta['resultado'] = round(($h / 3) * $suma, 5);
        $respuesta['info'] = "Integral definida (Área) de f(x) = x^2 desde $a hasta $b";
        break;

    case 'edo':
        // Parámetros: ?tipo=edo&x0=0&y0=1&xf=2
        // EDO: dy/dx = x + y (Método Runge-Kutta 4)
        $x0 = isset($_GET['x0']) ? floatval($_GET['x0']) : 0;
        $y0 = isset($_GET['y0']) ? floatval($_GET['y0']) : 0;
        $xf = isset($_GET['xf']) ? floatval($_GET['xf']) : 0;
        
        $dydx = function($x, $y) { return $x + $y; };
        $n = 100; 
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
        $respuesta['resultado'] = round($y, 5);
        $respuesta['info'] = "Resolución de dy/dx = x + y con condición inicial y($x0)=$y0, evaluado en x = $xf";
        break;

    default:
        $respuesta['error'] = "Tipo de cálculo no reconocido (Elige: basica, derivada, parcial, integral, edo)";
}

// Si no se generaron errores durante el proceso, la petición fue exitosa
if ($respuesta['error'] === null) {
    $respuesta['success'] = true;
}

// Retornamos la estructura JSON limpia
echo json_encode($respuesta, JSON_PRETTY_PRINT);