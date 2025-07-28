import numpy as np
import matplotlib.pyplot as plt
from gerador_dtmf import gerar_tom_dtmf
import os

# Cria a pasta resultados se não existir
os.makedirs("resultados", exist_ok=True)

# Parâmetros do filtro RC
R = 600  # ohms
fc = 1000  # Hz
RC = 1 / (2 * np.pi * fc)
C = RC / R
tau = R * C  # constante de tempo
print(f"RC = {RC:.2e}, C = {C:.2e}")

# Resposta ao impulso h[n] para o filtro RC
taxa_amostragem = 44100
duracao_impulso = 0.02  # segundos
t = np.arange(0, duracao_impulso, 1 / taxa_amostragem)
h = (1 / RC) * np.exp(-t / RC)

# Gera sinal DTMF (ex: '5')
sinal = gerar_tom_dtmf('5', 0.5, taxa_amostragem)

# Convolução no domínio do tempo
sinal_filtrado = np.convolve(sinal, h, mode='same')

# Normaliza o sinal filtrado para ter amplitude semelhante ao original
sinal_filtrado = sinal_filtrado / np.max(np.abs(sinal_filtrado)) * np.max(np.abs(sinal))


# Plota resultado
plt.figure(figsize=(12, 5))
plt.plot(sinal[:1000], label='Sinal original')
plt.plot(sinal_filtrado[:1000], label='Filtrado (RC)')
plt.title("Comparação do Sinal Original e Filtrado (Filtro RC Passa-Baixa)")
plt.xlabel("Amostras")
plt.ylabel("Amplitude")
plt.legend()
plt.grid(True)
plt.tight_layout()

# Salva o gráfico na pasta resultados
plt.savefig("resultados/filtro_rc_convolucao.png")
plt.close()
