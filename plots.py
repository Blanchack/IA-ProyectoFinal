import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def plot_paper_replication(fitness_log, filename="fitness_paper_replication.png"):
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(range(len(fitness_log)), fitness_log, color='blue', linewidth=1.4,
            label='Nuestra implementación')
    ax.set_title('Average fitness of 2000 generations with elimination factor',
                 fontsize=13, fontweight='bold')
    ax.set_xlabel('Generation', fontsize=12)
    ax.set_ylabel('Average fitness', fontsize=12)
    ax.set_ylim(0.15, 0.7)
    ax.set_xlim(0, len(fitness_log))
    ax.legend(loc='lower right')
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    print(f"  Gráfica guardada: {filename}")
    plt.close()
