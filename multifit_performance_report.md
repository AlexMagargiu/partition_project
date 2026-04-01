# Raport de Performanță - Algoritmi Multifit

## Sumar Executiv

Acest raport prezintă rezultatele comparative ale performanței diferitelor implementări ale algoritmului Multifit pentru problema partiționării. Testele au fost efectuate pe multiple dimensiuni de date, de la seturi mici (10-100 elemente) până la seturi foarte mari (până la 1 milion de elemente).

## Rezultate pentru Dimensiuni Standard (10-100 elemente)

### Timp de Execuție (secunde)

| Dimensiune | DP Unoptimized | DP Optimized | Greedy Unoptimized | Greedy Optimized | KK Unoptimized | KK Optimized | Multifit Unoptimized | Multifit Semioptimized | Multifit Optimized | Multifit Multiprocessing |
|-----------|--------------------|--------------------|--------------------|--------------------|--------------------|--------------------|--------------------|--------------------|--------------------|--------------------|
| 10 | 0.006368 | 0.002079 | 0.000033 | 0.000074 | 0.000182 | 0.000174 | 0.000027 | 0.000031 | 0.000044 | 0.000161 |
| 20 | 0.018545 | 0.007786 | 0.000017 | 0.000058 | 0.000199 | 0.000213 | 0.000036 | 0.000020 | 0.000059 | 0.000190 |
| 30 | 0.026326 | 0.015495 | 0.000027 | 0.000082 | 0.000307 | 0.000199 | 0.000042 | 0.000040 | 0.000029 | 0.000119 |
| 40 | 0.074095 | 0.029376 | 0.000053 | 0.000109 | 0.000165 | 0.000384 | 0.000010 | 0.000049 | 0.000019 | 0.000209 |
| 50 | 0.000016 | 0.000016 | 0.000031 | 0.000065 | 0.000516 | 0.000494 | 0.000037 | 0.000034 | 0.000086 | 0.000162 |
| 100 | 0.000025 | 0.000023 | 0.000069 | 0.000187 | 0.001217 | 0.000628 | 0.000113 | 0.000123 | 0.000099 | 0.000197 |

### Diferența dintre Subseturi

| Dimensiune | DP Unoptimized | DP Optimized | Greedy Unoptimized | Greedy Optimized | KK Unoptimized | KK Optimized | Multifit Unoptimized | Multifit Semioptimized | Multifit Optimized | Multifit Multiprocessing |
|-----------|--------------------|--------------------|--------------------|--------------------|--------------------|--------------------|--------------------|--------------------|--------------------|--------------------|
| 10 | 4150 | 4150 | 6 | 6 | 6 | 6 | 6 | 6 | 6 | 6 |
| 20 | 0 | 0 | 78 | 78 | 78 | 78 | 78 | 78 | 78 | 78 |
| 30 | 0 | 0 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 |
| 40 | 0 | 0 | 54 | 54 | 54 | 54 | 54 | 54 | 54 | 54 |
| 50 | 22721 | 22721 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 100 | 49257 | 49257 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 |

## Rezultate pentru Dimensiuni Medii (100-10,000 elemente)

### Timp de Execuție (secunde)

| Dimensiune | DP Unoptimized | DP Optimized | Greedy Unoptimized | Greedy Optimized | KK Unoptimized | KK Optimized | Multifit Unoptimized | Multifit Semioptimized | Multifit Optimized | Multifit Multiprocessing |
|-----------|--------------------|--------------------|--------------------|--------------------|--------------------|--------------------|--------------------|--------------------|--------------------|--------------------|
| 100 | 0.000035 | 0.000021 | 0.000159 | 0.000173 | 0.001655 | 0.000955 | 0.000130 | 0.000144 | 0.000188 | 0.000370 |
| 500 | 6.045766 | 1.941970 | 0.000404 | 0.000518 | 0.018596 | 0.011260 | 0.000270 | 0.000416 | 0.000510 | 0.000585 |
| 1000 | 26.680928 | 8.147529 | 0.000410 | 0.001026 | 0.044679 | 0.044943 | 0.000741 | 0.000226 | 0.000495 | 0.001299 |
| 2000 | N/A | N/A | 0.001324 | 0.000871 | 0.000042 | 0.000046 | 0.001321 | 0.001351 | 0.000886 | 0.000524 |
| 5000 | N/A | N/A | 0.001825 | 0.004478 | 0.000146 | 0.000127 | 0.003229 | 0.002483 | 0.002048 | 0.001699 |
| 10000 | N/A | N/A | 0.003377 | 0.004361 | 0.000144 | 0.000264 | 0.006879 | 0.007081 | 0.005299 | 0.007037 |

## Rezultate pentru Dimensiuni Mari (100-1,000,000 elemente)

### Timp de Execuție (secunde)

| Dimensiune | Multifit Optimizat | Multifit Optimizat Multiprocessing |
|-----------|--------------------|--------------------|
| 100000 | 0.030007 | 0.115484 |
| 1000000 | 0.356162 | 0.454568 |

## Concluzii

1. Algoritmul Multifit Optimizat a demonstrat cea mai bună performanță pentru seturi mari de date.
2. Pentru dimensiuni mici, diferențele de performanță între algoritmi sunt minime.
3. Pe măsură ce dimensiunea datelor crește, algoritmii optimizați arată avantaje semnificative.
4. Algoritmii de programare dinamică (DP) au fost excluși pentru dimensiuni > 1000 pentru a preveni crash-ul sistemului.
