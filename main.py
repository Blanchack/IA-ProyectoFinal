import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pacman_ga2.genetic import run_base
from pacman_ga2.genetic_improved import run_improved
from pacman_ga2.plots import plot_paper_replication
from pacman_ga2.visualizer import visualize_maze, save_maze_image


def main():
    print("=== Generador de Laberintos Ms. Pac-Man ===")
    print("1. AG base con elitismo (Fig. 6 — Safak 2016)")
    print("2. AG base sin elitismo (Fig. 4 — Safak 2016)")
    print("3. AG mejorado con elitismo — Zafar et al. 2020")
    print("4. AG mejorado sin elitismo — Zafar et al. 2020")
    opcion = input("Selecciona una opción: ")

    N_GENERATIONS = 1000

    if opcion == "1":
        fitness_log, best_per_gen = run_base(
            n_generations=N_GENERATIONS, pop_size=100, verbose=True, elitism=True
        )
        plot_paper_replication(fitness_log, "fitness_paper_replication.png")
        save_maze_image(best_per_gen[0], "paper_repl_gen1.png", "Gen 1")
        save_maze_image(best_per_gen[-1], "paper_repl_gen_final.png", "Gen final")
        visualize_maze(best_per_gen[-1], "Mejor laberinto — Safak 2016")

    elif opcion == "2":
        fitness_log, best_per_gen = run_base(
            n_generations=N_GENERATIONS, pop_size=100, verbose=True, elitism=False
        )
        plot_paper_replication(fitness_log, "fitness_paper_no_elitism.png")
        save_maze_image(best_per_gen[0], "paper_no_elitism_gen1.png", "Gen 1")
        save_maze_image(best_per_gen[-1], "paper_no_elitism_gen_final.png", "Gen final")
        visualize_maze(best_per_gen[-1], "Mejor laberinto — Sin elitismo")

    elif opcion == "3":
        fitness_log, best_per_gen = run_improved(
            n_generations=N_GENERATIONS, pop_size=100, verbose=True, elitism=True
        )
        plot_paper_replication(fitness_log, "fitness_improved.png")
        save_maze_image(best_per_gen[0], "improved_gen1.png", "Gen 1")
        save_maze_image(best_per_gen[-1], "improved_gen_final.png", "Gen final")
        visualize_maze(best_per_gen[-1], "Mejor laberinto — Zafar 2020 (con elitismo)")

    elif opcion == "4":
        fitness_log, best_per_gen = run_improved(
            n_generations=N_GENERATIONS, pop_size=100, verbose=True, elitism=False
        )
        plot_paper_replication(fitness_log, "fitness_improved_no_elitism.png")
        save_maze_image(best_per_gen[0], "improved_no_elitism_gen1.png", "Gen 1")
        save_maze_image(best_per_gen[-1], "improved_no_elitism_gen_final.png", "Gen final")
        visualize_maze(best_per_gen[-1], "Mejor laberinto — Zafar 2020 (sin elitismo)")

    else:
        print("Opción no válida.")


if __name__ == "__main__":
    main()
