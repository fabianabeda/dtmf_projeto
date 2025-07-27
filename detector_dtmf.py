
import numpy as np
from scipy.fft import fft
from filtros import aplicar_passabaixa_butter, aplicar_passaalta_butter
from gerador_dtmf import FREQUENCIAS_DTMF


MAPA_FREQUENCIA_DIGITO = {
    tuple(sorted(f)): d for d, f in FREQUENCIAS_DTMF.items()
}

def detectar_pico_freq(sinal, taxa_amostragem, faixa):
    N = len(sinal)
    freq = np.fft.fftfreq(N, 1 / taxa_amostragem)
    espectro = fft(sinal)
    indices = np.where(freq >= 0)
    freq_pos = freq[indices]
    amp = 2.0 / N * np.abs(espectro[indices])
    indices_validos = np.where((freq_pos >= faixa[0]) & (freq_pos <= faixa[1]))
    if len(indices_validos[0]) > 0:
        idx_pico = indices_validos[0][np.argmax(amp[indices_validos])]
        return freq_pos[idx_pico]
    return None

def detectar_digito_dtmf(sinal, taxa_amostragem, ordem_filtro=5):
    baixa = aplicar_passabaixa_butter(sinal, 1000, taxa_amostragem, ordem_filtro)
    alta = aplicar_passaalta_butter(sinal, 1100, taxa_amostragem, ordem_filtro)
    freq_baixa = detectar_pico_freq(baixa, taxa_amostragem, (600, 1000))
    freq_alta = detectar_pico_freq(alta, taxa_amostragem, (1200, 1500))
    if freq_baixa and freq_alta:
        todas_freqs = sorted(set(f for par in FREQUENCIAS_DTMF.values() for f in par))
        f1 = min(todas_freqs, key=lambda f: abs(f - freq_baixa))
        f2 = min(todas_freqs, key=lambda f: abs(f - freq_alta))
        return MAPA_FREQUENCIA_DIGITO.get(tuple(sorted((f1, f2))))
    return None

def adicionar_ruido_branco(sinal, snr_db):
    potencia_sinal = np.mean(sinal**2)
    snr_linear = 10 ** (snr_db / 10)
    potencia_ruido = potencia_sinal / snr_linear
    ruido = np.random.normal(0, np.sqrt(potencia_ruido), len(sinal))
    return sinal + ruido
