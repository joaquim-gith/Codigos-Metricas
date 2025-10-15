import os
import json
import re
from statistics import mean

FOLDER = "."  # o script deve estar dentro da pasta QwenMax

def tokenize(text):
    if not isinstance(text, str):
        return []
    text = text.lower()
    tokens = re.findall(r'[a-záàâãéèêíìîóòôõúùûçñ0-9]+', text, flags=re.UNICODE)
    return tokens

def lexical_diversity(text):
    tokens = tokenize(text)
    if not tokens:
        return 0.0
    return len(set(tokens)) / len(tokens)

def numero_inicio(nome):
    m = re.match(r"(\d+)", nome)
    return int(m.group(1)) if m else float('inf')

resultados = []
ttrs = []

for arquivo in sorted(os.listdir(FOLDER), key=numero_inicio):
    if not arquivo.lower().endswith(".json"):
        continue

    caminho = os.path.join(FOLDER, arquivo)
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        continue  # ignora os arquivos inválidos

    redacao = data.get("redacao")
    if not redacao:
        continue

    # Junta as frases em ordem numérica
    if isinstance(redacao, dict):
        try:
            texto_redacao = " ".join([redacao[k] for k in sorted(redacao.keys(), key=int)])
        except Exception:
            continue
    elif isinstance(redacao, str):
        texto_redacao = redacao
    else:
        continue

    ttr = lexical_diversity(texto_redacao)
    resultados.append({"arquivo": arquivo, "ttr_redacao": round(ttr, 3)})
    ttrs.append(ttr)

# Exibe os resultados
for r in resultados:
    print(f"✅ {r['arquivo']}: TTR = {r['ttr_redacao']}")

# Média de TTR
if ttrs:
    print(f"\n📈 Média de TTR das redações: {mean(ttrs):.3f}")
else:
    print("\nNenhuma redação válida encontrada.")

