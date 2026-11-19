import re
import pandas as pd

# Padrão de uma linha do WhatsApp: 15/11/2026 08:15 - Bruno: Bom dia!
PADRAO = re.compile(r"^(\d{2}/\d{2}/\d{4}) (\d{2}:\d{2}) - (.*)$")


def separar_linha(linha):
    """Separa uma linha em data, hora, autor e mensagem.
    Devolve None se a linha não começar com data (continuação de mensagem)."""
    achou = PADRAO.match(linha)
    if not achou:
        return None

    data, hora, resto = achou.groups()

    if ": " in resto:
        autor, mensagem = resto.split(": ", 1)
    else:
        # Mensagem de sistema (sem autor)
        autor, mensagem = None, resto

    return {"data": data, "hora": hora, "autor": autor, "mensagem": mensagem}


def juntar_mensagens(linhas):
    """Cria a lista de mensagens, juntando as que ocupam várias linhas."""
    mensagens = []
    for linha in linhas:
        item = separar_linha(linha)
        if item:
            mensagens.append(item)
        elif mensagens:
            mensagens[-1]["mensagem"] += "\n" + linha
    return mensagens


def montar_tabela(mensagens):
    """Transforma a lista de mensagens em uma tabela do pandas."""
    colunas = ["autor", "mensagem", "data_hora"]
    if not mensagens:
        return pd.DataFrame(columns=colunas)

    df = pd.DataFrame(mensagens)
    df["data_hora"] = pd.to_datetime(
        df["data"] + " " + df["hora"], format="%d/%m/%Y %H:%M"
    )
    df = df.drop(columns=["data", "hora"])
    df = df[df["autor"].notna()]  # tira mensagens de sistema
    return df


def ler_conversa(texto):
    """Recebe o texto inteiro da conversa e devolve a tabela pronta."""
    linhas = texto.splitlines()
    mensagens = juntar_mensagens(linhas)
    return montar_tabela(mensagens)


def ler_arquivo(caminho):
    """Lê um arquivo .txt do computador e devolve a tabela pronta."""
    with open(caminho, encoding="utf-8") as f:
        return ler_conversa(f.read())


if __name__ == "__main__":
    df = ler_arquivo("exemplos/conversa_teste.txt")
    print(df.to_string())
    print(df.shape)
