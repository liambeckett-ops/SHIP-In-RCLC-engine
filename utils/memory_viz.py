# utils/memory_viz.py

import matplotlib.pyplot as plt

def plot_drift(logs, tag_key="drift_tag"):
    drift_points = [(i, entry[tag_key])
                    for i, entry in enumerate(logs) if tag_key in entry]
    if not drift_points:
        print("No drift tags found.")
        return

    indices, tags = zip(*drift_points)
    plt.plot(indices, tags, marker='o', linestyle='-', label="Memory Drift")
    plt.title("Cognitive Drift Pattern")
    plt.xlabel("Log Index")
    plt.ylabel("Tag Value")
    plt.legend()
    plt.tight_layout()
    plt.show()
