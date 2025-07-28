import numpy as np
from scipy.fft import fft
from filtros import aplicar_passabaixa_butter, aplicar_passalta_butter
from gerador_dtmf import FREQUENCIAS_DTMF

# Mapa de frequências para dígitos
MAPA_FREQUENCIA_DIGITO = {
    tuple(sorted(f)): d for d, f in FREQUENCIAS_DTMF.items()
}

def detectar_pico_freq(sinal, taxa_amostragem, faixa):
    
    N = len(sinal)
    freq = np.fft.fftfreq(N, 1 / taxa_amostragem)
    espectro = fft(sinal)
    indices = np.where((freq >= faixa[0]) & (freq <= faixa[1]))
    freq_pos = freq[indices]
    amp = 2.0 / N * np.abs(espectro[indices])
    
    indices_validos = np.where((freq_pos >= faixa[0]) & (freq_pos <= faixa[1]))
    
    if len(indices_validos[0]) > 0:
        idx_pico = indices_validos[0][np.argmax(amp[indices_validos])]
        pico_amplitude = amp[idx_pico]
        
        # Definir um limiar de amplitude. Você precisará experimentar com este valor.
        # Por exemplo, 0.15 ou 0.2 pode ser um bom ponto de partida.
        limiar_amplitude = 0.15  # Este valor é um exemplo e precisa ser ajustado com testes
        
        if pico_amplitude < limiar_amplitude:
            return None  # Sinal muito fraco ou é apenas ruído, não detecta a frequência
        
        return freq_pos[idx_pico]
    
    return None

def detectar_digito_dtmf(sinal, taxa_amostragem, ordem_filtros=5):
    
    # Aplicar filtros para separar frequências baixas e altas
    baixa = aplicar_passabaixa_butter(sinal, 1000, taxa_amostragem, ordem_filtros)
    alta = aplicar_passalta_butter(sinal, 1100, taxa_amostragem, ordem_filtros)
    
    # Detectar picos de frequência
    freq_baixa = detectar_pico_freq(baixa, taxa_amostragem, (600, 1000))
    freq_alta = detectar_pico_freq(alta, taxa_amostragem, (1200, 1500))
    
    if freq_baixa and freq_alta:
        # Encontrar as frequências DTMF mais próximas
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

def testar_robustez_ruido(digito, taxa_amostragem, duracao=0.5, snr_range=range(-10, 31, 5)):
   
    from gerador_dtmf import gerar_tom_dtmf
    
    resultados = {}
    sinal_original = gerar_tom_dtmf(digito, duracao, taxa_amostragem)
    
    for snr in snr_range:
        sucessos = 0
        total_testes = 100
        
        for _ in range(total_testes):
            sinal_ruidoso = adicionar_ruido_branco(sinal_original, snr)
            digito_detectado = detectar_digito_dtmf(sinal_ruidoso, taxa_amostragem)
            
            if digito_detectado == digito:
                sucessos += 1
        
        taxa_sucesso = sucessos / total_testes
        resultados[snr] = taxa_sucesso
        print(f"SNR: {snr} dB, Taxa de sucesso: {taxa_sucesso:.2%}")
    
    return resultados

if __name__ == "__main__":
    # Teste básico
    from gerador_dtmf import gerar_tom_dtmf
    
    taxa = 44100
    duracao = 0.5
    
    # Testar detecção para cada dígito
    print("Testando detecção DTMF para sinais puros:")
    for digito in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '*', '#']:
        sinal = gerar_tom_dtmf(digito, duracao, taxa)
        detectado = detectar_digito_dtmf(sinal, taxa)
        status = "✓" if detectado == digito else "✗"
        print(f"Dígito {digito}: Detectado {detectado} {status}")
    
    # Testar robustez ao ruído para o dígito '5'
    print("\nTestando robustez ao ruído para o dígito '5':")
    testar_robustez_ruido('5', taxa)

