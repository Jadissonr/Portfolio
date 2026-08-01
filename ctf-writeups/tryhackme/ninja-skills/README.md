> ⚠️ Write-up focado em metodologia. Respostas específicas omitidas conforme boas práticas e termos de uso da plataforma.

# Ninja Skills

## Introdução

Sala do TryHackMe com foco em prática de comandos Linux para investigação de arquivos e propriedades de sistema. O objetivo principal é reforçar técnicas de análise de arquivos, permissões, hashes, regex e inspeção de metadados sem depender de soluções prontas.

- Plataforma: TryHackMe
- Nível: Easy
- Link: https://tryhackme.com/room/ninjaskills
- Objetivo: praticar comandos Linux de investigação de arquivos e descoberta de pistas em ambientes controlados.

## Metodologia

### 1. Localização dos arquivos

Comecei verificando o diretório indicado pela sala e percebi que ele estava vazio. A partir daí, passei a investigar outros diretórios do sistema com foco em localizar os arquivos relevantes. O uso de ferramentas de busca por nome, proprietário e contexto ajudou a identificar onde os artefatos reais estavam armazenados, mesmo quando não estavam no local esperado inicialmente.

### 2. Identificação por grupo

Usei listagem detalhada dos arquivos para verificar a coluna referente ao grupo proprietário. Esse tipo de inspeção é útil quando o ambiente exibe arquivos com propriedades diferentes de acordo com o contexto do usuário ou do grupo associado ao objeto.

### 3. Identificação de arquivo executável

Usei listagem detalhada para ler a string de permissões do sistema de arquivos, especialmente o bloco de permissões para outros usuários. A leitura visual das permissões ajuda a confirmar se o arquivo pode ser executado, mesmo quando a interpretação visual da cor do terminal pode ser enganosa ou não ser suficiente.

### 4. Verificação de hash

Usei uma ferramenta de hash para calcular o valor SHA1 de todos os arquivos de uma vez, e filtrei o resultado para identificar o item com o hash esperado. Esse tipo de abordagem é útil quando o desafio exige comparar valores de integridade entre múltiplos artefatos sem precisar inspecionar manualmente um por um.

### 5. Busca por padrão de IP dentro de arquivos

Essa parte foi a mais desafiadora e mostrou a importância de pensar de forma incremental. A primeira tentativa foi usar uma expressão regular simples, mas ela não foi suficiente para capturar o padrão de forma confiável. A partir daí, evolui para um padrão mais preciso usando classes de caracteres e quantificadores, como [0-9] e {1,3}, além do escape de caracteres especiais como o ponto.

Esse processo reforçou um ponto importante: a diferença entre regex básica e regex estendida. Em muitos casos, o uso de grep com a opção adequada faz diferença fundamental em termos de compatibilidade e precisão na busca.

### 6. Contagem de linhas

Usei contagem de linhas em todos os arquivos simultaneamente para identificar rapidamente se algum item tinha características diferentes. Esse procedimento revelou a presença de um arquivo oculto que não havia sido observado antes, o que reforçou a importância de considerar arquivos que não aparecem com wildcard simples por padrão.

### 7. Identificação por UID numérico

Usei listagem detalhada arquivo por arquivo e observei que, em alguns casos, o sistema exibiu o UID numérico bruto em vez do nome de usuário correspondente. Esse comportamento é importante porque mostra que o sistema de arquivos pode guardar identificadores numéricos quando não há um usuário cadastrado no sistema de usuários local.

## Principais Aprendizados

- A lista de arquivos não sempre está no local esperado, então investigar diretórios diferentes faz parte da metodologia.
- O uso de listagem detalhada é essencial para entender dono, grupo, permissões e metadados.
- Permissões podem ser interpretadas de forma mais confiável quando se lê a string completa, em vez de depender apenas da cor visual do terminal.
- A análise de hashes é uma técnica eficiente para comparar integridade de arquivos em massa.
- Regex pode evoluir de forma incremental; a precisão aumenta quando se usam classes de caracteres e quantificadores adequados.
- Há diferença prática entre regex básica e estendida, especialmente ao usar ferramentas como grep.
- Wildcards simples não capturam arquivos ocultos por padrão, então é importante considerar esse detalhe em inspeções.
- O UID numérico pode aparecer sem nome associado quando o usuário correspondente não existe no sistema local.

## Comandos Utilizados (referência)

| Comando | Propósito |
|---|---|
| find | Localizar arquivos em diretórios diferentes do sistema. |
| ls -l | Listar arquivos com detalhes de proprietário, grupo e permissões. |
| chmod | Ajustar permissões de arquivos ou diretórios. |
| stat | Inspecionar metadados de arquivos. |
| sha1sum | Gerar hashes SHA1 para comparação. |
| grep | Filtrar resultados de saída de comandos. |
| grep -E | Usar expressões regulares estendidas. |
| wc -l | Contar linhas de arquivos. |
| ls -la | Incluir arquivos ocultos na listagem. |
| id | Consultar informações de usuário e grupo. |
| file | Identificar o tipo de arquivo. |
| cut | Extrair colunas ou partes específicas de saída. |
| sort | Organizar resultados de forma mais legível. |
| uniq | Remover entradas duplicadas em saídas processadas. |
