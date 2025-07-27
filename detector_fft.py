
import numpy as np
from scipy.fft import fft

def detectar_frequencias_fft(sinal, taxa_amostragem, faixa_frequencia=None):
    N = len(sinal)
    espectro = fft(sinal)
    freq = np.fft.fftfreq(N, 1 / taxa_amostragem)
    idx_pos = np.where(freq >= 0)
    freq = freq[idx_pos]
    espectro = 2.0/N * np.abs(espectro[idx_pos])
    freq_filtrada, espec_filtrada = freq, espectro

    if faixa_frequencia:
        min_f, max_f = faixa_frequencia
        idx_validos = np.where((freq >= min_f) & (freq <= max_f))
        freq_filtrada = freq[idx_validos]
        espec_filtrada = espectro[idx_validos]

    freq_detectadas = []
    if len(espec_filtrada) > 0:
        indices = np.argsort(espec_filtrada)[::-1]
        limiar = 0.1 * np.max(espec_filtrada)
        for i in indices:
            if espec_filtrada[i] > limiar and all(abs(freq_filtrada[i] - f) > 10 for f in freq_detectadas):
                freq_detectadas.append(freq_filtrada[i])
            if len(freq_detectadas) == 2:
                break
    return sorted(freq_detectadas)
