
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft
import os

def plotar_sinal_e_espectro(sinal, taxa_amostragem, titulo, nome_arquivo=None, limite_freq=None):
    N = len(sinal)
    tempo = np.linspace(0, N / taxa_amostragem, N, endpoint=False)
    espectro = fft(sinal)
    freq = np.fft.fftfreq(N, 1 / taxa_amostragem)
    idx = np.where(freq >= 0)
    freq = freq[idx]
    amp = 2.0 / N * np.abs(espectro[idx])

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
    ax1.plot(tempo, sinal)
    ax1.set_title(f'{titulo} - Tempo')
    ax1.set_xlabel('Tempo (s)')
    ax1.set_ylabel('Amplitude')
    ax1.grid(True)

    ax2.plot(freq, amp)
    ax2.set_title(f'{titulo} - Frequência')
    ax2.set_xlabel('Frequência (Hz)')
    ax2.set_ylabel('Amplitude')
    ax2.grid(True)
    if limite_freq:
        ax2.set_xlim(limite_freq)

    plt.tight_layout()
    if nome_arquivo:
        os.makedirs("resultados", exist_ok=True)
        plt.savefig(os.path.join("resultados", nome_arquivo))
        plt.close(fig)
    else:
        plt.show()
