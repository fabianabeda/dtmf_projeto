import numpy as np
from scipy import signal

def aplicar_passabaixa_butter(sinal, freq_corte, taxa_amostragem, ordem=5):
    nyquist = taxa_amostragem / 2
    freq_norm = freq_corte / nyquist
    
    # Garantir que a frequência normalizada está no intervalo válido
    freq_norm = min(freq_norm, 0.99)
    
    b, a = signal.butter(ordem, freq_norm, btype='low')
    return signal.filtfilt(b, a, sinal)

def aplicar_passalta_butter(sinal, freq_corte, taxa_amostragem, ordem=5):
    nyquist = taxa_amostragem / 2
    freq_norm = freq_corte / nyquist
    
    # Garantir que a frequência normalizada está no intervalo válido
    freq_norm = min(freq_norm, 0.99)
    
    b, a = signal.butter(ordem, freq_norm, btype='high')
    return signal.filtfilt(b, a, sinal)

def aplicar_passafaixa_butter(sinal, freq_baixa, freq_alta, taxa_amostragem, ordem=5):
    nyquist = taxa_amostragem / 2
    freq_baixa_norm = freq_baixa / nyquist
    freq_alta_norm = freq_alta / nyquist
    
    # Garantir que as frequências normalizadas estão no intervalo válido
    freq_baixa_norm = max(freq_baixa_norm, 0.01)
    freq_alta_norm = min(freq_alta_norm, 0.99)
    
    b, a = signal.butter(ordem, [freq_baixa_norm, freq_alta_norm], btype='band')
    return signal.filtfilt(b, a, sinal)

def filtro_rc_analogico(sinal, taxa_amostragem, freq_corte):
    # Constante de tempo RC
    tau = 1 / (2 * np.pi * freq_corte)
    
    # Resposta ao impulso do filtro RC
    t = np.arange(0, 5 * tau, 1 / taxa_amostragem)
    h = (1 / tau) * np.exp(-t / tau)
    
    # Aplicar convolução
    sinal_filtrado = np.convolve(sinal, h, mode='same')
    
    # Normalizar para manter a amplitude
    return sinal_filtrado * (np.max(np.abs(sinal)) / np.max(np.abs(sinal_filtrado)))

def projetar_filtro_chebyshev(freq_corte, taxa_amostragem, ordem=5, ripple=0.5):
    nyquist = taxa_amostragem / 2
    freq_norm = freq_corte / nyquist
    freq_norm = min(freq_norm, 0.99)
    
    return signal.cheby1(ordem, ripple, freq_norm, btype='low')

def projetar_filtro_elliptic(freq_corte, taxa_amostragem, ordem=5, ripple=0.5, atenuacao=40):
    nyquist = taxa_amostragem / 2
    freq_norm = freq_corte / nyquist
    freq_norm = min(freq_norm, 0.99)
    
    return signal.ellip(ordem, ripple, atenuacao, freq_norm, btype='low')

def calcular_resposta_frequencia(b, a, taxa_amostragem, pontos=1024):
    w, h = signal.freqz(b, a, worN=pontos, fs=taxa_amostragem)
    return w, h

if __name__ == "__main__":
    # Exemplo de uso dos filtros
    import matplotlib.pyplot as plt
    
    # Gerar sinal de teste
    taxa = 44100
    t = np.linspace(0, 1, taxa, endpoint=False)
    
    # Sinal composto por múltiplas frequências
    sinal_teste = (np.sin(2 * np.pi * 500 * t) +  # 500 Hz
                   np.sin(2 * np.pi * 1500 * t) +  # 1500 Hz
                   np.sin(2 * np.pi * 3000 * t))   # 3000 Hz
    
    # Aplicar diferentes filtros
    sinal_pb = aplicar_passabaixa_butter(sinal_teste, 1000, taxa)
    sinal_pa = aplicar_passalta_butter(sinal_teste, 1000, taxa)
    sinal_pf = aplicar_passafaixa_butter(sinal_teste, 800, 2000, taxa)
    
    print("Filtros aplicados com sucesso!")
    print(f"Sinal original: {len(sinal_teste)} amostras")
    print(f"Sinal passa-baixa: {len(sinal_pb)} amostras")
    print(f"Sinal passa-alta: {len(sinal_pa)} amostras")
    print(f"Sinal passa-faixa: {len(sinal_pf)} amostras")