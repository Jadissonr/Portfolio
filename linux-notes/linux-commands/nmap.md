# Nmap - Cheatsheet para Análise de Rede

> **AVISO IMPORTANTE**: Os comandos listados neste documento devem ser utilizados APENAS em ambientes autorizados: laboratórios (TryHackMe, HackTheBox), máquinas virtuais pessoais, homelab ou ambientes de teste contratados. Uso não autorizado é ilegal. Sempre tenha permissão explícita antes de escanear qualquer rede ou sistema.

---

## Descoberta de Hosts (Host Discovery / Ping Scan)

Essas técnicas são usadas para identificar quais hosts estão ativos na rede sem fazer um scan de portas completo.

### Ping ICMP Simples
Envia requisições ICMP echo para verificar quais hosts respondem:
```bash
nmap -sn 192.168.1.0/24
```

### Ping com ARP (Mais efetivo em redes locais)
Usa ARP (Address Resolution Protocol) para descobrir hosts na mesma rede — muito mais rápido e preciso em LAN:
```bash
nmap -PR 192.168.1.0/24
```

### Ping com TCP SYN (Porta 80)
Envia pacotes TCP SYN para a porta 80 (HTTP); hosts ativos podem responder mesmo quando bloqueados para ICMP:
```bash
nmap -PS80 192.168.1.0/24
```

### Ping com TCP ACK (Porta 443)
Tenta iniciar conexão TCP na porta 443 (HTTPS); útil quando a porta 80 está filtrada:
```bash
nmap -PA443 192.168.1.0/24
```

### Ping com UDP
Envia pacotes UDP para descobrir hosts; menos confiável que TCP/ICMP mas às vezes passa por filtros:
```bash
nmap -PU53 192.168.1.0/24
```

### Sem Ping (Assume todos os hosts online)
Pula o ping e escaneia diretamente; útil quando o host não responde a ping mas tem portas abertas:
```bash
nmap -Pn 192.168.1.1
```

---

## Escaneamento de Portas (TCP e UDP)

Diferentes técnicas de scan de portas variam em velocidade, sigilo e precisão.

### TCP SYN Scan (Stealth Scan - Padrão)
O mais comum e recomendado. Não completa a conexão TCP (não registra nos logs da aplicação):
```bash
nmap -sS 192.168.1.1
```

### TCP Connect Scan
Completa a conexão TCP inteira (três-way handshake). Mais lento e deixa registros, mas funciona quando SYN não é permitido:
```bash
nmap -sT 192.168.1.1
```

### UDP Scan
Escaneia portas UDP; mais lento que TCP e frequentemente filtrado por firewalls:
```bash
nmap -sU 192.168.1.1
```

### Scan específico de portas
Escaneia apenas as portas listadas em vez de todas (22, 80, 443, 3306, etc.):
```bash
nmap -p 22,80,443,3306 192.168.1.1
```

### Scan de range de portas
Escaneia um intervalo contínuo de portas (1 a 1024):
```bash
nmap -p 1-1024 192.168.1.1
```

### Scan de portas comuns (Top 1000)
Escaneia as 1000 portas mais comuns (padrão do Nmap):
```bash
nmap 192.168.1.1
```

### Scan de todas as portas
Escaneia as 65535 portas (leva tempo, ideal com -T4 ou -T5):
```bash
nmap -p- 192.168.1.1
```

---

## Detecção de Serviço e Versão (-sV)

Identifica não apenas portas abertas, mas também qual serviço está rodando e sua versão.

### Versão simples
Tenta identificar a versão do serviço rodando em cada porta aberta:
```bash
nmap -sV 192.168.1.1
```

### Versão com intensidade alta
Mais agressivo na detecção; testa mais porbes e leva mais tempo, mas é mais preciso:
```bash
nmap -sV --version-intensity 9 192.168.1.1
```

### Versão com intensidade baixa
Mais rápido mas menos preciso; bom para scans iniciais em muitos hosts:
```bash
nmap -sV --version-intensity 2 192.168.1.1
```

---

## Detecção de Sistema Operacional (-O)

Identifica qual sistema operacional está rodando no host baseado em características da pilha TCP/IP.

### OS Detection simples
Tenta adivinhar o SO do alvo:
```bash
nmap -O 192.168.1.1
```

### Requisitos: você precisa de pelo menos uma porta aberta e outra fechada para que funcione adequadamente:
```bash
nmap -O --osscan-guess 192.168.1.1
```

### Combinado com versão
Scan completo de identificação: SO + versão de serviço:
```bash
nmap -A 192.168.1.1
```

---

## Scripts NSE (Nmap Scripting Engine)

O NSE permite executar scripts Lua para enumeração avançada, detecção de vulnerabilidades e coleta de informações.

### Scripts padrão (safe + default)
Executa scripts que são considerados seguros e padrão (não causam danos):
```bash
nmap -sV --script default,safe 192.168.1.1
```

### Scripts de descoberta
Coleta informações adicionais sobre o host (SNMP, DNS, etc.):
```bash
nmap --script discovery 192.168.1.1
```

### Scripts de vulnerabilidade
Tenta identificar vulnerabilidades conhecidas (use com cuidado em prod):
```bash
nmap --script vuln 192.168.1.1
```

### Scripts específicos por categoria
Executa scripts de uma categoria específica (http, ftp, dns, ssh, etc.):
```bash
nmap --script http-title,http-methods 192.168.1.1
```

### Scripts de enumeração HTTP
Útil em reconhecimento de web servers; coleta títulos, métodos HTTP, etc.:
```bash
nmap -p 80,443 --script http-enum,http-title 192.168.1.1
```

### SMB Enumeration (Windows)
Coleta informações via protocolo SMB (NetBIOS, compartilhamentos, contas):
```bash
nmap -p 139,445 --script smb-enum-shares,smb-os-discovery 192.168.1.1
```

### SSH Enumeration
Identifica algoritmos SSH, banner grabbing, versão exata:
```bash
nmap -p 22 --script ssh-hostkey,ssh2-enum-algos 192.168.1.1
```

---

## Timing e Performance (-T0 a -T5, --min-rate)

Controlam a velocidade do scan; crucial para otimizar entre velocidade e detecção de IDS.

### T0 - Paranoid (Muito lento)
Intervalo de 5 minutos entre pacotes; praticamente indetectável mas impraticável em redes grandes:
```bash
nmap -T0 192.168.1.1
```

### T1 - Sneaky (Lento)
Ativo contra IDS/IPS; mais lento que o normal, intervalo de 15 segundos entre pacotes:
```bash
nmap -T1 192.168.1.1
```

### T2 - Polite (Normal com consideração)
Reduz carga na rede; bom para redes de produção onde você quer evitar impacto:
```bash
nmap -T2 192.168.1.1
```

### T3 - Normal (Padrão)
Comportamento padrão do Nmap; equilíbrio entre velocidade e confiabilidade:
```bash
nmap -T3 192.168.1.1
```

### T4 - Aggressive (Rápido)
Aumenta velocidade significativamente; bom para redes internas ou rápidas:
```bash
nmap -T4 192.168.1.1
```

### T5 - Insane (Muito rápido)
Máxima velocidade; assume rede de alta velocidade, pode perder informações:
```bash
nmap -T5 192.168.1.1
```

### Min-rate (Pacotes mínimos por segundo)
Define uma taxa mínima de pacotes/segundo; garante velocidade mínima:
```bash
nmap --min-rate 100 192.168.1.1
```

### Max-rate (Pacotes máximos por segundo)
Limita a quantidade de pacotes/segundo; útil para não sobrecarregar a rede:
```bash
nmap --max-rate 50 192.168.1.1
```

---

## Formatos de Saída (-o*)

Diferentes formatos para armazenar resultados do scan para análise posterior.

### Normal (Saída em texto padrão)
Salva a saída padrão do Nmap em arquivo de texto:
```bash
nmap 192.168.1.1 -oN resultado.txt
```

### XML (Extensible Markup Language)
Formato estruturado, ideal para parsing e integração com outras ferramentas:
```bash
nmap 192.168.1.1 -oX resultado.xml
```

### Grepable (Formato simplificado)
Formato otimizado para buscar com grep; útil em análise rápida via linha de comando:
```bash
nmap 192.168.1.1 -oG resultado.gnmap
```

### All formats (-oA)
Salva em todos os formatos (N, X, G) simultaneamente:
```bash
nmap 192.168.1.1 -oA resultado
```

---

## Técnicas de Evasão de Firewall/IDS

Métodos para contornar sistemas de detecção e filtragem de pacotes.

### Fragmentação de pacotes
Divide os pacotes em fragmentos pequenos para evitar detecção de padrões:
```bash
nmap -f 192.168.1.1
```

### Fragmentação extra (mais agressiva)
Fragmentação com tamanho menor (MTU de 8 bytes):
```bash
nmap --mtu 8 192.168.1.1
```

### Decoy (Iscas)
Envia pacotes de vários endereços IP falsificados para confundir o IDS:
```bash
nmap -D RND:10 192.168.1.1
```

### Source Port spoofing
Faz parecer que o tráfego vem de uma porta legítima (ex: 53 - DNS):
```bash
nmap --source-port 53 192.168.1.1
```

### Data randomization
Preenche os pacotes com dados aleatórios para evitar assinaturas conhecidas:
```bash
nmap --data-length 25 192.168.1.1
```

### Null, FIN, Xmas Scans (TCP sem bandeira SYN)
Técnicas alternativas de varredura que não usam SYN; passam por alguns firewalls:
```bash
nmap -sN 192.168.1.1  # Null Scan
nmap -sF 192.168.1.1  # FIN Scan
nmap -sX 192.168.1.1  # Xmas Scan
```

### Idle/Zombie Scan
Usa um host terceiro inativo para fazer o scan; muito furtivo mas lento:
```bash
nmap -sI 192.168.1.100 192.168.1.1
```

---

## Combos Úteis

Comandos que combinam múltiplas flags para criar scans práticos e eficientes.

### Reconhecimento Rápido (Blue Team - Primeiro passo)
Scan rápido com detecção de versão, scripts padrão e timing agressivo:
```bash
nmap -sV --script default,safe -T4 192.168.1.0/24 -oA scan_rapido
```

### Scan Completo (Análise profunda de um host)
Detecção de SO, versão de serviço, scripts de descoberta e all ports:
```bash
nmap -A -p- --script discovery,vuln -T3 192.168.1.1 -oX scan_completo.xml
```

### Enumeração Windows (SMB/NetBIOS)
Focado em hosts Windows para coleta de informações de compartilhamentos e versão:
```bash
nmap -p 135,139,445 --script smb-enum-shares,smb-os-discovery -sV 192.168.1.0/24 -oN enum_windows.txt
```

### Scan Furtivo com Timing Lento (Evasão de IDS)
Combina fragmentação, decoy e timing paranóico para máxima discrição:
```bash
nmap -f -D RND:5 -T1 --scan-delay 2s 192.168.1.1 -oG scan_furtivo.gnmap
```

---

## Dicas Gerais

- **Sempre salve seus resultados**: Use `-oA` para ter os dados em múltiplos formatos
- **Teste primeiro com -Pn** se o host parecer offline mas você sabe que está ativo
- **Use --top-ports para scans rápidos**: `nmap --top-ports 100 target`
- **Combine -A com -T4** para reconhecimento rápido mas completo
- **Mantenha NSE scripts atualizados**: `nmap --script-updatedb`
- **Em redes internas, -sS é sempre preferível**: Mais rápido e mais sigiloso que -sT
