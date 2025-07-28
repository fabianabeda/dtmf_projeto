
# 📞 Projeto DTMF - Detecção de Tons Telefônicos

Este projeto detecta dígitos DTMF (Dual-Tone Multi-Frequency) utilizando FFT, filtros Butterworth e simulação de filtro RC por convolução. Foi desenvolvido para a disciplina de Sinais e Sistemas.

## ▶️ Como executar

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

2. Execute a análise principal:
```bash
python main.py
```

3. Para gerar gráficos adicionais (ex: filtro RC):
```bash
python gerar_filtros.py
```

## 📁 Principais arquivos

- `gerador_dtmf.py`: gera os tons DTMF
- `filtros.py`: aplica filtros digitais
- `filtro_rc_convolucao.py`: simula filtro RC
- `detector_fft.py`: detecta frequências por FFT
- `index.html`: relatório interativo com resultados
- `resultados/`: gráficos gerados automaticamente

## ⚙️ Requisitos

- Python 3.8+
- NumPy, SciPy, Matplotlib

---

Relatório técnico completo disponível em `index.html`.
