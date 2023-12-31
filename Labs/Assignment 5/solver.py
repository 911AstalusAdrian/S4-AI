theta_ranges = {"NVB": (None, -40, -25), "NB": (-40, -25, -10), "N": (-20, -10, 0), "ZO": (-5, 0, 5), "P": (0, 10, 20),
                "PB": (10, 25, 40), "PVB": (25, 40, None)}
omega_ranges = {"NB": (None, -8, -3), "N": (-6, -3, 0), "ZO": (-1, 0, 1), "P": (0, 3, 6), "PB": (3, 8, None)}
fRanges = {"NVVB": (None, -32, -24), "NVB": (-32, -24, -16), "NB": (-24, -16, -8), "N": (-16, -8, 0), "Z": (-4, 0, 4),
           "P": (0, 8, 16), "PB": (8, 16, 24), "PVB": (16, 24, 32), "PVVB": (24, 32, None)}
bValues = {key: value[1] for key, value in fRanges.items()}
fuzzy_table = dict()
fuzzy_table["NB"] = dict()
fuzzy_table["NB"]["NB"] = "NVVB"
fuzzy_table["NB"]["N"] = "NVB"
fuzzy_table["NB"]["ZO"] = "NB"
fuzzy_table["NB"]["P"] = "N"
fuzzy_table["NB"]["PB"] = "Z"
fuzzy_table["N"] = dict()
fuzzy_table["N"]["NB"] = "NVB"
fuzzy_table["N"]["N"] = "NB"
fuzzy_table["N"]["ZO"] = "N"
fuzzy_table["N"]["P"] = "Z"
fuzzy_table["N"]["PB"] = "P"
fuzzy_table["ZO"] = dict()
fuzzy_table["ZO"]["NB"] = "NB"
fuzzy_table["ZO"]["N"] = "N"
fuzzy_table["ZO"]["ZO"] = "Z"
fuzzy_table["ZO"]["P"] = "P"
fuzzy_table["ZO"]["PB"] = "PB"
fuzzy_table["P"] = dict()
fuzzy_table["P"]["NB"] = "N"
fuzzy_table["P"]["N"] = "Z"
fuzzy_table["P"]["ZO"] = "P"
fuzzy_table["P"]["P"] = "PB"
fuzzy_table["P"]["PB"] = "PVB"
fuzzy_table["PB"] = dict()
fuzzy_table["PB"]["NB"] = "Z"
fuzzy_table["PB"]["N"] = "P"
fuzzy_table["PB"]["ZO"] = "PB"
fuzzy_table["PB"]["P"] = "PVB"
fuzzy_table["PB"]["PB"] = "PVVB"
fuzzy_table["PVB"] = dict()
fuzzy_table["PVB"]["NB"] = "P"
fuzzy_table["PVB"]["N"] = "PB"
fuzzy_table["PVB"]["ZO"] = "PVB"
fuzzy_table["PVB"]["P"] = "PVVB"
fuzzy_table["PVB"]["PB"] = "PVVB"
fuzzy_table["NVB"] = dict()
fuzzy_table["NVB"]["N"] = "NVVB"
fuzzy_table["NVB"]["ZO"] = "NVB"
fuzzy_table["NVB"]["P"] = "NB"
fuzzy_table["NVB"]["PB"] = "N"
fuzzy_table["NVB"]["NB"] = "NVVB"


def fuzzify(x, left, middle, right):
    if left is not None and left <= x < middle:
        return (x - left) / (middle - left)
    elif right is not None and middle <= x < right:
        return (right - x) / (right - middle)
    elif left is None and x <= middle:
        return 1
    elif right is None and x >= middle:
        return 1
    else:
        return 0


def compute_values(value, ranges):
    to_return = dict()
    for key in ranges:
        to_return[key] = fuzzify(value, *ranges[key])
    return to_return


def solver(theta, omega):
    theta_values = compute_values(theta, theta_ranges)
    omega_values = compute_values(omega, omega_ranges)
    f_values = dict()
    for theta_key in fuzzy_table:
        for omega_key, f_value in fuzzy_table[theta_key].items():
            value = min(theta_values[theta_key], omega_values[omega_key])
            if f_value not in f_values:
                f_values[f_value] = value
            else:
                f_values[f_value] = max(value, f_values[f_value])
    s = sum(f_values.values())
    if s == 0:
        return None
    return sum(f_values[fSet] * bValues[fSet] for fSet in f_values.keys())
