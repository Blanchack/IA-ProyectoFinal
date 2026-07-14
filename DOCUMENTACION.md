# Documentacion del Proyecto: Generador de Laberintos Ms. Pac-Man

## Estructura del proyecto

```
pacman_ga2/
├── __init__.py          # Paquete
├── maze.py              # Clase Maze (representacion del laberinto)
├── fitness.py           # Funciones de fitness (base + mejoradas)
├── genetic.py           # AG base (Safak et al. 2016)
├── genetic_improved.py  # AG mejorado con FI2POP (Zafar et al. 2020)
├── main.py              # Menu principal (opciones 1-4)
├── plots.py             # Graficos de convergencia
├── visualizer.py        # Visualizacion con Pygame
└── DOCUMENTACION.md     # Este archivo
```

---

## 1. `maze.py` — Representacion del laberinto

| Elemento | Descripcion |
|---|---|
| `Maze.SIZE = 22` | Matriz de 22x22 = 484 celdas |
| `_enforce_borders()` | Las 4 orillas siempre son pared (84 bordes) |
| `to_chromosome()` | Convierte la grilla a lista plana de 0/1 (cromosoma) |
| `from_chromosome()` | Reconstruye el Maze desde un cromosoma |

---

## 2. `fitness.py` — Funciones de evaluacion

### Funciones base compartidas

| Funcion | Que mide | Rango |
|---|---|---|
| `bfs_reachability(grid)` | % de celdas libres alcanzables via BFS | [0, 1] |
| `is_finishable(grid)` | 1.0 si reachability >= 0.95, 0.0 si no | {0, 1} |
| `intersected_block_ratio(grid)` | Proporcion de paredes con al menos 1 vecino pared | [0, 1] |
| `horizontal_vertical_ratio(grid)` | Ratio paredes horizontales / verticales | [0, ∞) |
| `block_size_ratio(grid)` | (interior_walls - 48) / 48 (target 48) | [-1, ~7] |
| `homogeneity_factor(grid)` | Uniformidad de paredes entre 4 cuadrantes | [0, 1] |

### Funciones nuevas (Zafar 2020)

| Funcion | Que mide | Rango | Papel |
|---|---|---|---|
| `reachability_ratio(grid)` | rB/tNB continuo (sin umbral) | [0, 1] | Dificultad |
| `room_structure_ratio(grid)` | Paredes en esquina (2 vecinos en direcciones perpendiculares) / total paredes | [0, 1] | Estetica |
| `density_target_ratio(grid)` | `max(0, 1 - |density - 0.3|*2)` penaliza alejarse de 0.3 | [0, 1] | Estetica |
| `symmetry_ratio(grid)` | `max(0, 1 - |n_UL - n_UR + n_LL - n_LR| / total_cells)` | [0, 1] | Estetica |
| `balance_ratio(grid)` | `max(0, 1 - |O_TR - O_BR| / total_cells)` | [0, 1] | Estetica |
| `isolated_elements_ratio(grid)` | Dispersion de paredes (distancia promedio al centroide) | [0, 1] | Dificultad |
| `dead_end_ratio(grid)` | `1 - callejones / celdas_libres` (menos dead ends = mejor) | [0, 1] | Dificultad |

### `fitness_base(individual)` — Safak 2016

```
fit = 0.4 * finish - 0.1 * ibr + 0.2 * hf + 0.2 * hvr + 0.2 * bsr
```

Pesos: `finish` domina; `hvr` y `bsr` recompensan proporcion H/V y cercania a 48 paredes.

### `fitness_improved(individual)` — Zafar 2020 extendido

```
fit = 0.25 * reach - 0.10 * ibr + 0.10 * hvr + 0.20 * rs + 0.15 * dr + 0.15 * sr + 0.10 * br + 0.10 * ie + 0.30 * de
```

| Termino | Peso | Efecto |
|---|---|---|
| `reach` | +0.25 | Maximizar celdas alcanzables |
| `ibr` | -0.10 | Penalizar paredes agrupadas |
| `hvr` | +0.10 | Proporcion H/V cercana a 1 |
| `rs` | +0.20 | Favorecer esquinas (rooms) |
| `dr` | +0.15 | Densidad cercana a 0.3 |
| `sr` | +0.15 | Simetria espejada 4 cuadrantes |
| `br` | +0.10 | Balance arriba/abajo |
| `ie` | +0.10 | Paredes dispersas |
| `de` | +0.30 | Pocos callejones sin salida |

Ademas, almacena `individual.dead_end_pct` (porcentaje crudo de dead ends) para que FI2POP lo use como criterio de division.

---

## 3. `genetic.py` — AG base (Safak 2016)

### Parametros

| Parametro | Valor |
|---|---|
| `POPULATION_SIZE` | 100 |
| `N_GENERATIONS` | 1000 |
| `CROSSOVER_PROB` | 0.7 |
| `MUTATION_PROB` | 0.05 |
| `CHROMOSOME_LENGTH` | 22x22 = 484 |
| `MAX_INTERIOR_WALLS` | 48 |

### Algoritmo

```
1. Inicializar poblacion aleatoria de 100 individuos
2. Aplicar _fix_individual a cada uno:
   a. enforce_borders: bordes = 1
   b. _enforce_exact_interior_walls: exactamente 48 paredes interiores
3. Evaluar con fitness_base
4. Por cada generacion (1000):
   a. varAnd: crossover 3-puntos + mutacion flip-bit
   b. Reparar individuos (bordes + 48 paredes)
   c. Evaluar
   d. Seleccion por ruleta (selRoulette)
   e. Elitismo: reemplazar peor por mejor global
   f. Logging cada 200 gens
5. Retornar fitness_log y best_per_gen
```

### Operadores geneticos

- **Cruce**: 3-puntos (`cx_three_point`) — intercambia segmentos 1/4 y 3/4 del cromosoma
- **Mutacion**: `mutFlipBit` con prob 0.05 por gen
- **Seleccion**: `selRoulette` (ruleta, probabilidad proporcional al fitness)
- **Elitismo**: opcional, preserva el mejor individuo de todas las generaciones

### Restriccion dura

`_enforce_exact_interior_walls` fuerza **exactamente 48 paredes interiores** (excluyendo bordes). Si hay mas, elimina al azar; si hay menos, agrega al azar. Esto garantiza que `interior_walls = 48` para todos los individuos.

---

## 4. `genetic_improved.py` — AG mejorado con FI2POP (Zafar 2020)

### Parametros

| Parametro | Valor |
|---|---|
| `POPULATION_SIZE` | 100 |
| `N_GENERATIONS` | 1000 |
| `CROSSOVER_PROB` | 0.7 |
| `MUTATION_PROB` | 0.05 |
| `CHROMOSOME_LENGTH` | 22x22 = 484 |
| `DEAD_END_THRESHOLD` | 0.3 |

### Algoritmo FI2POP (Feasible-Infeasible Two Population)

```
1. Inicializar poblacion aleatoria de 100 individuos
2. Aplicar _fix_individual (SOLO bordes, SIN restriccion de 48)
3. Evaluar con fitness_improved
4. Dividir en 2 poblaciones por dead_end_pct:
   - LO (low dead ends): dead_end_pct < 0.3
   - HI (high dead ends): dead_end_pct >= 0.3
5. Mejor global = mejor de LO (o de HI si LO esta vacio)
6. Por cada generacion:
   a. Evolucionar LO: seleccion por ruleta (fitness_improved) -> varAnd
   b. Evolucionar HI: seleccion ponderada por 1-dead_end_pct -> varAnd
   c. Mergear todo y re-dividir por dead_end_pct
   d. Balancear: mantener ~50% en cada poblacion
   e. Si LO vacio, promover mejores HI
   f. Si HI vacio, degradar peores LO
   g. Elitismo: clonar mejor global en LO
   h. Actualizar mejor global
   i. Logging cada 200 gens con LO:N HI:M
7. Retornar fitness_log y best_per_gen
```

### Diferencias clave con `genetic.py`

| Aspecto | `genetic.py` (Base) | `genetic_improved.py` (FI2POP) |
|---|---|---|
| **Fitness** | `fitness_base` (5 terminos) | `fitness_improved` (9 terminos) |
| **Poblacion** | Unica (100 individuos) | Dos: LO y HI (~50 cada una) |
| **Paredes interiores** | **Forzadas a 48** | **Sin restriccion** |
| **Criterio de seleccion** | Solo fitness | LO: fitness; HI: 1-dead_end_pct |
| **Cruce/Mutacion** | Una poblacion | Ambas poblaciones por separado |
| **Migracion** | No | Individuos pasan de LO a HI y viceversa segun dead_end_pct |
| **Elitismo** | Reemplaza peor de la unica poblacion | Reemplaza peor de LO |
| **Log** | `[Base] Avg: X Best: Y` | `[FI2POP] Avg: X Best: Y LO:N HI:M` |

### Por que remover la restriccion de 48 paredes?

En la version mejorada no hay `_enforce_exact_interior_walls`. Esto permite que:

- `density_target_ratio` sea significativa (si todos tuvieran 48, la densidad siempre seria 48/484 ≈ 0.1, lejos del target 0.3)
- `room_structure_ratio` y `isolated_elements_ratio` tengan variabilidad real
- El AG explore libremente diferentes densidades

### Criterio de division FI2POP

Las poblaciones se dividen segun `dead_end_pct` (proporcion de celdas libres que son callejon sin salida):

- **LO** (`dead_end_pct < 0.3`): soluciones con pocos callejones. Evolucionan normalmente con `fitness_improved`.
- **HI** (`dead_end_pct >= 0.3`): soluciones con muchos callejones. Evolucionan con presion hacia MENOS dead ends (seleccion por `1 - dead_end_pct`).

Cuando un individuo cruza el umbral (pasa de HI a LO o viceversa), migra automaticamente entre poblaciones.

---

## 5. `main.py` — Menu de ejecucion

| Opcion | Funcion | Elitismo | Paredes |
|---|---|---|---|
| 1 | `run_base` | Si | Forzadas a 48 |
| 2 | `run_base` | No | Forzadas a 48 |
| 3 | `run_improved` (FI2POP) | Si | Sin restriccion |
| 4 | `run_improved` (FI2POP) | No | Sin restriccion |

Todas las opciones usan `N_GENERATIONS = 1000` y `pop_size = 100`.

### Como ejecutar

```bash
cd pacman_ga2
python3 main.py
```

O desde el directorio padre:

```bash
cd /ruta/a/IA-final
python -m pacman_ga2.main
```

---

## 6. Resumen de metricas por version

| Fuente | Metricas usadas |
|---|---|
| **Safak 2016** (base) | finish (umbral 95%), ibr, hf, hvr, bsr |
| **Zafar 2020** (mejorado) | reach (continuo), ibr, hvr, rs, dr, sr, br, ie, de |
| **Ambos papers** | ibr, hvr (compartidas pero con distinto peso) |

Las metricas nuevas (`room_structure_ratio`, `density_target_ratio`, `symmetry_ratio`, `balance_ratio`, `isolated_elements_ratio`, `dead_end_ratio`) y el algoritmo FI2POP estan inspirados en Zafar et al. 2020, adaptados al dominio de Pac-Man.
