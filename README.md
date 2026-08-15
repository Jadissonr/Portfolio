# 🤖 TryHackMe Progress Tracker

Automação que busca as salas concluídas no TryHackMe e atualiza sozinha o arquivo
`ctf-writeups/tryhackme/progresso-geral.md` do portfólio, toda semana, via GitHub Actions.

> ⚠️ Usa uma API não-oficial da TryHackMe (engenharia reversa feita pela comunidade,
> não documentada nem suportada oficialmente). Pode parar de funcionar sem aviso se
> a TryHackMe mudar algo internamente — nesse caso, é só ajustar o script.

## Como funciona

```
GitHub Actions (agendado toda segunda) 
        → roda fetch_progress.py 
        → busca salas concluídas na API pública do seu perfil THM 
        → gera a tabela em progresso-geral.md 
        → commita e faz push automaticamente, só se algo mudou
```

## Passo 1 — Deixe seu perfil TryHackMe público

Vá em **Configurações → Privacidade** no TryHackMe e marque o perfil como público.
Isso evita precisar guardar cookie de sessão (mais simples e mais seguro).

## Passo 2 — Encontre seu THM_USER_HASH

1. Abra `https://tryhackme.com/p/SEU_USUARIO` no navegador
2. Abra o **DevTools** (`F12`) → aba **Network**
3. Recarregue a página (`F5`)
4. Procure uma requisição pra `completed-rooms` na lista de requisições
5. Copie o valor do parâmetro `?user=XXXXXXXX` da URL — esse é seu hash

## Passo 3 — Configure o Secret no GitHub

No seu repositório do portfólio:

1. Vá em **Settings → Secrets and variables → Actions**
2. Clique em **New repository secret**
3. Nome: `THM_USER_HASH`
4. Valor: o hash que você copiou no Passo 2
5. (Só se seu perfil for **privado**) Adicione também um secret `THM_COOKIE` com
   o valor do cookie `connect.sid` da sua sessão logada — **nunca** coloque isso
   direto no código

## Passo 4 — Copie os arquivos pro seu repositório

```
seu-portfolio/
├── fetch_progress.py
└── .github/
    └── workflows/
        └── update-progress.yml
```

## Passo 5 — Teste manualmente

Na aba **Actions** do seu repositório no GitHub, selecione o workflow
"Atualizar progresso do TryHackMe" e clique em **Run workflow** pra testar
sem esperar a segunda-feira.

## Manutenção

Como a API não é oficial, se o script parar de funcionar (erro HTTP ou lista vazia):
1. Repita o Passo 2 pra confirmar se o endpoint/estrutura mudou
2. Abra o DevTools de novo e compare o JSON retornado com os nomes de campo
   usados na função `normalizar_sala()` do script — ajuste se necessário
