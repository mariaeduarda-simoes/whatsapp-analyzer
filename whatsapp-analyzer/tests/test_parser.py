from app.parser import juntar_mensagens, ler_conversa, separar_linha

CONVERSA = """15/11/2026 08:12 - As mensagens são protegidas com criptografia.
15/11/2026 08:12 - Ana: Bom dia!
15/11/2026 12:41 - Bruno: Olha esse meme
que eu achei agora
15/11/2026 12:50 - Ana: Kkkk muito bom"""


def test_separar_linha_normal():
    resultado = separar_linha("15/11/2026 08:15 - Bruno: Bom dia!")
    assert resultado["autor"] == "Bruno"
    assert resultado["mensagem"] == "Bom dia!"
    assert resultado["hora"] == "08:15"


def test_separar_linha_de_sistema_nao_tem_autor():
    resultado = separar_linha("15/11/2026 08:12 - Mensagens protegidas")
    assert resultado["autor"] is None


def test_linha_de_continuacao_devolve_none():
    assert separar_linha("que eu achei agora") is None


def test_mensagem_de_varias_linhas_fica_junta():
    mensagens = juntar_mensagens(CONVERSA.splitlines())
    meme = mensagens[2]["mensagem"]
    assert meme == "Olha esse meme\nque eu achei agora"


def test_tabela_sem_mensagens_de_sistema():
    df = ler_conversa(CONVERSA)
    assert len(df) == 3
    assert set(df["autor"]) == {"Ana", "Bruno"}


def test_texto_vazio_devolve_tabela_vazia():
    df = ler_conversa("")
    assert df.empty
