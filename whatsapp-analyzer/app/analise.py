import re
from collections import Counter

# Palavras que não queremos contar
IGNORAR = {"mídia", "oculta", "mensagem", "apagada"}


def mensagens_por_autor(df):
    contagem = df["autor"].value_counts()
    return {autor: int(total) for autor, total in contagem.items()}


def horario_de_pico(df):
    horas = df["data_hora"].dt.hour
    return int(horas.value_counts().idxmax())


def mensagens_por_mes(df):
    meses = df["data_hora"].dt.strftime("%Y-%m")
    contagem = meses.value_counts().sort_index()
    return {mes: int(total) for mes, total in contagem.items()}


def palavras_mais_usadas(df, quantidade=5):
    contador = Counter()
    for mensagem in df["mensagem"]:
        palavras = re.findall(r"\w+", mensagem.lower())
        for palavra in palavras:
            if len(palavra) >= 4 and palavra not in IGNORAR:
                contador[palavra] += 1
    return [
        {"palavra": palavra, "vezes": vezes}
        for palavra, vezes in contador.most_common(quantidade)
    ]


def mensagens_por_hora(df):
    """Usado no gráfico: quantas mensagens em cada hora do dia (0 a 23)."""
    contagem = df["data_hora"].dt.hour.value_counts()
    return {hora: int(contagem.get(hora, 0)) for hora in range(24)}


def estatisticas(df):
    """Junta todas as estatísticas em um único resultado."""
    return {
        "total_mensagens": int(len(df)),
        "mensagens_por_autor": mensagens_por_autor(df),
        "horario_de_pico": horario_de_pico(df),
        "mensagens_por_mes": mensagens_por_mes(df),
        "palavras_mais_usadas": palavras_mais_usadas(df),
    }
