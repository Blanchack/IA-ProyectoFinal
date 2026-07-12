import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pacman_ga2.genetic import run_base, N_GENERATIONS
from pacman_ga2.plots import plot_paper_replication
from pacman_ga2.visualizer import visualize_maze, save_maze_image


def main():
    print("=== Generador de Laberintos Ms. Pac-Man (Safak et al. 2016) ===")
    print("1. Ejecutar AG con elitismo (Fig. 6 del paper)")
    print("2. Ejecutar AG sin elitismo (Fig. 4 del paper)")
    opcion = input("Selecciona una opción: ")

    if opcion == "1":
        fitness_log, best_per_gen = run_base(
            n_generations=N_GENERATIONS, pop_size=100, verbose=True, elitism=True
        )
        print(f"\n  Fitness inicial: {fitness_log[0]:.4f}")
        print(f"  Fitness final:   {fitness_log[-1]:.4f}")
        print(f"  Fitness mejor:   {max(fitness_log):.4f}")
        plot_paper_replication(fitness_log, "fitness_paper_replication.png")
        save_maze_image(best_per_gen[0], "paper_repl_gen1.png", "Gen 1")
        save_maze_image(best_per_gen[-1], "paper_repl_gen_final.png", "Gen final")
        visualize_maze(best_per_gen[-1], "Mejor laberinto — Safak 2016")

    elif opcion == "2":
        fitness_log, best_per_gen = run_base(
            n_generations=N_GENERATIONS, pop_size=100, verbose=True, elitism=False
        )
        print(f"\n  Fitness inicial: {fitness_log[0]:.4f}")
        print(f"  Fitness final:   {fitness_log[-1]:.4f}")
        print(f"  Fitness mejor:   {max(fitness_log):.4f}")
        plot_paper_replication(fitness_log, "fitness_paper_no_elitism.png")
        save_maze_image(best_per_gen[0], "paper_no_elitism_gen1.png", "Gen 1")
        save_maze_image(best_per_gen[-1], "paper_no_elitism_gen_final.png", "Gen final")
        visualize_maze(best_per_gen[-1], "Mejor laberinto — Sin elitismo")

    else:
        print("Opción no válida.")


if __name__ == "__main__":
    main()
