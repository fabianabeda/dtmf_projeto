
import numpy as np
import os
from scipy.io import wavfile

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
