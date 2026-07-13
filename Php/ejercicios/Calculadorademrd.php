<?php
$f = fn($x) => pow($x, 2); // f(x) = x²
$f_parcial = fn($x, $y) => pow($x, 2) + pow($y, 3);
$dydx = fn($x, $y) => $x; 
$h = 0.00001;

function calcularBasicas($a, $b) {
    return [
        "Suma"           => $a + $b,
        "Resta"          => $a - $b,
        "Multiplicación" => $a * $b,
        "División"       => ($b != 0) ? $a / $b : "Error: División por cero"
    ];
}

$derivada_num = fn($x) => ($f($x + $h) - $f($x)) / $h;

$derivada_parcial_x = fn($x, $y) => ($f_parcial($x + $h, $y) - $f_parcial($x, $y)) / $h;

function integralDefinida($func, $a, $b, $pasos = 1000) {
    $dx = ($b - $a) / $pasos;
    $suma = 0;
    for ($i = 0; $i < $pasos; $i++) {
        $suma += (($func($a + $i * $dx) + $func($a + ($i + 1) * $dx)) / 2) * $dx;
    }
    return $suma;
}

function resolverEDO($func_dydx, $x0, $y0, $xf, $pasos = 100) {
    $dt = ($xf - $x0) / $pasos;
    for ($i = 0; $i < $pasos; $i++) {
        $y0 += $func_dydx($x0, $y0) * $dt;
        $x0 += $dt;
    }
    return $y0;
}
echo "=== CALCULADORA BÁSICA ===\n";
foreach (calcularBasicas(10, 5) as $operacion => $resultado) {
    echo "$operacion: $resultado\n";
}

echo "\n=== CÁLCULO AVANZADO (f(x) = x²) ===\n";
echo "Derivada analítica (Texto): d/dx(x²) = 2x\n";
echo "Derivada numérica en x=3: " . round($derivada_num(3), 4) . "\n";
echo "Integral indefinida (Texto): ∫(x²)dx = (x³/3) + C\n";
echo "Integral definida [0 a 2]: " . round(integralDefinida($f, 0, 2), 4) . "\n";

echo "\n=== ECUACIONES DIFERENCIALES Y PARCIALES ===\n";
echo "EDO (Euler) dy/dx=x con y(0)=1 -> Valor en y(2): " . round(resolverEDO($dydx, 0, 1, 2), 4) . "\n";
echo "Derivada Parcial df/dx de (x²+y³) en el punto (2,3): " . round($derivada_parcial_x(2, 3), 4) . "\n";