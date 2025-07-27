
from scipy.signal import butter, lfilter

def butterworth(corte, fs, tipo, ordem=5):
    nyq = 0.5 * fs
    normalizado = corte / nyq if isinstance(corte, (int, float)) else [c / nyq for c in corte]
    b, a = butter(ordem, normalizado, btype=tipo)
    return b, a

def aplicar_filtro(sinal, corte, fs, tipo, ordem=5):
    b, a = butterworth(corte, fs, tipo, ordem)
    return lfilter(b, a, sinal)

def aplicar_passabaixa_butter(sinal, corte, fs, ordem=5):
    return aplicar_filtro(sinal, corte, fs, 'low', ordem)

def aplicar_passaalta_butter(sinal, corte, fs, ordem=5):
    return aplicar_filtro(sinal, corte, fs, 'high', ordem)

def aplicar_passafaixa_butter(sinal, faixa, fs, ordem=5):
    return aplicar_filtro(sinal, faixa, fs, 'band', ordem)
