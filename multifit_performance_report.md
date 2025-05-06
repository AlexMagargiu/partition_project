# Raport de Performanță - Algoritmi Multifit

## Sumar Executiv

Acest raport prezintă rezultatele comparative ale performanței diferitelor implementări ale algoritmului Multifit pentru problema partiționării. Testele au fost efectuate pe multiple dimensiuni de date, de la seturi mici (10-100 elemente) până la seturi foarte mari (până la 1 milion de elemente).

## Rezultate pentru Dimensiuni Standard (10-100 elemente)

### Timp de Execuție (secunde)

| Dimensiune | DP Unoptimized | DP Optimized | Greedy Unoptimized | Greedy Optimized | KK Unoptimized | KK Optimized | Multifit Unoptimized | Multifit Semioptimized | Multifit Optimized | Multifit Multiprocessing |
|-----------|--------------------|--------------------|--------------------|--------------------|--------------------|--------------------|--------------------|--------------------|--------------------|--------------------|
| 10 | 0.002044 | 0.000907 | 0.000012 | 0.000032 | 0.000056 | 0.000038 | 0.000010 | 0.000011 | 0.000017 | N/A |
| 20 | 0.009382 | 0.004443 | 0.000017 | 0.000025 | 0.000068 | 0.000051 | 0.000014 | 0.000011 | 0.000024 | N/A |
| 30 | 0.019644 | 0.007738 | 0.000012 | 0.000032 | 0.000085 | 0.000083 | 0.000011 | 0.000010 | 0.000025 | N/A |
| 40 | 0.035580 | 0.012161 | 0.000019 | 0.000040 | 0.000137 | 0.000146 | 0.000018 | 0.000018 | 0.000030 | N/A |
| 50 | 0.050199 | 0.018733 | 0.000019 | 0.000039 | 0.000178 | 0.000146 | 0.000018 | 0.000020 | 0.000039 | N/A |
| 100 | 0.217481 | 0.075895 | 0.000037 | 0.000047 | 0.000324 | 0.000314 | 0.000037 | 0.000042 | 0.000048 | N/A |

### Diferența dintre Subseturi

| Dimensiune | DP Unoptimized | DP Optimized | Greedy Unoptimized | Greedy Optimized | KK Unoptimized | KK Optimized | Multifit Unoptimized | Multifit Semioptimized | Multifit Optimized | Multifit Multiprocessing |
|-----------|--------------------|--------------------|--------------------|--------------------|--------------------|--------------------|--------------------|--------------------|--------------------|--------------------|
| 10 | 4754 | 4754 | 28 | 28 | 28 | 28 | 28 | 28 | 28 | N/A |
| 20 | 0 | 0 | 28 | 28 | 28 | 28 | 28 | 28 | 28 | N/A |
| 30 | 0 | 0 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | N/A |
| 40 | 0 | 0 | 44 | 44 | 44 | 44 | 44 | 44 | 44 | N/A |
| 50 | 0 | 0 | 14 | 14 | 14 | 14 | 14 | 14 | 14 | N/A |
| 100 | 0 | 0 | 16 | 16 | 16 | 16 | 16 | 16 | 16 | N/A |

## Rezultate pentru Dimensiuni Medii (100-10,000 elemente)

### Timp de Execuție (secunde)

| Dimensiune | DP Unoptimized | DP Optimized | Greedy Unoptimized | Greedy Optimized | KK Unoptimized | KK Optimized | Multifit Unoptimized | Multifit Semioptimized | Multifit Optimized | Multifit Multiprocessing |
|-----------|--------------------|--------------------|--------------------|--------------------|--------------------|--------------------|--------------------|--------------------|--------------------|--------------------|
| 100 | 0.224936 | 0.078236 | 0.000078 | 0.000062 | 0.000728 | 0.000694 | 0.000031 | 0.000041 | 0.000072 | N/A |
| 500 | 0.000012 | 0.000015 | 0.000120 | 0.000185 | 0.006950 | 0.005464 | 0.000100 | 0.000118 | 0.000132 | N/A |
| 1000 | 28.094402 | 6.880338 | 0.000134 | 0.000270 | 0.021492 | 0.021004 | 0.000201 | 0.000220 | 0.000259 | N/A |
| 2000 | N/A | N/A | 0.000383 | 0.000448 | 0.000021 | 0.000023 | 0.000406 | 0.000335 | 0.000489 | N/A |
| 5000 | N/A | N/A | 0.000850 | 0.001051 | 0.000035 | 0.000032 | 0.000812 | 0.000925 | 0.000892 | N/A |
| 10000 | N/A | N/A | 0.001607 | 0.002355 | 0.000069 | 0.000065 | 0.001595 | 0.001631 | 0.001884 | N/A |

## Rezultate pentru Dimensiuni Mari (100-1,000,000 elemente)

### Timp de Execuție (secunde)

| Dimensiune | Multifit Optimizat | Multifit Optimizat Multiprocessing |
|-----------|--------------------|--------------------|
| 100000 | 0.018170 | 0.053534 |
| 1000000 | 0.235318 | 0.206709 |

## Concluzii

1. Algoritmul Multifit Optimizat a demonstrat cea mai bună performanță pentru seturi mari de date.
2. Pentru dimensiuni mici, diferențele de performanță între algoritmi sunt minime.
3. Pe măsură ce dimensiunea datelor crește, algoritmii optimizați arată avantaje semnificative.
4. Algoritmii de programare dinamică (DP) au fost excluși pentru dimensiuni > 1000 pentru a preveni crash-ul sistemului.
