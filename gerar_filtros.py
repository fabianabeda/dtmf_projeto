import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter, freqz
from gerador_dtmf import gerar_tom_dtmf
from scipy.fft import fft, fftfreq

Fs = 8000  # Hz
duracao = 0.5  # segundos
digito = '5'
sinal = gerar_tom_dtmf(digito, Fs, duracao)
t = np.linspace(0, duracao, int(Fs * duracao), endpoint=False)

# Filtro passa-faixa para 770 Hz
def filtro_banda(freq_central, largura, Fs, ordem=4):
    nyq = 0.5 * Fs
    low = (freq_central - largura/2) / nyq
    high = (freq_central + largura/2) / nyq
    b, a = butter(ordem, [low, high], btype='band')
    return b, a

# Aplicar filtro e plotar
def aplicar_e_plotar(freq, label, nome_arquivo):
    b, a = filtro_banda(freq, 80, Fs)
    sinal_filtrado = lfilter(b, a, sinal)

    # FFT
    N = len(sinal_filtrado)
    freqs = fftfreq(N, 1/Fs)
    espectro = np.abs(fft(sinal_filtrado))

    plt.figure(figsize=(12, 4))

    # Domínio do tempo
    plt.subplot(1, 2, 1)
    plt.plot(t, sinal_filtrado)
    plt.title(f'Sinal Filtrado - {label}')
    plt.xlabel('Tempo (s)')
    plt.ylabel('Amplitude')

    # Domínio da frequência
    plt.subplot(1, 2, 2)
    plt.plot(freqs[:N//2], espectro[:N//2])
    plt.title(f'Espectro - {label}')
    plt.xlabel('Frequência (Hz)')
    plt.ylabel('Magnitude')

    plt.tight_layout()
    plt.savefig(f'resultados/{nome_arquivo}.png')
    plt.close()

# Gerar figuras
aplicar_e_plotar(770, 'Frequência Baixa (770 Hz)', 'dtmf_filtered_low_signal')
aplicar_e_plotar(1336, 'Frequência Alta (1336 Hz)', 'dtmf_filtered_high_signal')
