import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from scipy.optimize import minimize


# 1. Load and clean dengue dataset
df = pd.read_excel('data/dengue_summary.xlsx')
df['Date'] = pd.to_datetime(df['Date'], format='%d-%b-%Y')
df = df.sort_values('Date').reset_index(drop=True)

# Handle missing dates using linear interpolation
full_date_range = pd.date_range(
    start=df['Date'].min(), end=df['Date'].max(), freq='D')
df_cleaned = df.set_index('Date').reindex(
    full_date_range).interpolate(method='linear')

daily_cases = df_cleaned['Weekly Case'].values
days = len(daily_cases)
t = np.arange(days)

# 2. RK4 Numerical Solver for SIR Model


def rk4_sir_simulation(N, beta, gamma, I0, days):
    dt = 1.0  # 1-day time step
    S = np.zeros(days)
    I = np.zeros(days)
    R = np.zeros(days)
    new_cases = np.zeros(days)

    S[0] = N - I0
    I[0] = I0
    R[0] = 0
    new_cases[0] = beta * S[0] * I[0] / N

    for i in range(days - 1):
        s, idx, r = S[i], I[i], R[i]

        # Derivatives function
        def derivatives(s_val, i_val):
            ds = -beta * s_val * i_val / N
            di = beta * s_val * i_val / N - gamma * i_val
            return ds, di

        # RK4 Slopes (k1, k2, k3, k4)
        k1_s, k1_i = derivatives(s, idx)
        k2_s, k2_i = derivatives(s + 0.5*dt*k1_s, idx + 0.5*dt*k1_i)
        k3_s, k3_i = derivatives(s + 0.5*dt*k2_s, idx + 0.5*dt*k2_i)
        k4_s, k4_i = derivatives(s + dt*k3_s, idx + dt*k3_i)

        # Update values using weighted average of slopes
        S[i+1] = s + (dt/6.0)*(k1_s + 2*k2_s + 2*k3_s + k4_s)
        I[i+1] = idx + (dt/6.0)*(k1_i + 2*k2_i + 2*k3_i + k4_i)
        R[i+1] = N - S[i+1] - I[i+1]

        new_cases[i+1] = beta * S[i+1] * I[i+1] / N

    return S, I, R, new_cases

# 3. Optimize parameters (Beta, Gamma) to match actual data


def loss_function(params):
    beta, gamma, N_eff, I0 = params
    if beta <= 0 or gamma <= 0 or N_eff <= 100 or I0 <= 0:
        return 1e10
    _, _, _, pred_cases = rk4_sir_simulation(N_eff, beta, gamma, I0, days)
    return np.mean((pred_cases - daily_cases)**2)


# Initial parameter guesses
initial_guess = [0.25, 0.10, 50000, 30]
bounds = [(0.01, 2.0), (0.01, 1.0), (5000, 500000), (1, 500)]

res = minimize(loss_function, initial_guess, bounds=bounds, method='L-BFGS-B')
beta_opt, gamma_opt, N_opt, I0_opt = res.x
R0_val = beta_opt / gamma_opt

# Run final simulation with optimized parameters
S_sim, I_sim, R_sim, daily_sim = rk4_sir_simulation(
    N_opt, beta_opt, gamma_opt, I0_opt, days)

# 4. Visualization
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Plot 1: Daily Cases vs SIR Fitting
ax1.plot(df_cleaned.index, daily_cases, 'o-', color='blue',
         alpha=0.7, label='Actual Daily Cases', markersize=4)
ax1.plot(df_cleaned.index, daily_sim, 'r--', linewidth=2.5,
         label=f'SIR (RK4 Fit: R0={R0_val:.2f})')
ax1.set_title('Daily Dengue Infections: Actual vs SIR Model (RK4)',
              fontsize=12, fontweight='bold')
ax1.set_xlabel('Date')
ax1.set_ylabel('New Cases')
ax1.grid(True, linestyle='--', alpha=0.5)
ax1.legend()

# Plot 2: Susceptible, Infectious, Recovered Dynamics
ax2.plot(df_cleaned.index, S_sim, color='green',
         linewidth=2, label='Susceptible (S)')
ax2.plot(df_cleaned.index, I_sim, color='red',
         linewidth=2, label='Infectious (I)')
ax2.plot(df_cleaned.index, R_sim, color='purple',
         linewidth=2, label='Recovered (R)')
ax2.set_title('SIR Model Dynamics over Time (RK4 Simulation)',
              fontsize=12, fontweight='bold')
ax2.set_xlabel('Date')
ax2.set_ylabel('Population')
ax2.grid(True, linestyle='-', alpha=0.5)
ax2.legend()

for ax in ax1, ax2:
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d %b'))
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.setp(ax.get_xticklabels(), rotation=30, ha='left')


plt.tight_layout()
plt.savefig('images/dengue_sir_rk4_analysis.png', dpi=300)
plt.show()

print(f"Calculated R0 (Reproduction Number): {R0_val:.2f}")
