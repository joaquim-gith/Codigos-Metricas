# -*- coding: utf-8 -*-
import os
import re
import json
import statistics

def natural_sort_key(texto):

    #Resolve o problema de 97,98,99,9,100
    import re
    return [int(c) if c.isdigit() else c for c in re.split(r'(\d+)', texto)]


# Silabificação
VOWELS = set("aeoáéóíúãõâêôàü")

def _is_vowel(w: str, i: int) -> bool:
    if i >= len(w): return False
    c = w[i]
    if c in VOWELS: return True
    if c in "iu":
        prev = i > 0 and _is_vowel(w, i - 1)
        nxt = i + 1 < len(w) and _is_vowel(w, i + 1)
        return not (prev or nxt)
    return False

def word2syllables(w: str):
    w = w.strip().lower()
    if not w or len(w) == 1:
        return [w] if w else []
    vowels = [i for i in range(len(w)) if _is_vowel(w, i)]
    if not vowels:
        return [w]
    syllables = []
    start = 0
    for i, v in enumerate(vowels):
        if i == len(vowels) - 1:
            end = len(w) - 1
        else:
            next_v = vowels[i + 1]
            cons = next_v - v - 1
            end = v if cons <= 1 else v + cons // 2
        syllables.append(w[start:end + 1])
        start = end + 1
    return syllables

def extrair_palavras(texto):
    if not texto or not texto.strip():
        return []
    return re.findall(r'\b[a-zA-ZÀ-ÿ]{3,}\b', texto.lower())

def calcular_ttr_silabico(texto):
    palavras = extrair_palavras(texto)
    if not palavras:
        return 0.0

    todas_silabas = []
    for palavra in palavras:
        try:
            silabas = word2syllables(palavra)
            todas_silabas.extend(silabas)
        except:
            continue

    if not todas_silabas:
        return 0.0

    return len(set(todas_silabas)) / len(todas_silabas)


#Leitura dos datasets


def processar_data():
    PASTA = "Data"
    if not os.path.isdir(PASTA):
        print(f" Pasta 'Data' não encontrada.")
        return []

    subpastas = [d for d in os.listdir(PASTA) if os.path.isdir(os.path.join(PASTA, d))]
    subpastas.sort(key=natural_sort_key)  #Ordenação numérica correta
    
    ttrs = []
    print("\n COMANDOS ORIGINAIS (Data)")
    
    for subpasta in subpastas:
        xml_path = os.path.join(PASTA, subpasta, "prompt.xml")
        if not os.path.isfile(xml_path):
            continue

        try:
            with open(xml_path, "r", encoding="utf-8") as f:
                conteudo = f.read()
            match = re.search(r"<body>(.*?)</body>", conteudo, re.DOTALL | re.IGNORECASE)
            if not match:
                continue
            body = match.group(1).strip()
            if not body:
                continue

            ttr = calcular_ttr_silabico(body)
            if ttr > 0:
                print(f"{subpasta:<20} → TTR: {ttr:.4f}")
                ttrs.append(ttr)
        except:
            continue

    return ttrs

def processar_qwenmax():
    PASTA = "QwenMax"
    if not os.path.isdir(PASTA):
        print(f" Pasta 'QwenMax' não foi encontrada.")
        return []

    json_files = [f for f in os.listdir(PASTA) if f.endswith(".json")]
    json_files.sort(key=natural_sort_key)  #Ordenação numérica correta
    
    ttrs = []
    print("\n COMANDOS SINTÉTICOS (QwenMax)")
    
    for arquivo in json_files:
        caminho = os.path.join(PASTA, arquivo)
        try:
            with open(caminho, "r", encoding="utf-8") as f:
                dados = json.load(f)
            
            if "comando_tematico" in dados and isinstance(dados["comando_tematico"], dict):
                comandos = list(dados["comando_tematico"].values())
            elif isinstance(dados, dict) and all(isinstance(v, str) for v in dados.values()):
                comandos = list(dados.values())
            elif isinstance(dados, list):
                comandos = dados
            else:
                continue

            for i, cmd in enumerate(comandos):
                if not isinstance(cmd, str):
                    continue
                cmd = cmd.strip()
                if not cmd:
                    continue
                ttr = calcular_ttr_silabico(cmd)
                if ttr > 0:
                    nome_exibicao = f"{arquivo}#{i}"
                    print(f"{nome_exibicao:<20} → TTR: {ttr:.4f}")
                    ttrs.append(ttr)

        except Exception as e:
            continue

    return ttrs

#Execução principal

def main():
    print("Métrica de Diversidade Lexical")
    
    ttrs_originais = processar_data()
    ttrs_sinteticos = processar_qwenmax()

    print("\n" + "="*60)
    print(" ESTATÍSTICAS – Dataset Data")
    print("="*60)
    if ttrs_originais:
        media = statistics.mean(ttrs_originais)
        desvio = statistics.stdev(ttrs_originais) if len(ttrs_originais) > 1 else 0.0
        print(f"Média do TTR:   {media:.4f}")
        print(f"Desvio padrão:  {desvio:.4f}")
    else:
        print("Nenhum comando original processado.")

    print("\n" + "="*60)
    print("ESTATÍSTICAS – Dataset QwenMax")
    print("="*60)
    if ttrs_sinteticos:
        media = statistics.mean(ttrs_sinteticos)
        desvio = statistics.stdev(ttrs_sinteticos) if len(ttrs_sinteticos) > 1 else 0.0
        print(f"Média do TTR:   {media:.4f}")
        print(f"Desvio padrão:  {desvio:.4f}")
    else:
        print("Nenhum comando sintético processado.")

if __name__ == "__main__":
    main()
