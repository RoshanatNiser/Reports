import json
import numpy as np
import matplotlib.pyplot as plt
import os

# -----------------------------
# SET OUTPUT DIRECTORY
# -----------------------------
OUTPUT_DIR = "GM_2_output"

def ensure_dir():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

def save_txt(text, filename):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)


# -----------------------------
# LOAD DATA
# -----------------------------
with open("GM_2.json", "r") as f:
    data = json.load(f)


# -----------------------------
# EXP 5
# -----------------------------
def analyze_exp5(exp):

    rho = exp["density_al"]
    results = {}
    report = "\n===== EXPERIMENT 5 =====\n"

    for source_name, source in exp["sources"].items():

        bg = source["background_counts"]
        T = source["count_time"]

        thickness_gcm2 = []
        cps = []

        for d in source["data"]:
            t = d["thickness_mm"]
            c = d["counts"]

            net = c - bg
            cps_val = net / T
            t_gcm2 = rho * (t / 10)

            thickness_gcm2.append(t_gcm2)
            cps.append(cps_val)

        thickness_gcm2 = np.array(thickness_gcm2)
        cps = np.array(cps)

        half_max = max(cps) / 2
        idx = np.argmin(np.abs(cps - half_max))
        range_est = thickness_gcm2[idx]
        energy = (range_est + 0.09) / 0.52

        report += f"\n{source_name}:\n"
        report += f"Range = {range_est:.4f} g/cm²\n"
        report += f"Energy = {energy:.4f} MeV\n"

        results[source_name] = {
            "range": float(range_est),
            "energy": float(energy)
        }

        # Plot
        plt.figure()
        plt.plot(thickness_gcm2, cps, 'o-')
        plt.axhline(half_max, linestyle='--')
        plt.xlabel("Thickness (g/cm²)")
        plt.ylabel("CPS")
        plt.title(f"Beta Absorption - {source_name}")
        plt.grid()
        plt.savefig(f"{OUTPUT_DIR}/exp5_{source_name}.png")
        plt.close()

    return results, report


# -----------------------------
# EXP 6
# -----------------------------
def analyze_exp6(exp):

    report = "\n===== EXPERIMENT 6 =====\n"

    thickness = []
    avg_counts = []

    for d in exp["data"]:
        t = d["thickness_mm"]
        avg = (d["counts1"] + d["counts2"]) / 2

        thickness.append(t)
        avg_counts.append(avg)

    thickness = np.array(thickness)
    avg_counts = np.array(avg_counts)

    gradients = np.gradient(avg_counts)
    idx = np.argmin(np.abs(gradients))
    saturation = thickness[idx]

    report += f"Saturation thickness = {saturation:.4f} mm\n"

    plt.figure()
    plt.plot(thickness, avg_counts, 'o-')
    plt.xlabel("Thickness (mm)")
    plt.ylabel("Counts")
    plt.title("Backscattering")
    plt.grid()
    plt.savefig(f"{OUTPUT_DIR}/exp6_backscatter.png")
    plt.close()

    return {
        "saturation": float(saturation)
    }, report


# -----------------------------
# EXP 7
# -----------------------------
def analyze_exp7(exp):

    bg = exp["background_counts"]
    T = exp["count_time"]

    report = "\n===== EXPERIMENT 7 =====\n"

    labels = []
    mean_net = []
    std_dev = []

    results = {}

    for name, config in exp["configurations"].items():

        counts = np.array(config["counts"])

        mean_counts = np.mean(counts)
        std_counts = np.std(counts, ddof=1)

        net = mean_counts - bg
        cps = net / T

        report += f"\n{name}:\n"
        report += f"Mean = {mean_counts:.2f}\n"
        report += f"Std = {std_counts:.2f}\n"
        report += f"Net = {net:.2f}\n"
        report += f"CPS = {cps:.4f}\n"

        labels.append(name)
        mean_net.append(net)
        std_dev.append(std_counts)

        results[name] = {
            "mean": float(mean_counts),
            "std": float(std_counts),
            "net": float(net),
            "cps": float(cps)
        }

    # Relative comparison
    max_val = max(mean_net)
    report += "\nRelative Intensities:\n"

    for l, v in zip(labels, mean_net):
        rel = v / max_val
        report += f"{l}: {rel:.3f}\n"

    # Plot
    plt.figure()
    plt.errorbar(labels, mean_net, yerr=std_dev, fmt='o', capsize=5)
    plt.ylabel("Net Counts")
    plt.title("Bremsstrahlung Comparison")
    plt.grid()
    plt.savefig(f"{OUTPUT_DIR}/exp7_bremsstrahlung.png")
    plt.close()

    return results, report


# -----------------------------
# MAIN
# -----------------------------
def main():

    ensure_dir()

    final_report = ""

    res5, rep5 = analyze_exp5(data["exp5_beta_absorption"])
    res6, rep6 = analyze_exp6(data["exp6_backscattering"])
    res7, rep7 = analyze_exp7(data["exp7_bremsstrahlung"])

    final_report += rep5 + rep6 + rep7

    # Save JSON
    with open(f"{OUTPUT_DIR}/results.json", "w") as f:
        json.dump({
            "exp5": res5,
            "exp6": res6,
            "exp7": res7
        }, f, indent=4)

    # Save text report
    save_txt(final_report, f"{OUTPUT_DIR}/report.txt")

    print("\nAll analysis complete. Check GM_2_output folder.")


if __name__ == "__main__":
    main()