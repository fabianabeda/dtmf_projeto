
# Projeto DTMF com Análise por FFT e Filtros

Este projeto implementa um sistema de geração, análise e detecção de tons DTMF (Dual-Tone Multi-Frequency), utilizando FFT e filtros digitais para identificação precisa dos dígitos, mesmo em presença de ruído.

## 📁 Estrutura do Projeto

```
dtmf_project/
├── main.py                 # Script principal de execução
├── gerador_dtmf.py         # Geração dos sinais DTMF
├── filtros.py              # Filtros Butterworth passa-baixa, alta e faixa
├── detector_dtmf.py        # Detecção de dígitos DTMF
├── detector_fft.py         # Detecção de frequências por FFT
├── visualizacao.py         # Funções de plotagem e visualização
├── requirements.txt        # Dependências do projeto
```

## 🚀 Como Executar

### 1. Clone ou baixe este repositório
Ou apenas extraia o `.zip` que você baixou.

### 2. Instale as dependências
Certifique-se de estar usando Python 3.8+ e instale as bibliotecas necessárias:

```bash
pip install -r requirements.txt
```

### 3. Execute o projeto
Dentro da pasta `dtmf_projeto`, execute:

```bash
python3 main.py
```

Isso irá:
- Gerar sinais DTMF para os dígitos 1 a 6
- Adicionar ruído com SNR de 30, 20 e 10 dB
- Detectar os dígitos automaticamente
- Gerar gráficos no tempo e frequência salvos na pasta `resultados/`

## 📊 Resultados
Os gráficos mostram a decomposição do sinal em frequência, evidenciando os pares DTMF mesmo com ruído.

Os nomes dos arquivos gerados são como:

- `5_original.png`
- `5_ruido_snr10.png`
- etc.

## 🧠 Tecnologias Usadas

- Python 3
- Numpy
- Scipy
- Matplotlib


