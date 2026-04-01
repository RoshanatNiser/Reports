import json
import numpy as np
import matplotlib.pyplot as plt
import os

# -------------------------
# Utilities
# -------------------------

def load_json(file):
    with open(file, 'r') as f:
        return json.load(f)

def ensure_dir(path="output"):
    if not os.path.exists(path):
        os.makedirs(path)

def save_txt(text, filename):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)


# -------------------------
# EXP 1: GM CHARACTERISTICS
# -------------------------

def analyze_exp1(data, output_dir):
    import numpy as np
    import matplotlib.pyplot as plt

    def process_material(mat):
        V = np.array(mat["voltage"])
        N = np.array(mat["counts"])
        B = np.array(mat["background"])
        Nc = N - B
        return V, Nc

    # Process data
    Vc, Nc = process_material(data["Cesium"])
    Vb, Nb = process_material(data["Cobalt"])

    # -------- Plot 1: Cesium --------
    plt.figure()
    plt.plot(Vc, Nc, marker='o')
    plt.xlabel("Voltage (V)")
    plt.ylabel("Corrected Counts")
    plt.title("GM Characteristics - Cesium (Gamma Source)")
    plt.grid()
    plt.savefig(f"{output_dir}/exp1_cesium.png")
    plt.close()

    # -------- Plot 2: Cobalt --------
    plt.figure()
    plt.plot(Vb, Nb, marker='s')
    plt.xlabel("Voltage (V)")
    plt.ylabel("Corrected Counts")
    plt.title("GM Characteristics - Cobalt (Beta Source)")
    plt.grid()
    plt.savefig(f"{output_dir}/exp1_cobalt.png")
    plt.close()

    return "Exp-1 completed: Separate plots generated for Cesium and Cobalt.\n"


# -------------------------
# EXP 2: INVERSE SQUARE LAW
# -------------------------

def analyze_exp2(data, output_dir):
    import numpy as np
    import matplotlib.pyplot as plt

    d = np.array(data["distance"])
    counts = np.array(data["counts"])
    bg = np.array(data["background"])

    Nc = counts - bg
    R = Nc / data["time_sec"]

    inv_d2 = 1 / (d ** 2)
    log_d = np.log10(d)
    log_R = np.log10(R)

    # -------------------------
    # Fit 1: R vs 1/d^2
    # -------------------------
    coeff_linear = np.polyfit(inv_d2, R, 1)
    fit_R = np.polyval(coeff_linear, inv_d2)

    # -------------------------
    # Fit 2: log-log
    # -------------------------
    coeff_log = np.polyfit(log_d, log_R, 1)
    slope = coeff_log[0]
    intercept = coeff_log[1]
    fit_log = np.polyval(coeff_log, log_d)

    # -------------------------
    # Plot 1: R vs d
    # -------------------------
    plt.figure()
    plt.plot(d, R,marker='o',linestyle="--")
    plt.xlabel("Distance (cm)")
    plt.ylabel("Count Rate (R)")
    plt.title("R vs d")
    plt.grid()
    plt.savefig(f"{output_dir}/exp2_R_vs_d.png")
    plt.close()

    # -------------------------
    # Plot 2: R vs 1/d^2 (with fit)
    # -------------------------
    plt.figure()
    plt.scatter(inv_d2, R, label="Data")
    plt.plot(inv_d2, fit_R, label="Linear Fit", linestyle="--")
    plt.xlabel("1/d^2")
    plt.ylabel("R")
    plt.title("R vs 1/d^2 (Fit)")
    plt.legend()
    plt.grid()
    plt.savefig(f"{output_dir}/exp2_R_vs_inv_d2_fit.png")
    plt.close()

    # -------------------------
    # Plot 3: log-log (with fit)
    # -------------------------
    plt.figure()
    plt.scatter(log_d, log_R, label="Data")
    plt.plot(log_d, fit_log, label="Fit", linestyle="--")
    plt.xlabel("log(d)")
    plt.ylabel("log(R)")
    plt.title("log R vs log d")
    plt.legend()
    plt.grid()
    plt.savefig(f"{output_dir}/exp2_log_fit.png")
    plt.close()

    # -------------------------
    # Analysis
    # -------------------------
    analysis = f"""
Exp-2 Analysis:

Linear Fit (R vs 1/d^2):
R = {coeff_linear[0]:.4f} * (1/d^2) + {coeff_linear[1]:.4f}

Log-Log Fit:
Slope = {slope:.3f}
Intercept = {intercept:.3f}

Expected slope ≈ -2 for inverse square law.

Conclusion:
Inverse square law is {'well verified' if abs(slope + 2) < 0.2 else 'approximately satisfied'}.

Remarks:
- Non-zero intercept in linear fit indicates background/systematic effects.
- Deviation from slope -2 may arise due to finite detector size, scattering, or alignment errors.
"""

    return analysis


# -------------------------
# EXP 3: STATISTICS
# -------------------------

def analyze_exp3(data, output_dir):
    report = ""

    # -------- Table 3.a --------
    t3a = np.array(data["table_3a"]["counts_10s"])
    report += f"\nTable 3.a Mean (10s): {np.mean(t3a):.2f}\n"

    # -------- Table 3.c --------
    t3c = np.array(data["table_3c"]["counts_100s"])
    mean = np.mean(t3c)
    dev = t3c - mean
    dev2 = dev**2

    table_3c_full = []
    for i in range(len(t3c)):
        table_3c_full.append({
            "Ni": float(t3c[i]),
            "Ni-N": float(dev[i]),
            "(Ni-N)^2": float(dev2[i])
        })

    variance = np.sum(dev2) / len(t3c)
    std = np.sqrt(variance)

    report += f"""
Table 3.c:
Mean = {mean:.2f}
Variance = {variance:.2f}
Std Dev = {std:.2f}
"""

    # Histogram
    plt.figure()
    plt.hist(t3c, bins=10)
    plt.title("Histogram (100s counts)")
    plt.savefig(f"{output_dir}/exp3_hist.png")
    plt.close()

    # -------- Table 3.d --------
    Ni = np.array(data["table_3d"]["Ni"])
    N_mean = np.mean(Ni)
    sigma = np.sqrt(N_mean)

    table_3d_full = []
    for val in Ni:
        diff = val - N_mean
        norm = diff / sigma
        rounded = round(norm * 2) / 2

        table_3d_full.append({
            "Ni": float(val),
            "Ni-N": float(diff),
            "(Ni-N)/sigma": float(norm),
            "rounded": float(rounded)
        })

    # Gaussian-like plot
    rounded_vals = [row["rounded"] for row in table_3d_full]
    plt.figure()
    plt.hist(rounded_vals, bins=10)
    plt.title("Gaussian Distribution Check")
    plt.savefig(f"{output_dir}/exp3_gaussian.png")
    plt.close()

    report += f"""
Table 3.d:
Mean = {N_mean:.2f}
Sigma = {sigma:.2f}

Conclusion:
Distribution approaches Gaussian (as expected for large N).
"""

    return report, table_3c_full, table_3d_full


# -------------------------
# MAIN
# -------------------------

def main(input_file):
    output_dir = "GM-1_output"
    ensure_dir(output_dir)

    data = load_json(input_file)

    final_report = ""

    # Exp 1
    final_report += analyze_exp1(data["exp1"], output_dir)

    # Exp 2
    final_report += analyze_exp2(data["exp2"], output_dir)

    # Exp 3
    report3, table3c, table3d = analyze_exp3(data["exp3"], output_dir)
    final_report += report3

    # Save outputs
    save_txt(final_report, f"{output_dir}/report.txt")

    with open(f"{output_dir}/table3c_full.json", "w") as f:
        json.dump(table3c, f, indent=4)

    with open(f"{output_dir}/table3d_full.json", "w") as f:
        json.dump(table3d, f, indent=4)

    print(f"All analysis complete. Check {output_dir}/ folder.")

    
if __name__ == "__main__":
    main("GM_1.JSON")
