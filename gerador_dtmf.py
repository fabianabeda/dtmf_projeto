import numpy as np
import os
from scipy.io import wavfile

# Frequências DTMF padrão
FREQUENCIAS_DTMF = {
    '1': (697, 1209), '2': (697, 1336), '3': (697, 1477),
    '4': (770, 1209), '5': (770, 1336), '6': (770, 1477),
    '7': (852, 1209), '8': (852, 1336), '9': (852, 1477),
    '*': (941, 1209), '0': (941, 1336), '#': (941, 1477),
}

def gerar_tom_dtmf(digito, duracao, taxa_amostragem):
    if digito not in FREQUENCIAS_DTMF:
        raise ValueError(f"Dígito inválido: {digito}")
    
    f_baixa, f_alta = FREQUENCIAS_DTMF[digito]
    
    t = np.linspace(0, duracao, int(taxa_amostragem * duracao), endpoint=False)
    return (np.sin(2 * np.pi * f_baixa * t) + np.sin(2 * np.pi * f_alta * t)) / 2

def salvar_audio_wav(sinal, taxa_amostragem, nome_arquivo):

    sinal_normalizado = np.int16(sinal / np.max(np.abs(sinal)) * 32767)
    
    # Criar diretório se não existir
    os.makedirs(os.path.dirname(nome_arquivo), exist_ok=True)
    
    # Salvar arquivo WAV
    wavfile.write(nome_arquivo, taxa_amostragem, sinal_normalizado)

def gerar_sequencia_dtmf(digitos, duracao_digito, pausa_entre_digitos, taxa_amostragem):
    sequencia = []
    
    for i, digito in enumerate(digitos):
        # Adicionar tom DTMF
        tom = gerar_tom_dtmf(digito, duracao_digito, taxa_amostragem)
        sequencia.append(tom)
        
        # Adicionar pausa (exceto após o último dígito)
        if i < len(digitos) - 1:
            pausa = np.zeros(int(pausa_entre_digitos * taxa_amostragem))
            sequencia.append(pausa)
    
    return np.concatenate(sequencia)

if __name__ == "__main__":
    # Exemplo de uso
    taxa = 44100
    duracao = 0.5
    
    # Gerar tons individuais
    for digito in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '*', '#']:
        sinal = gerar_tom_dtmf(digito, duracao, taxa)
        salvar_audio_wav(sinal, taxa, f"resultados/dtmf_{digito}.wav")
        print(f"Tom DTMF para '{digito}' gerado e salvo.")
    
    # Gerar sequência de exemplo
    sequencia = gerar_sequencia_dtmf("123456789*0#", 0.3, 0.1, taxa)
    salvar_audio_wav(sequencia, taxa, "resultados/sequencia_dtmf.wav")
    print("Sequência DTMF completa gerada e salva.")


