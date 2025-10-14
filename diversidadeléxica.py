import re

def tokenize(text):
    """
    Transforma o texto em uma lista de palavras (tokens),
    removendo pontuação e convertendo tudo para minúsculas.
    """
    text = text.lower()
    tokens = re.findall(r'\b\w+\b', text, flags=re.UNICODE)
    return tokens

def lexical_diversity(text):
    """
    Calcula a diversidade léxica (TTR = tipos / tokens).
    Retorna um número entre 0 e 1.
    """
    tokens = tokenize(text)
    if not tokens:
        return 0.0
    types = set(tokens)
    return len(types) / len(tokens)

# Exemplo de uso:
if __name__ == "__main__":
    redacao = input("Digite a redação do aluno:\n")
    diversidade = lexical_diversity(redacao)
    print(f"\nDiversidade léxica (TTR): {diversidade:.3f}")
