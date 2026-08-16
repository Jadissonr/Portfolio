> ⚠️ Write-up focado em metodologia de investigação. Respostas específicas e indicadores de solução foram omitidos conforme boas práticas e termos de uso da plataforma.

# TryHackMe — Investigating Windows

**Categoria:** Forense / Blue Team  
**Dificuldade:** Easy / Intermediário  
**Link da sala:** https://tryhackme.com/room/investigatingwindows

## Cenário

A sala simula um ambiente Windows comprometido, no qual o objetivo é reconstruir a atividade maliciosa usando dados locais do sistema, registros do evento e configurações de segurança. Em vez de focar apenas em uma resposta pronta, a investigação se torna um exercício de análise de evidências: o que foi alterado, quando, por quem e quais elementos mostram que a máquina foi usada de forma suspeita.

## Objetivo da investigação

Eles não pedem apenas "encontrar um indicador"; a tarefa é reconstruir uma narrativa de incidentes em um host Windows. Isso envolve verificar:

- a versão do sistema e contexto do host;
- contas locais e acessos adicionados;
- eventos de autenticação, criação de usuários e ações administrativas;
- tarefas agendadas que sugerem persistência;
- regras de firewall que abrem conexões suspeitas;
- alterações no arquivo de hosts que direcionam tráfego para endereços maliciosos;
- sinais de atividade que não parecem consistentes com o uso legítimo da máquina.

## Metodologia

### 1. Confirmar a base do sistema: `winver`

O primeiro passo foi verificar a versão exata do Windows e o build do sistema. Isso parece simples, mas é importante porque ajuda a entender o contexto da máquina e quais recursos ou caminhos esperados devem estar presentes.

Em ambientes Windows, o comando `winver` é rápido e útil para confirmar:

- edição do sistema operacional;
- versão do Windows;
- build do sistema;
- se o host provavelmente está em um ambiente corporativo ou de usuário final.

Mesmo sendo uma etapa inicial, ela ajuda a responder perguntas como: "é um sistema antigo, mais vulnerável?" ou "há recursos específicos que o atacante usou para sobreviver ao ambiente?".

### 2. Revisar usuários locais com `net user` no PowerShell

Depois de validar a base do sistema, a investigação passou para o que é mais importante em um sistema comprometido: contas locais e usuários. O comando é simples, mas extremamente útil.

No PowerShell, executei:

```powershell
net user
```

Esse comando lista os usuários do sistema e ajuda a detectar:

- contas novas ou inesperadas;
- usuários com nome semelhante a serviços ou perfis suspeitos;
- contas que foram criadas no momento do comprometimento;
- diferenças entre contas administrativas e contas do cotidiano.

Também vale verificar contas específicas:

```powershell
net user <usuario>
```

Isso mostra detalhes como:

- grupo ao qual pertence;
- status da conta;
- se a conta está habilitada ou desabilitada;
- privilégios e participação em grupos administrativos.

No contexto de forense e blue team, a análise de contas locais é uma das formas mais diretas de perceber se houve criação de um usuário para persistência ou uso remoto.

### 3. Verificar contas e grupos com `lusrmgr.msc`

Em seguida, passei para a ferramenta de gerenciamento local de usuários e grupos:

```text
lusrmgr.msc
```

Ela expande o que `net user` mostra e ajuda a revisar a estrutura de identidade do host. A análise aqui fica mais clara quando se busca:

- usuários criados recentemente;
- contas adicionadas ao grupo Administradores;
- grupos com privilégios anômalos;
- contas sem propósito claro para o ambiente;
- relações que sugiram escalada de privilégio ou persistência.

Essa etapa é especialmente importante porque, em muitos cenários, o atacante não tenta "esconder" um abuso; ele apenas cria uma conta nova e a coloca em um grupo de privilégios, deixando uma evidência muito clara para quem investiga o endpoint.

### 4. Checar eventos de segurança no Event Viewer

A parte mais importante da investigação foi a análise dos logs do sistema via Event Viewer. Essa ferramenta permite reconstruir uma linha do tempo dos eventos importantes do Windows.

Acessando:

```text
eventvwr.msc
```

Foi necessário focar em logs como:

- Windows Logs > Security
- Windows Logs > System
- Applications and Services Logs

Dentro do Security Log, procurei por indicadores como:

- sucessos e falhas de login;
- criação de contas;
- alteração de permissões;
- reinicializações e desligamentos;
- uso de contas administrativas;
- eventos relacionados a serviços e execução remota.

Sinais típicos de atividade suspeita incluem:

- logons usando contas pouco comuns;
- acessos fora do horário normal;
- tentativas de login repetidas;
- criação de usuário seguida de acesso administrativo;
- execução de ações sem contexto de rotina.

Sem a linha do tempo dos eventos, uma máquinaWindows comprometida vira um conjunto de artefatos desconexos. O Event Viewer é o que transforma isso em uma investigação coerente.

### 5. Inspecionar tarefas agendadas: Agendador de Tarefas

Uma vez que o sistema mostrou sinais de alteração, a próxima camada foi o Agendador de Tarefas. O objetivo era procurar persistência: ações que continuam rodando mesmo após o usuário sair da sessão.

A ferramenta pode ser aberta por:

```text
taskschd.msc
```

A análise foi focada em:

- tarefas criadas por usuários desconhecidos;
- execução em intervalos estranhos ou fora de rotina;
- programas apontando para locais fora do padrão;
- tasks executadas em contexto de sistema ou com privilégios elevados;
- caminhos como `AppData`, `Temp`, `Downloads` ou pastas pouco usuais.

Essa etapa é importante porque persistência não é sempre um processo rodando à toa. Na prática, o atacante costuma criar uma tarefa para reexecutar um payload em horários previsíveis. Isso é uma das evidências mais fortes de que a máquina foi explorada e que a atividade não foi apenas um teste casual.

### 6. Revisar regras de Firewall do Windows

A próxima etapa foi verificar se o host tinha regras novas ou permissivas no firewall. O Windows Firewall é uma fonte valiosa de evidência porque pode revelar:

- portas abertas inesperadas;
- serviços expostos para acesso remoto;
- regras criadas para permitir comunicação com domínio suspeito;
- atividade que só faria sentido em um cenário de persistência ou exfiltração.

A ferramenta pode ser aberta com:

```text
wf.msc
```

Também é útil revisar regras de firewall em linha de comando, quando precisa de uma visão mais completa:

```powershell
netsh advfirewall firewall show rule name=all
```

Entre os pontos que procurei, estavam:

- regras novas sem justificativa;
- portas incomuns ou fora do padrão da máquina;
- portas para serviços de administração ou acesso remoto sem necessidade;
- regras que permitiam comunicação de saída ou entrada para IPs ou domínios suspeitos.

Isso ajuda a responder se a máquina foi usada como ponto de entrada, serviço acessível ou canal de saída para comando e controle.

### 7. Inspecionar o arquivo `hosts`

O arquivo `hosts` costuma passar despercebido, mas em investigações de endpoint ele é muito relevante. Ele define mapeamentos de nomes para IPs e pode ser usado para redirecionar tráfego ou ocultar domínios maliciosos.

O caminho geralmente é:

```text
C:\Windows\System32\drivers\etc\hosts
```

Ao analisar esse arquivo, procurei por:

- entradas de domínio estranhas;
- redirecionamentos para `127.0.0.1` ou IPs locais;
- domínios que apontam para endereços de servidores externos ou de controle;
- nomes que não fazem parte da infraestrutura real da máquina.

Esse tipo de alteração é interessante porque não depende de software externo; basta um arquivo local para tornar a máquina capaz de resolver nomes de forma manipulada, influenciando o comportamento do sistema e criando um canal de persistência ou desvio de tráfego.

## Ferramentas e comandos de referência

| Comando/Ferramenta | Função |
|---|---|
| `winver` | Verificar versão, build e edição do Windows |
| `net user` | Listar contas locais no sistema |
| `net user <usuario>` | Consultar detalhes de uma conta específica |
| `lusrmgr.msc` | Gerenciar e inspecionar usuários e grupos locais |
| `eventvwr.msc` | Acessar o Event Viewer |
| `taskschd.msc` | Abrir o Agendador de Tarefas |
| `wf.msc` | Abrir o Firewall do Windows |
| `netsh advfirewall firewall show rule name=all` | Revisar regras de firewall |
| `C:\Windows\System32\drivers\etc\hosts` | Verificar entradas de resolução de nomes |
| `Get-LocalUser` | Alternativa PowerShell para listar usuários locais |

## Como a investigação se conecta

O ponto central dessa sala é entender que a investigação de uma máquina Windows comprometida não é uma busca por um único arquivo ou comando isolado. Ela é uma síntese de várias evidências:

- a máquina informa o contexto do sistema;
- o usuário local revela quem foi adicionado;
- o Event Viewer mostra a linha do tempo;
- o Agendador de Tarefas revela persistência;
- o Firewall mostra comunicação aberta ou regras suspeitas;
- o `hosts` expõe manipulação de resolução e comunicação fora do normal.

Essa combinação de técnicas reflete um processo real de resposta a incidentes: começar com o host, entender o que mudou, confirmar quando foi alterado e validar se a atividade é legítima ou maliciosa.

## Aprendizados

- `winver` é uma verificação rápida que ajuda a contextualizar a máquina antes de aprofundar na investigação.
- `net user` em PowerShell é uma das formas mais simples de detectar contas locais suspeitas.
- `lusrmgr.msc` traz mais clareza sobre a estrutura de usuários e grupos locais.
- O Event Viewer é a principal fonte de linha do tempo em um host Windows.
- Tarefas agendadas são um forte indicador de persistência se aparecerem em locais incomuns ou com execução em horários estranhos.
- O Firewall do Windows pode revelar portas ou regras que apontam para acesso remoto ou comunicação externa anômala.
- O arquivo `hosts` é um artefato que merece atenção por ser simples, porém extremamente útil em atividades de manipulação de tráfego.
- A investigação de endpoint exige correlacionar evidências de diferentes camadas para formar uma conclusão correta.
