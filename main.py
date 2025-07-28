from gerador_dtmf import gerar_tom_dtmf
from detector_dtmf import detectar_digito_dtmf, adicionar_ruido_branco, testar_robustez_ruido
from visualizacao import plotar_sinal_e_espectro, plotar_taxa_sucesso_snr, plotar_matriz_confusao
import numpy as np

def main():
    taxa = 44100
    duracao = 0.05
    digitos_teste = [str(i) for i in range(10)] + ["*", "#"]
    snrs = [30, 20, 10, 5, 0, -5, -10]
    
    # Geração de sinais e espectros para dígitos individuais e diferentes SNRs
    for dig in ["1", "5", "6"]:
        sinal = gerar_tom_dtmf(dig, duracao, taxa)
        plotar_sinal_e_espectro(sinal, taxa, f"Sinal Original ({dig})", f"{dig}_original.png", (600, 1500))
        for snr in [10, -10]:
            ruidoso = adicionar_ruido_branco(sinal, snr)
            plotar_sinal_e_espectro(ruidoso, taxa, f"Sinal com Ruído ({dig}) SNR={snr}dB", f"{dig}_ruido_snr{snr}.png", (600, 1500))

    # Teste de robustez ao ruído para todos os dígitos
    resultados_snr_geral = {}
    for digito in digitos_teste:
        print(f"\nTestando robustez ao ruído para o dígito \'{digito}\':")
        resultados_digito = testar_robustez_ruido(digito, taxa, duracao, snr_range=snrs)
        for snr, taxa_sucesso in resultados_digito.items():
            if snr not in resultados_snr_geral:
                resultados_snr_geral[snr] = []
            resultados_snr_geral[snr].append(taxa_sucesso)
    
    # Calcular média da taxa de sucesso para cada SNR
    snr_medias = {snr: np.mean(taxas) for snr, taxas in resultados_snr_geral.items()}
    plotar_taxa_sucesso_snr(snr_medias, nome_arquivo="taxa_sucesso_snr.png")

    # Geração da matriz de confusão para um SNR específico (ex: 0 dB)
    print("\nGerando matriz de confusão para SNR = 0 dB:")
    matriz_confusao = np.zeros((len(digitos_teste), len(digitos_teste)), dtype=int)
    num_testes_matriz = 100 # Número de testes por dígito para a matriz

    for i, digito_real in enumerate(digitos_teste):
        sinal_original = gerar_tom_dtmf(digito_real, duracao, taxa)
        for _ in range(num_testes_matriz):
            sinal_ruidoso = adicionar_ruido_branco(sinal_original, 0) # SNR de 0 dB
            digito_detectado = detectar_digito_dtmf(sinal_ruidoso, taxa)
            
            if digito_detectado in digitos_teste:
                j = digitos_teste.index(digito_detectado)
                matriz_confusao[i, j] += 1
            else:
                # Se não detectado ou detectado como None, pode ser contado como erro
                # ou ter uma categoria 'não detectado' na matriz
                pass # Por simplicidade, ignoramos 'None' para esta matriz
    
    plotar_matriz_confusao(matriz_confusao, digitos_teste, nome_arquivo="matriz_confusao.png")

if __name__ == "__main__":
    main()
