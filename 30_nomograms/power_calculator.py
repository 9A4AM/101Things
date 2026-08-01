import numpy as np
import scipy as sc
import matplotlib.pyplot as plt
from matplotlib.ticker import LogLocator, NullFormatter

def to_mW(W):
    return W*1000

def to_dBW(W):
    return 10*np.log10(W)

def to_dBm(W):
    return 10*np.log10(to_mW(W))

def to_S(W):
    return (to_dBm(W)- -127)/6

def to_Vrms(W):
    return np.sqrt(W*50)

def to_Vpkpk(W):
    return 2.0*np.sqrt(2.0)*to_Vrms(W)

# Scale ranges
W_min, W_max = 1e-18, 1e3 # Watts
mW_min, mW_max = to_mW(W_min), to_mW(W_max)
dBm_min, dBm_max = to_dBm(W_min), to_dBm(W_max)
dBW_min, dBW_max = to_dBW(W_min), to_dBW(W_max)
S_min, S_max = to_S(W_min), to_S(W_max)
Vrms_min, Vrms_max = to_Vrms(W_min), to_Vrms(W_max)
Vpkpk_min, Vpkpk_max = to_Vpkpk(W_min), to_Vpkpk(W_max)

def lin_to_y(P, _min, _max):
    p0 = np.log10(_min)
    p1 = np.log10(_max)
    return (np.log10(P) - p0) / (p1 - p0)

def log_to_y(P, _min, _max):
    p0 = _min
    p1 = _max
    return (P - p0) / (p1 - p0)

# ------------------------------------------------------------
# Plot
# ------------------------------------------------------------

fig, ax = plt.subplots(figsize=(8.27, 11.69))  # A4 portrait

ax.set_xlim(-0.1, 1.1)
ax.set_ylim(-0.1, 1.08)
ax.axis("off")

def format_value(value):

    if value >= 1e9:
        return f"{value/1e9:g} G"
    elif value >= 1e6:
        return f"{value/1e6:g} M"
    elif value >= 1e3:
        return f"{value/1e3:g} k"
    elif value >= 1:
        return f"{value:g}"
    elif value >= 1e-3:
        return f"{value*1e3:g} m"
    elif value >= 1e-6:
        return f"{value*1e6:g} µ"
    elif value >= 1e-9:
        return f"{value*1e9:g} n"
    elif value >= 1e-12:
        return f"{value*1e12:g} p"
    elif value >= 1e-15:
        return f"{value*1e15:g} f"
    elif value >= 1e-18:
        return f"{value*1e18:g} a"
    else:
        return f"{value:g}"

def format_number(value):
    return f"{value:g}"

# ------------------------------------------------------------
# Draw scales
# ------------------------------------------------------------

def draw_scale(x, colour, label, right, transform, _min, _max, major_values, minor_values, minor_labels=True, lim=None, _format=format_value):

    if lim is None:
        lim=[_min, _max]

    # Main scale line
    ax.plot(
        [x, x],
        [transform(lim[0], _min, _max), transform(lim[1], _min, _max)],
        linewidth=1.2,
        color=colour
    )

    # Label
    ax.text(
        x,
        1 + 0.035,
        label,
        ha="center",
        va="bottom",
        fontsize=13,
        fontweight="bold",
        color=colour
    )

    for value in major_values:
        y = transform(value, _min, _max)

        # Tick
        ax.plot(
            [x - 0.025 if right else x + 0.025, x],
            [y, y],
            linewidth=0.8,
            color=colour
        )

        # Label
        ax.text(
            x - 0.045 if right else x + 0.045,
            y,
            _format(value),
            ha="right" if right else "left",
            va="center",
            fontsize=8,
            color=colour
        )

    for value in minor_values:
        y = transform(value, _min, _max)

        # Tick
        ax.plot(
            [x - 0.015 if right else x + 0.015, x],
            [y, y],
            linewidth=0.8,
            color=colour
        )

        if minor_labels:

            # Label
            ax.text(
                x - 0.045 if right else x + 0.045,
                y,
                _format(value),
                ha="right" if right else "left",
                va="center",
                fontsize=8,
                color=colour
            )




# ------------------------------------------------------------
# Major ticks
# ------------------------------------------------------------

decades = np.arange(-19, 12)
decades = np.power(10.0*np.ones_like(decades), decades)
minor = np.concatenate([decades*2, decades*3, decades*4, decades*5, decades*6, decades*7, decades*8, decades*9])

W_ticks = [i for i in decades if i <= W_max and i >= W_min]
W_minor_ticks = [i for i in minor if i <= W_max and i >= W_min]
mW_ticks = [i for i in decades if i <= mW_max and i >= mW_min]
mW_minor_ticks = [i for i in minor if i <= mW_max and i >= mW_min]
Vrms_ticks = [i for i in decades if i <= Vrms_max and i >= Vrms_min]
Vrms_minor_ticks = [i for i in minor if i <= Vrms_max and i >= Vrms_min]
Vpkpk_ticks = [i for i in decades if i <= Vpkpk_max and i >= Vpkpk_min]
Vpkpk_minor_ticks = [i for i in minor if i <= Vpkpk_max and i >= Vpkpk_min]

log_decades = np.arange(-180, 120, 10)
log_minor = np.arange(-180, 120)

dBW_ticks = [i for i in log_decades if i <= dBW_max and i >= dBW_min]
dBW_minor_ticks = [i for i in log_minor if i <= dBW_max and i >= dBW_min]
dBm_ticks = [i for i in log_decades if i <= dBm_max and i >= dBm_min]
dBm_minor_ticks = [i for i in log_minor if i <= dBm_max and i >= dBm_min]

s_scale = np.arange(1, 10)
s_scale_minor = np.arange(1, 9, 0.1)
S_ticks = [i for i in s_scale if i <= S_max and i >= S_min]
S_minor_ticks = [i for i in s_scale_minor if i <= S_max and i >= S_min]


#draw grid
for y in W_ticks:
    ax.plot(
        [0, 1],
        [lin_to_y(y, W_min, W_max), lin_to_y(y, W_min, W_max)],
        linewidth=0.8,
        color="lightgrey"
    )

for y in W_minor_ticks:
    ax.plot(
        [0, 1],
        [lin_to_y(y, W_min, W_max), lin_to_y(y, W_min, W_max)],
        linewidth=0.2,
        color="lightgrey"
    )

draw_scale(0,   "darkblue", "RMS (W/mW)", True,  lin_to_y, W_min, W_max, W_ticks, W_minor_ticks, False)
draw_scale(0.01, "darkblue", "",          False, lin_to_y, mW_min, mW_max, mW_ticks, mW_minor_ticks, False, _format=format_number)

draw_scale(0.99, "purple", "V RMS/pk-pk (50Ω)", True,  lin_to_y, Vrms_min, Vrms_max, Vrms_ticks, Vrms_minor_ticks, False)
draw_scale(1.00, "purple", "",          False, lin_to_y, Vpkpk_min, Vpkpk_max, Vpkpk_ticks, Vpkpk_minor_ticks, False, _format=format_number)


draw_scale(0.3,  "darkred", "",  True,  log_to_y, S_min, S_max, S_ticks, S_minor_ticks, False, [1, 9])
draw_scale(0.5,  "darkgreen", "RMS (dBW/dBm)",  True,  log_to_y, dBW_min, dBW_max, dBW_ticks, dBW_minor_ticks, False)
draw_scale(0.51, "darkgreen", "",               False, log_to_y, dBm_min, dBm_max, dBm_ticks, dBm_minor_ticks, False)


# ------------------------------------------------------------
# Formula
# ------------------------------------------------------------

ax.text(
    0.5,
    -0.08,
    "101things.readthedocs.io",
    ha="center",
    va="top",
    fontsize=10,
    color = "blue"
)

ax.text(
    0.3,
    0.38,
    "S Units",
    ha="center",
    va="bottom",
    fontsize=13,
    fontweight="bold",
    color="darkred"
)

ax.set_title(
    "Power Calculator",
    ha="center",
    va="bottom",
    fontsize=16,
    fontweight="bold"
)

# ------------------------------------------------------------
# Output
# ------------------------------------------------------------

plt.savefig(
    "power_calculator.pdf",
    bbox_inches="tight"
)

plt.show()
