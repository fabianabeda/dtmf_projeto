
# 📞 Projeto DTMF com Análise por FFT e Filtros
**Projeto desenvolvido na disciplina de Análise de Sinais e Sistemas Lineares.**

Este projeto implementa um sistema de geração, análise e detecção de tons DTMF (Dual-Tone Multi-Frequency), utilizando FFT e filtros digitais para identificação precisa dos dígitos, mesmo em presença de ruído.

---

## 📁 Estrutura do Projeto

```
DTMF_PROJETO/
├── __pycache__/              # Cache automático do Python
├── resultados/               # Pasta de saída com imagens e gráficos gerados
│
├── __init__.py               # Inicialização do pacote (opcional)
├── main.py                   # Script principal de execução do projeto
├── gerador_dtmf.py           # Geração dos sinais DTMF (tom de teclado telefônico)
├── gerar_filtros.py          # Geração e salvamento de sinais filtrados com gráficos
├── filtros.py                # Implementação de filtros digitais (Butterworth, etc.)
├── filtro_rc_convolucao.py   # Simulação de filtro RC analógico via convolução
├── detector_dtmf.py          # Detecção de dígitos DTMF por método direto
├── detector_fft.py           # Detecção de frequências com FFT e espectrograma
├── visualizacao.py           # Funções auxiliares para visualização e gráficos
│
├── index.html                # Página do relatório interativo
├── styles.css                # Estilo da página HTML
├── script.js                 # Funcionalidades interativas da página
│
├── requirements.txt          # Dependências do projeto
├── README.txt                # Descrição alternativa do projeto (legado)
```

---

## 🚀 Como Executar

### 1. Clone ou baixe este repositório
Ou apenas extraia o `.zip` que você baixou.

### 2. Instale as dependências

Certifique-se de estar usando **Python 3.8+** e instale as bibliotecas com:

```bash
pip install -r requirements.txt
```

### 3. Execute o projeto

Dentro da pasta `DTMF_PROJETO`, execute:

```bash
python3 main.py
```

Ou, para gerar os gráficos de filtragem RC:

```bash
python3 gerar_filtros.py
```

---

## 📊 Resultados

Os gráficos gerados mostram:

- O espectro dos tons DTMF originais e com ruído
- A atuação dos filtros digitais e analógicos
- A comparação entre sinais filtrados e não filtrados

Os arquivos são salvos na pasta `resultados/`. Exemplos:

- `5_original.png`
- `5_ruido_snr10.png`
- `dtmf_filtered_low_signal.png`
- `espectro_fft_digito_5.png`

---

## 🧠 Tecnologias Usadas

- Python 3
- [NumPy](https://numpy.org/)
- [SciPy](https://scipy.org/)
- [Matplotlib](https://matplotlib.org/)

---
