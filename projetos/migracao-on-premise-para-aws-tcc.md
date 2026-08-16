# Migração On-Premise para AWS (TCC)

Projeto de TCC voltado para a migração de uma infraestrutura on-premise para a AWS, com foco em WordPress, MySQL, monitoramento e segurança de infraestrutura.

## Objetivo

Avaliar e implementar uma migração de ambiente web para a nuvem, preservando disponibilidade, controle de acesso e observabilidade da aplicação.

## Serviços e ferramentas

| Serviço / Ferramenta | Função |
|---|---|
| WordPress | Aplicação web hospedada em instância EC2 |
| MySQL | Banco de dados relacional da aplicação |
| Amazon CloudWatch | Monitoramento de métricas e logs da infraestrutura |
| AWS Trusted Advisor | Recomendações de custo, segurança e performance |
| Iptables | Firewall configurado na camada do sistema operacional Linux |

## Status
✅ Concluído

## Diagrama de topologia de rede AWS

```mermaid
graph TD
    U[Usuário externo] --> IGW[Internet Gateway]
    IGW --> VPC[VPC - Virtual Private Cloud]

    subgraph Publica[Subnet Pública]
        EC2[EC2 - WordPress<br/>Aplicação Web]
        SG_APP[Security Group<br/>EC2 - Regras HTTP/HTTPS]
        EC2 --> SG_APP
    end

    subgraph Privada[Subnet Privada]
        RDS[(RDS / MySQL<br/>Banco de dados)]
        SG_DB[Security Group<br/>DB - Acesso restrito]
        RDS --> SG_DB
    end

    VPC --> Publica
    VPC --> Privada

    SG_APP -->|TCP 3306| RDS
    EC2 -->|Conexão aplicação-banco| RDS

    subgraph Seguranca[Segurança e Governança]
        IPT[iptables<br/>Firewall no SO]
        CW[Amazon CloudWatch<br/>Logs e métricas]
        TA[AWS Trusted Advisor<br/>Recomendações]
        IAM[IAM<br/>Políticas e grupos]
        AK[Access Keys<br/>Autenticação de usuários/serviços]
    end

    EC2 --> IPT
    EC2 --> CW
    RDS --> CW
    IAM --> AK
    IAM -->|Políticas de acesso| EC2
    IAM -->|Políticas de acesso| RDS
    TA -->|Recomendações| VPC
    TA -->|Recomendações| EC2
    TA -->|Recomendações| RDS

    U -->|HTTPS| EC2
```

## Descrição da arquitetura

- A aplicação WordPress roda em uma instância EC2 localizada na subnet pública.
- O banco de dados MySQL fica em uma subnet privada, isolado de acesso direto externo.
- O Security Group da instância EC2 permite tráfego Web, enquanto o Security Group do banco restringe o acesso apenas à aplicação.
- O iptables atua como camada adicional de firewall no sistema operacional.
- Amazon CloudWatch e AWS Trusted Advisor complementam o monitoramento e a governança da solução.
