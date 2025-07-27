
from gerador_dtmf import gerar_tom_dtmf
from detector_dtmf import detectar_digito_dtmf, adicionar_ruido_branco
from visualizacao import plotar_sinal_e_espectro


def main():
    taxa = 44100
    duracao = 0.5
    digitos = ['1', '2', '3', '4', '5', '6']
    snrs = [30, 20, 10]

    for dig in digitos:
        sinal = gerar_tom_dtmf(dig, duracao, taxa)
        plotar_sinal_e_espectro(sinal, taxa, f"Sinal Original ({dig})", f"{dig}_original.png", (600, 1500))
        for snr in snrs:
            ruidoso = adicionar_ruido_branco(sinal, snr)
            plotar_sinal_e_espectro(ruidoso, taxa, f"Sinal com Ruído {dig} SNR={snr}", f"{dig}_ruido_snr{snr}.png", (600, 1500))
            detectado = detectar_digito_dtmf(ruidoso, taxa)
            print(f"Dígito: {dig}, Detectado: {detectado}, SNR={snr} dB")

if __name__ == '__main__':
    main()
