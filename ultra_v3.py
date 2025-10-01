import numba as nb
import numpy as np
import pandas as pd

@nb.njit(fastmath=True, cache=True)
def ultra_01_v3(ret):
    return np.sign(ret) * (np.abs(ret) ** 0.3)

@nb.njit(fastmath=True, cache=True)
def ultra_02_v3(ret):
    return np.tanh(ret * 8)

@nb.njit(fastmath=True, cache=True)
def ultra_03_v3(ret):
    return np.sign(ret) * (np.abs(ret) ** 0.15)   # eski 0.10 → daha hassas

@nb.njit(fastmath=True, cache=True)
def ultra_04_v3(ret):
    return ret / (1 + np.abs(ret))

@nb.njit(fastmath=True, cache=True)
def ultra_05_v3(ret):
    return np.log1p(ret) if ret > -0.99 else -10

@nb.njit(fastmath=True, cache=True)
def ultra_06_v3(ret):
    return np.arctan(ret * 5)

@nb.njit(fastmath=True, cache=True)
def ultra_07_v3(ret):
    return np.tanh(ret * 12)                   # eski 10 → 12

@nb.njit(fastmath=True, cache=True)
def ultra_08_v3(ret):
    return ret * np.exp(-np.abs(ret))

@nb.njit(fastmath=True, cache=True)
def ultra_09_v3(ret):
    return np.sign(ret) * np.sqrt(np.abs(ret))

@nb.njit(fastmath=True, cache=True)
def ultra_10_v3(ret):
    return ret / (1 + ret**2)

@nb.njit(fastmath=True, cache=True)
def ultra_11_v3(ret):
    return np.sinh(ret) / np.cosh(ret * 2)

@nb.njit(fastmath=True, cache=True)
def ultra_12_v3(ret):
    return np.sin(ret * np.pi / 2) if -1 <= ret <= 1 else np.sign(ret)

@nb.njit(fastmath=True, cache=True)
def ultra_13_v3(ret):
    return ret * (2 / (1 + np.exp(-ret * 3)) - 1)

@nb.njit(fastmath=True, cache=True)
def ultra_14_v3(ret):
    return np.sign(ret) * (1 - np.exp(-np.abs(ret)))

@nb.njit(fastmath=True, cache=True)
def ultra_15_v3(ret):
    return ret / np.sqrt(1 + ret**2)

@nb.njit(fastmath=True, cache=True)
def ultra_16_v3(ret):
    return np.tanh(ret) * np.exp(-ret**2 / 2)

@nb.njit(fastmath=True, cache=True)
def ultra_17_v3(ret):
    return ret * (1 - np.abs(ret) / 2) if np.abs(ret) < 2 else np.sign(ret)

@nb.njit(fastmath=True, cache=True)
def ultra_18_v3(ret):
    return np.arcsin(np.clip(ret, -0.99, 0.99))

@nb.njit(fastmath=True, cache=True)
def ultra_19_v3(ret):
    return ret * np.cos(ret * np.pi / 4)

# Tüm ULTRA v3 fonksiyonları
ULTRA_V3_FUNCS = [
    ultra_01_v3, ultra_02_v3, ultra_03_v3, ultra_04_v3, ultra_05_v3,
    ultra_06_v3, ultra_07_v3, ultra_08_v3, ultra_09_v3, ultra_10_v3,
    ultra_11_v3, ultra_12_v3, ultra_13_v3, ultra_14_v3, ultra_15_v3,
    ultra_16_v3, ultra_17_v3, ultra_18_v3, ultra_19_v3
]

def compute_ultra_v3_core(returns):
    """ULTRA v3 hesaplama - Numba devre dışı"""
    out = np.zeros(19)
    
    out[0] = np.sign(returns[0]) * (np.abs(returns[0]) ** 0.3)
    out[1] = np.tanh(returns[1] * 8)
    out[2] = np.sign(returns[2]) * (np.abs(returns[2]) ** 0.15)
    out[3] = returns[3] / (1 + np.abs(returns[3]))
    out[4] = np.log1p(returns[4]) if returns[4] > -0.99 else -10
    out[5] = np.arctan(returns[5] * 5)
    out[6] = np.tanh(returns[6] * 12)
    out[7] = returns[7] * np.exp(-np.abs(returns[7]))
    out[8] = np.sign(returns[8]) * np.sqrt(np.abs(returns[8]))
    out[9] = returns[9] / (1 + returns[9]**2)
    out[10] = np.sinh(returns[10]) / np.cosh(returns[10] * 2)
    out[11] = np.sin(returns[11] * np.pi / 2) if -1 <= returns[11] <= 1 else np.sign(returns[11])
    out[12] = returns[12] * (2 / (1 + np.exp(-returns[12] * 3)) - 1)
    out[13] = np.sign(returns[13]) * (1 - np.exp(-np.abs(returns[13])))
    out[14] = returns[14] / np.sqrt(1 + returns[14]**2)
    out[15] = np.tanh(returns[15]) * np.exp(-returns[15]**2 / 2)
    out[16] = returns[16] * (1 - np.abs(returns[16]) / 2) if np.abs(returns[16]) < 2 else np.sign(returns[16])
    out[17] = np.arcsin(np.maximum(-0.99, np.minimum(0.99, returns[17])))
    out[18] = returns[18] * np.cos(returns[18] * np.pi / 4)
    
    return out

def compute_ultra_v3(returns):
    """ULTRA v3 ana hesaplama fonksiyonu"""
    try:
        if len(returns) < 19:
            return 0.0
        
        # Son 19 getiriyi numpy array'e çevir - null ve inf değerleri temizle
        raw_returns = returns[-19:]
        cleaned_returns = []
        
        for r in raw_returns:
            if pd.isna(r) or np.isinf(r):
                cleaned_returns.append(0.0)
            else:
                try:
                    cleaned_returns.append(float(r))
                except (ValueError, TypeError):
                    cleaned_returns.append(0.0)
        
        returns_array = np.array(cleaned_returns, dtype=np.float64)
        
        # Numba ile hızlandırılmış hesaplama
        ultra_scores = compute_ultra_v3_core(returns_array)
        
        # Ortalama al ve tanh ile normalize et
        mean_score = np.mean(ultra_scores)
        final_score = float(np.tanh(mean_score)) * 45  # eski 35 → 45
        
        return final_score
        
    except Exception as e:
        print(f"ULTRA v3 hesaplama hatası: {e}")
        return 0.0