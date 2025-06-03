import time
from scipy.optimize import minimize
from ball_tracker import get_ball_position
from modbus_server import store  # Dette må du ha i din serverfil

# === Konfigurasjon ===
TARGET_Y = 0
SCALE = 1000  # For å sende som INT
KP_ADDR = 7
KI_ADDR = 8
KD_ADDR = 9

# === Funksjon for å sende PID til Modbus (lokalt i RAM) ===
def write_pid_to_modbus(Kp, Ki, Kd):
    kp_val = int(Kp * SCALE)
    ki_val = int(Ki * SCALE)
    kd_val = int(Kd * SCALE)
    store.setValues(3, KP_ADDR, [kp_val])
    store.setValues(3, KI_ADDR, [ki_val])
    store.setValues(3, KD_ADDR, [kd_val])
    print(f"[MODBUS] Skrev Kp={kp_val}, Ki={ki_val}, Kd={kd_val} til adresser 7-9")

# === Leser ballens y-posisjon og beregner feil ===
def get_response_error():
    pos = get_ball_position()
    if pos is None:
        return 9999  # Stor feil hvis ball ikke sees
    y = pos[1]
    error = abs(y - TARGET_Y)
    print(f"[Ball] Y={y}, Feil={error:.1f}")
    return error

# === Kostnadsfunksjon for tuning ===
def cost_function(params):
    Kp, Ki, Kd = params
    print(f"[Tune] Tester Kp={Kp:.3f}, Ki={Ki:.3f}, Kd={Kd:.3f}")
    write_pid_to_modbus(Kp, Ki, Kd)
    time.sleep(1.0)  # Vent på respons

    errors = []
    for _ in range(5):
        errors.append(get_response_error())
        time.sleep(0.2)
    
    avg_error = sum(errors) / len(errors)
    print(f"[Tune] → Snittfeil: {avg_error:.2f}")
    return avg_error

# === Hovedfunksjon ===
def autotune_pid():
    print("[START] Starter autotuning...")
    bounds = [(0.1, 5.0), (0.01, 1.0), (0.01, 1.0)]
    result = minimize(cost_function, [1.0, 0.1, 0.05], bounds=bounds)

    best_Kp, best_Ki, best_Kd = result.x
    print(f"\n🎯 Beste verdier funnet:")
    print(f"Kp = {best_Kp:.3f}")
    print(f"Ki = {best_Ki:.3f}")
    print(f"Kd = {best_Kd:.3f}")

    write_pid_to_modbus(best_Kp, best_Ki, best_Kd)
    return best_Kp, best_Ki, best_Kd

if __name__ == "__main__":
    autotune_pid()
