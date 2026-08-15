#!/usr/bin/env python3
"""
TryHackMe Progress Tracker
---------------------------
Busca as salas concluidas no TryHackMe (via API nao-oficial de perfil publico)
e atualiza automaticamente o arquivo progresso-geral.md do portfolio no GitHub.

IMPORTANTE - leia antes de usar:
- Essa API NAO e oficial/documentada pela TryHackMe. Pode quebrar sem aviso
  se eles mudarem a estrutura interna do site.
- O endpoint usado e de "perfil publico". Seu perfil TryHackMe precisa estar
  configurado como publico (Configuracoes > Privacidade) para funcionar
  sem autenticacao.

Como achar seu nome de usuario:
- E o mesmo username que voce usa para logar no TryHackMe (aparece na URL
  do seu perfil: https://tryhackme.com/p/SEU_USUARIO)
"""

import os
import sys
import json
import re
import time
from datetime import datetime
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

THM_USERNAME = os.environ.get("THM_USER_HASH", "")  # nome da env var mantido por compatibilidade

API_URL = "https://tryhackme.com/api/v2/public-profile/completed-rooms"
OUTPUT_FILE = "ctf-writeups/tryhackme/progresso-geral.md"
MAX_TENTATIVAS = 5
ESPERA_BASE_SEGUNDOS = 20

# Salas que ja tem write-up completo dedicado (link em vez de so o resumo)
SALAS_COM_WRITEUP = {
    "ninjaskills": ("Ninja Skills", "./ninja-skills/"),
    "disgruntled": ("Disgruntled", "./disgruntled/"),
}


def requisitar_com_retry(url, headers):
    """Faz a requisicao HTTP, tentando de novo com espera crescente se vier 429."""
    for tentativa in range(1, MAX_TENTATIVAS + 1):
        req = Request(url, headers=headers)
        try:
            with urlopen(req, timeout=15) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except HTTPError as e:
            if e.code == 429 and tentativa < MAX_TENTATIVAS:
                espera = ESPERA_BASE_SEGUNDOS * tentativa
                print(f"Recebido 429 (rate limit). Tentativa {tentativa}/{MAX_TENTATIVAS}. "
                      f"Aguardando {espera}s antes de tentar de novo...")
                time.sleep(espera)
                continue
            print(f"ERRO HTTP {e.code} ao consultar a API. "
                  f"Verifique se o username esta certo e se o perfil e publico.")
            sys.exit(1)
        except URLError as e:
            print(f"ERRO de rede: {e}")
            sys.exit(1)

    print("ERRO: numero maximo de tentativas excedido (rate limit persistente).")
    sys.exit(1)


def buscar_salas_completas():
    """Busca todas as paginas de salas concluidas via API publica."""
    if not THM_USERNAME:
        print("ERRO: variavel de ambiente THM_USER_HASH nao definida (deve conter seu username).")
        sys.exit(1)

    todas_salas = []
    pagina = 1
    limite = 50

    while True:
        url = f"{API_URL}?username={THM_USERNAME}&limit={limite}&page={pagina}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json",
        }

        dados = requisitar_com_retry(url, headers)

        # A resposta pode vir como lista direta ou dentro de uma chave "data"/"rooms"
        lote = dados if isinstance(dados, list) else dados.get("data") or dados.get("rooms") or []

        if not lote:
            break

        todas_salas.extend(lote)

        if len(lote) < limite:
            break
        pagina += 1

    return todas_salas


def normalizar_sala(sala):
    """Extrai titulo, codigo e data de conclusao, cobrindo variacoes de nome de campo."""
    titulo = sala.get("title") or sala.get("roomTitle") or sala.get("name") or "Sala sem nome"
    codigo = sala.get("code") or sala.get("roomCode") or sala.get("id") or ""
    data_bruta = (
        sala.get("completedAt")
        or sala.get("dateCompleted")
        or sala.get("timeCompleted")
        or sala.get("date")
    )

    data_formatada = "?"
    if data_bruta:
        try:
            dt = datetime.fromisoformat(str(data_bruta).replace("Z", "+00:00"))
            data_formatada = dt.strftime("%d/%m/%Y")
        except ValueError:
            data_formatada = str(data_bruta)[:10]

    return titulo, codigo, data_formatada


def gerar_markdown(salas):
    """Monta a tabela markdown final, ordenada da mais recente para a mais antiga."""
    linhas_processadas = []
    for sala in salas:
        titulo, codigo, data = normalizar_sala(sala)
        codigo_normalizado = re.sub(r"[^a-z0-9]", "", codigo.lower())

        resumo = titulo
        if codigo_normalizado in SALAS_COM_WRITEUP:
            nome_link, caminho = SALAS_COM_WRITEUP[codigo_normalizado]
            resumo = f"{titulo} — [ver write-up completo]({caminho})"

        linhas_processadas.append((data, titulo, resumo))

    # Ordena por data desc (strings "?" ficam por ultimo)
    linhas_processadas.sort(key=lambda x: x[0] if x[0] != "?" else "0", reverse=True)

    cabecalho = (
        "> 📋 Lista de progresso — salas concluídas no TryHackMe, atualizada "
        "automaticamente via GitHub Actions.\n"
        "> Para desafios com raciocínio técnico aprofundado, veja os write-ups "
        "completos nas pastas dedicadas (ex: `ninja-skills/`, `disgruntled/`).\n\n"
        f"_Última atualização: {datetime.now().strftime('%d/%m/%Y %H:%M')}_\n\n"
    )

    tabela = "| Data | Sala | Resumo |\n|---|---|---|\n"
    for data, titulo, resumo in linhas_processadas:
        tabela += f"| {data} | {titulo} | {resumo} |\n"

    return cabecalho + tabela


def main():
    salas = buscar_salas_completas()
    if not salas:
        print("Nenhuma sala encontrada. Verifique o THM_USER_HASH e a privacidade do perfil.")
        sys.exit(1)

    markdown = gerar_markdown(salas)

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(markdown)

    print(f"OK: {len(salas)} salas processadas. Arquivo atualizado em {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
