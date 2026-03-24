import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

def linear_fit_analysis(x=None, y=None, y_err=None, plot=True,title="Linear_fit",xlab="V",ylab="I"):
    x = np.array(x)
    y = np.array(y)
    n = len(x)

    # -----------------------------
    # Linear regression
    # -----------------------------
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)

    y_fit = slope * x + intercept
    residuals = y - y_fit

    # -----------------------------
    # Uncertainties
    # -----------------------------
    sigma2 = np.sum(residuals**2) / (n - 2)
    x_mean = np.mean(x)

    slope_err = std_err
    intercept_err = np.sqrt(
        sigma2 * (1/n + x_mean**2 / np.sum((x - x_mean)**2))
    )

    # -----------------------------
    # Plot
    # -----------------------------
    if plot:
        plt.errorbar(x, y, yerr=y_err, fmt='o', label='Data')

        x_line = np.linspace(min(x), max(x), 100)
        y_line = slope * x_line + intercept

        # Legend with uncertainties
        label = (
            f"Fit: y = ({slope:.3f} ± {slope_err:.3f})x + ({intercept:.3f} ± {intercept_err:.3f})\n"
            f"R = {r_value:.4f}, R² = {r_value**2:.4f}"
        )

        plt.plot(x_line, y_line, label=label)

        plt.xlabel(xlab)
        plt.ylabel(ylab)
        plt.title(title)
        plt.legend()
        plt.grid()
        plt.savefig(f"{title}.pdf")
        plt.show()
        plt.close

    return {
        "slope": slope,
        "intercept": intercept,
        "slope_err": slope_err,
        "intercept_err": intercept_err,
        "R": r_value,
        "R_squared": r_value**2
    }
