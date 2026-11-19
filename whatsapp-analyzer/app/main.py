import io

import matplotlib
matplotlib.use("Agg")  # permite gerar gráfico sem abrir janela
import matplotlib.pyplot as plt
from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.responses import Response

from app.analise import estatisticas, mensagens_por_hora
from app.parser import ler_conversa

app = FastAPI(
    title="WhatsApp Analyzer",
    description="Envie uma conversa exportada do WhatsApp (.txt) e receba estatísticas.",
)


async def ler_tabela_do_arquivo(arquivo):
    """Lê o arquivo enviado e devolve a tabela. Dá erro se estiver vazio."""
    conteudo = await arquivo.read()
    texto = conteudo.decode("utf-8")
    df = ler_conversa(texto)
    if df.empty:
        raise HTTPException(
            status_code=400,
            detail="Nenhuma mensagem encontrada. Envie um .txt exportado do WhatsApp.",
        )
    return df


@app.get("/saude")
def saude():
    return {"status": "ok"}


@app.post("/analisar")
async def analisar(arquivo: UploadFile):
    df = await ler_tabela_do_arquivo(arquivo)
    return estatisticas(df)


@app.post("/grafico/horarios")
async def grafico_horarios(arquivo: UploadFile):
    df = await ler_tabela_do_arquivo(arquivo)
    dados = mensagens_por_hora(df)

    plt.figure(figsize=(8, 4))
    plt.bar(list(dados.keys()), list(dados.values()))
    plt.title("Mensagens por horário")
    plt.xlabel("Hora do dia")
    plt.ylabel("Quantidade de mensagens")
    plt.xticks(range(0, 24, 2))

    imagem = io.BytesIO()
    plt.savefig(imagem, format="png")
    plt.close()

    return Response(content=imagem.getvalue(), media_type="image/png")
