> ⚠️ Write-up focado em metodologia. Respostas específicas omitidas conforme boas práticas e termos de uso da plataforma.

# TryHackMe — Disgruntled

**Categoria:** Forense em Linux (DFIR)
**Dificuldade:** Easy
**Link da sala:** https://tryhackme.com/room/disgruntled

## Cenário

Um funcionário de TI foi preso por suspeita de phishing. A tarefa é investigar a última máquina em que ele trabalhou para identificar ações suspeitas e determinar se há algo com que a empresa precise se preocupar.

## Metodologia

Investigação conduzida via análise de logs do systemd (`journalctl`) e histórico de comandos do usuário (`.bash_history`), sem interface gráfica — abordagem típica de forense em ambientes Linux comprometidos.

### 1. Comandos privilegiados

```bash
journalctl _COMM=sudo
```

Esse filtro retorna especificamente os registros de execução via `sudo`, permitindo reconstruir uma timeline de ações privilegiadas sem vasculhar o log inteiro do sistema. A partir dele identifiquei um pacote instalado fora do escopo esperado de trabalho do funcionário — primeiro sinal de algo fora do padrão.

### 2. Criação de um novo usuário

Continuando a análise do mesmo log, identifiquei a criação de um novo usuário logo após a instalação do pacote, e o momento exato em que ele recebeu privilégios de `sudo` — a edição do `/etc/sudoers` (via `visudo`) fica registrada no log, permitindo cravar o timestamp exato da escalada.

O mesmo log mostrou também a abertura de um script suspeito no editor `vi`.

### 3. Um arquivo que não existia mais

O script identificado na etapa anterior já não existia mais no sistema no momento da investigação. Para reconstruir origem e destino, recorri ao histórico de comandos do usuário criado:

```bash
cat /home/<usuario>/.bash_history
```

Isso permitiu identificar o `curl` usado para baixar o script de um servidor externo, e o comando usado em seguida para renomeá-lo e movê-lo — técnica clássica de disfarce, dando ao arquivo um nome que parece legítimo.

Com o novo caminho em mãos:

```bash
stat <caminho_do_arquivo>   # confirma a última modificação
cat <caminho_do_arquivo>    # revela o conteúdo do script
```

O conteúdo mostrou que o script, ao ser executado, geraria evidência de sua própria execução — indício claro de comportamento malicioso/destrutivo.

### 4. Agendamento via crontab

Faltava saber quando o script seria executado. A resposta estava no `crontab` do usuário, mas a expressão cron não deixa óbvio o horário real.

**Dificuldade:** converter a expressão cron para um horário legível não é intuitivo.
**Solução:** com ajuda da IA integrada do TryHackMe, encontrei o [crontab.guru](https://crontab.guru), que traduz expressões cron em horário/frequência real.

## Ferramentas e comandos

| Comando/Ferramenta | Função |
|---|---|
| `journalctl _COMM=sudo` | Listar comandos executados com privilégios elevados |
| `.bash_history` | Reconstruir a sequência de comandos do usuário investigado |
| `stat` | Verificar data de modificação de um arquivo |
| `cat` | Ler conteúdo de logs e scripts |
| [crontab.guru](https://crontab.guru) | Converter expressão cron em horário real |

## Aprendizados

- `journalctl` com filtro `_COMM=` isola ações privilegiadas em meio a um log grande e ruidoso.
- `.bash_history` + `stat` + `cat` reconstroem boa parte de uma timeline de incidente, mesmo com o artefato original já removido.
- Renomear um script para um nome "inofensivo" é uma técnica simples de disfarce — reforça checar histórico de comandos, não só o estado atual do sistema.
- Ferramentas simples e específicas (como o crontab.guru) resolvem gargalos pontuais mais rápido do que insistir em interpretar manualmente uma sintaxe pouco intuitiva.
