
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

def plotar_comparacao_filtros(sinal_original, sinal_filtrado, taxa_amostragem, titulo, nome_arquivo=None):
    N = len(sinal_original)
    tempo = np.linspace(0, N / taxa_amostragem, N, endpoint=False)
    
    # Espectros
    espectro_orig = fft(sinal_original)
    espectro_filt = fft(sinal_filtrado)
    freq = np.fft.fftfreq(N, 1 / taxa_amostragem)
    idx = np.where(freq >= 0)
    freq = freq[idx]
    amp_orig = 2.0 / N * np.abs(espectro_orig[idx])
    amp_filt = 2.0 / N * np.abs(espectro_filt[idx])
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
    
    # Sinais no tempo
    ax1.plot(tempo, sinal_original, 'b-', label='Original')
    ax1.set_title('Sinal Original - Tempo')
    ax1.set_xlabel('Tempo (s)')
    ax1.set_ylabel('Amplitude')
    ax1.grid(True)
    ax1.legend()
    
    ax2.plot(tempo, sinal_filtrado, 'r-', label='Filtrado')
    ax2.set_title('Sinal Filtrado - Tempo')
    ax2.set_xlabel('Tempo (s)')
    ax2.set_ylabel('Amplitude')
    ax2.grid(True)
    ax2.legend()
    
    # Espectros
    ax3.plot(freq, amp_orig, 'b-', label='Original')
    ax3.set_title('Espectro Original')
    ax3.set_xlabel('Frequência (Hz)')
    ax3.set_ylabel('Amplitude')
    ax3.grid(True)
    ax3.legend()
    
    ax4.plot(freq, amp_filt, 'r-', label='Filtrado')
    ax4.set_title('Espectro Filtrado')
    ax4.set_xlabel('Frequência (Hz)')
    ax4.set_ylabel('Amplitude')
    ax4.grid(True)
    ax4.legend()
    
    plt.suptitle(titulo, fontsize=16)
    plt.tight_layout()
    
    if nome_arquivo:
        os.makedirs("resultados", exist_ok=True)
        plt.savefig(os.path.join("resultados", nome_arquivo))
        plt.close(fig)
    else:
        plt.show()

def plotar_resposta_filtro(b, a, taxa_amostragem, titulo, nome_arquivo=None):
    
    from scipy import signal
    
    w, h = signal.freqz(b, a, worN=1024, fs=taxa_amostragem)
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
    
    # Magnitude
    ax1.plot(w, 20 * np.log10(abs(h)))
    ax1.set_title(f'{titulo} - Resposta em Magnitude')
    ax1.set_xlabel('Frequência (Hz)')
    ax1.set_ylabel('Magnitude (dB)')
    ax1.grid(True)
    
    # Fase
    ax2.plot(w, np.angle(h) * 180 / np.pi)
    ax2.set_title(f'{titulo} - Resposta em Fase')
    ax2.set_xlabel('Frequência (Hz)')
    ax2.set_ylabel('Fase (graus)')
    ax2.grid(True)
    
    plt.tight_layout()
    
    if nome_arquivo:
        os.makedirs("resultados", exist_ok=True)
        plt.savefig(os.path.join("resultados", nome_arquivo))
        plt.close(fig)
    else:
        plt.show()

def plotar_matriz_confusao(matriz, digitos, titulo="Matriz de Confusão", nome_arquivo=None):
    
    fig, ax = plt.subplots(figsize=(10, 8))
    im = ax.imshow(matriz, interpolation='nearest', cmap=plt.cm.Blues)
    ax.figure.colorbar(im, ax=ax)
    
    ax.set(xticks=np.arange(matriz.shape[1]),
           yticks=np.arange(matriz.shape[0]),
           xticklabels=digitos, yticklabels=digitos,
           title=titulo,
           ylabel='Dígito Real',
           xlabel='Dígito Detectado')
    
    # Rotacionar os labels do eixo x
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
    
    # Adicionar texto nas células
    thresh = matriz.max() / 2.
    for i in range(matriz.shape[0]):
        for j in range(matriz.shape[1]):
            ax.text(j, i, format(matriz[i, j], 'd'),
                   ha="center", va="center",
                   color="white" if matriz[i, j] > thresh else "black")
    
    plt.tight_layout()
    
    if nome_arquivo:
        os.makedirs("resultados", exist_ok=True)
        plt.savefig(os.path.join("resultados", nome_arquivo))
        plt.close(fig)
    else:
        plt.show()

def plotar_taxa_sucesso_snr(resultados_snr, titulo="Taxa de Sucesso vs SNR", nome_arquivo=None):
    snr_values = list(resultados_snr.keys())
    success_rates = [resultados_snr[snr] * 100 for snr in snr_values]
    
    plt.figure(figsize=(10, 6))
    plt.plot(snr_values, success_rates, 'bo-', linewidth=2, markersize=8)
    plt.title(titulo)
    plt.xlabel('SNR (dB)')
    plt.ylabel('Taxa de Sucesso (%)')
    plt.grid(True, alpha=0.3)
    plt.ylim(0, 105)
    
    # Adicionar linha de referência em 90%
    plt.axhline(y=90, color='r', linestyle='--', alpha=0.7, label='90% de sucesso')
    plt.legend()
    
    plt.tight_layout()
    
    if nome_arquivo:
        os.makedirs("resultados", exist_ok=True)
        plt.savefig(os.path.join("resultados", nome_arquivo))
        plt.close()
    else:
        plt.show()

def plotar_espectrograma(sinal, taxa_amostragem, titulo, nome_arquivo=None):
    from scipy import signal as sig
    
    f, t, Sxx = sig.spectrogram(sinal, taxa_amostragem, nperseg=1024)
    
    plt.figure(figsize=(12, 6))
    plt.pcolormesh(t, f, 10 * np.log10(Sxx), shading='gouraud')
    plt.ylabel('Frequência (Hz)')
    plt.xlabel('Tempo (s)')
    plt.title(titulo)
    plt.colorbar(label='Potência (dB)')
    plt.ylim(0, 2000)  # Limitar a frequência para DTMF
    
    if nome_arquivo:
        os.makedirs("resultados", exist_ok=True)
        plt.savefig(os.path.join("resultados", nome_arquivo))
        plt.close()
    else:
        plt.show()

if __name__ == "__main__":
    # Exemplo de uso
    from gerador_dtmf import gerar_tom_dtmf
    
    taxa = 44100
    duracao = 0.5
    
    # Gerar sinal de teste
    sinal_teste = gerar_tom_dtmf('5', duracao, taxa)
    
    # Plotar sinal e espectro
    plotar_sinal_e_espectro(sinal_teste, taxa, "Tom DTMF - Dígito 5", "teste_visualizacao.png")
    
    print("Gráfico de teste gerado em resultados/teste_visualizacao.png")

