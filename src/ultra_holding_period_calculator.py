import numpy as np
from numba import njit

@njit(fastmath=True, cache=True)
def ultra_01(ret: float) -> float:
    return np.sign(ret) * (abs(ret) ** 0.1)

@njit(fastmath=True, cache=True)
def ultra_02(ret: float) -> float:
    return np.tanh(ret * 10)

@njit(fastmath=True, cache=True)
def ultra_03(ret: float) -> float:
    return np.sin(ret * np.pi * 2)

@njit(fastmath=True, cache=True)
def ultra_04(ret: float) -> float:
    return np.cos(ret * np.pi * 3)

@njit(fastmath=True, cache=True)
def ultra_05(ret: float) -> float:
    return ret * 0.5 + np.sin(ret * 5)

@njit(fastmath=True, cache=True)
def ultra_06(ret: float) -> float:
    return np.log1p(abs(ret)) * np.sign(ret)

@njit(fastmath=True, cache=True)
def ultra_07(ret: float) -> float:
    return np.sqrt(abs(ret)) * np.sign(ret)

@njit(fastmath=True, cache=True)
def ultra_08(ret: float) -> float:
    return ret ** 3 if abs(ret) < 0.1 else ret

@njit(fastmath=True, cache=True)
def ultra_09(ret: float) -> float:
    return np.exp(-abs(ret)) * ret

@njit(fastmath=True, cache=True)
def ultra_10(ret: float) -> float:
    return ret / (1 + abs(ret))

@njit(fastmath=True, cache=True)
def ultra_11(ret: float) -> float:
    return np.sin(ret * 7) * 0.3 + ret * 0.7

@njit(fastmath=True, cache=True)
def ultra_12(ret: float) -> float:
    return ret * np.cos(ret * 4)

@njit(fastmath=True, cache=True)
def ultra_13(ret: float) -> float:
    return np.tanh(ret * 5) * 0.8

@njit(fastmath=True, cache=True)
def ultra_14(ret: float) -> float:
    return ret * (1 - abs(ret) * 0.1)

@njit(fastmath=True, cache=True)
def ultra_15(ret: float) -> float:
    return np.sin(ret * 12) * 0.2 + ret * 0.8

@njit(fastmath=True, cache=True)
def ultra_16(ret: float) -> float:
    return ret * np.exp(-ret**2)

@njit(fastmath=True, cache=True)
def ultra_17(ret: float) -> float:
    return np.arctan(ret * 10) / np.pi * 2

@njit(fastmath=True, cache=True)
def ultra_18(ret: float) -> float:
    return ret * (2 / (1 + np.exp(-abs(ret))))

@njit(fastmath=True, cache=True)
def ultra_19(ret: float) -> float:
    return np.sign(ret) * np.log1p(abs(ret))

# 19 fonksiyon listesi
ULTRA_FUNCS = [ultra_01, ultra_02, ultra_03, ultra_04, ultra_05,
               ultra_06, ultra_07, ultra_08, ultra_09, ultra_10,
               ultra_11, ultra_12, ultra_13, ultra_14, ultra_15,
               ultra_16, ultra_17, ultra_18, ultra_19]

def compute_ultra_scores(returns: np.ndarray) -> np.ndarray:
    """
    returns: 1D numpy array (991,)
    returns: (991, 19) ndarray
    """
    out = np.empty((returns.size, 19))
    for i, f in enumerate(ULTRA_FUNCS):
        for j in range(returns.size):
            out[j, i] = f(returns[j])
    return out