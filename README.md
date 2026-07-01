# SiteWatch - Plataforma de Monitoramento de Sites

![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-API-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue)
![Docker](https://img.shields.io/badge/Docker-Containers-blue)
![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-CI%2FCD-black)
![Prometheus](https://img.shields.io/badge/Prometheus-Monitoring-orange)
![Grafana](https://img.shields.io/badge/Grafana-Dashboards-yellow)
![AWS](https://img.shields.io/badge/AWS-EC2-orange)
![Terraform](https://img.shields.io/badge/Terraform-IaC-purple)
![Linux](https://img.shields.io/badge/Linux-Ubuntu-green)

SiteWatch é uma plataforma de monitoramento de sites criada para demonstrar, em um projeto prático, o uso de APIs REST, banco de dados, containers, CI/CD, cloud, infraestrutura como código e observabilidade.

A aplicação permite cadastrar sites, executar verificações de disponibilidade, registrar histórico de checks, exportar métricas no formato Prometheus e visualizar indicadores em dashboards no Grafana.

---

## Visão Geral

O projeto é composto por:

* API REST desenvolvida com FastAPI
* Worker de monitoramento periódico em Python
* Banco PostgreSQL para persistência dos sites e verificações
* Prometheus para coleta de métricas
* Grafana para visualização dos indicadores
* Docker Compose para execução da stack
* GitHub Actions para deploy automatizado em AWS EC2
* Terraform para provisionamento básico da infraestrutura AWS

---

## Arquitetura da Solução

```text
                     Git Push
                         |
                         v
                 GitHub Repository
                         |
                         v
                  GitHub Actions
                         |
                         v
                      AWS EC2
                         |
                         v
                  Docker Compose
                         |
        +----------------+----------------+
        |                |                |
        v                v                v
   SiteWatch API   SiteWatch Monitor   PostgreSQL
        |
        v
   Prometheus
        |
        v
     Grafana
```

---

## Fluxo de Monitoramento

```text
Sites cadastrados
       |
       v
SiteWatch Monitor
       |
       v
POST /sites/{id}/check
       |
       v
Registro no PostgreSQL
       |
       v
Métricas em /metrics
       |
       v
Prometheus + Grafana
```

---

## Evidências do Projeto

As imagens abaixo demonstram a aplicação em funcionamento, incluindo deploy automatizado, containers em produção, documentação da API, endpoints, métricas e dashboard de observabilidade.

### Pipeline CI/CD com GitHub Actions

![GitHub Actions Deploy](docs/images/github-actions-deploy.png)

### Containers Docker em Execução na AWS EC2

![Docker Containers](docs/images/ec2-docker-containers.png)

### Documentação Interativa da API

![Swagger API](docs/images/swagger-api.png)

### Listagem de Sites Monitorados

![Sites Endpoint](docs/images/sites-endpoint.png)

### Health Check da Aplicação

![Health Endpoint](docs/images/health-endpoint.png)

### Métricas Exportadas para Prometheus

![Prometheus Metrics](docs/images/prometheus-metrics.png)

### Dashboard no Grafana

![Grafana Dashboard](docs/images/grafana-dashboard.png)

---

## Funcionalidades

* Cadastro de sites para monitoramento
* Listagem de sites cadastrados
* Execução manual de verificação por site
* Monitoramento periódico via worker
* Registro de status HTTP, disponibilidade e tempo de resposta
* Histórico de verificações por site
* Endpoint de health check
* Endpoint de métricas compatível com Prometheus
* Dashboard de acompanhamento no Grafana
* Deploy automatizado em instância EC2

---

## Endpoints Principais

| Método | Rota | Descrição |
| --- | --- | --- |
| `GET` | `/` | Verifica se a API está respondendo |
| `GET` | `/health` | Retorna o status de saúde da aplicação |
| `GET` | `/metrics` | Exporta métricas no formato Prometheus |
| `GET` | `/sites` | Lista os sites cadastrados |
| `POST` | `/sites` | Cadastra um novo site |
| `POST` | `/sites/{site_id}/check` | Executa uma verificação manual |
| `GET` | `/sites/{site_id}/checks` | Lista o histórico de verificações |

Exemplo de cadastro:

```json
{
  "name": "GitHub",
  "url": "https://github.com"
}
```

---

## Métricas Exportadas

| Métrica | Descrição |
| --- | --- |
| `sitewatch_site_up` | Status do site monitorado, usando `1` para online e `0` para offline |
| `sitewatch_response_time_ms` | Tempo de resposta do site em milissegundos |
| `sitewatch_checks_total` | Total de verificações executadas por site |

---

## Tecnologias Utilizadas

* Python 3.12
* FastAPI
* PostgreSQL
* Docker
* Docker Compose
* Prometheus
* Grafana
* GitHub Actions
* AWS EC2
* Terraform
* Ubuntu Linux

---

## Estrutura do Projeto

```text
sitewatch/
├── .github/
│   └── workflows/
│       └── deploy.yml
├── app/
│   ├── Dockerfile
│   ├── main.py
│   ├── monitor.py
│   └── requirements.txt
├── docs/
│   └── images/
├── infrastructure/
│   └── terraform/
│       ├── backend.tf
│       ├── main.tf
│       ├── outputs.tf
│       └── variables.tf
├── observability/
│   └── prometheus/
│       └── prometheus.yml
├── docker-compose.yml
└── README.md
```

---

## Execução com Docker Compose

Suba a stack localmente:

```bash
docker compose up -d --build
```

Serviços publicados:

| Serviço | URL |
| --- | --- |
| API | `http://localhost:8000` |
| Swagger UI | `http://localhost:8000/docs` |
| Prometheus | `http://localhost:9090` |
| Grafana | `http://localhost:3000` |
| PostgreSQL | `localhost:5432` |

Para acompanhar os logs:

```bash
docker compose logs -f
```

Para parar os containers:

```bash
docker compose down
```

---

## Deploy Automatizado

O deploy é executado pelo GitHub Actions quando há push na branch `main`.

O workflow acessa a instância EC2 por SSH, atualiza o repositório no servidor e recria os containers com Docker Compose:

```text
git pull origin main
docker compose up -d --build
docker image prune -f
```

Secrets utilizados pela pipeline:

* `EC2_HOST`
* `EC2_USER`
* `EC2_SSH_KEY`

---

## Infraestrutura AWS

O diretório `infrastructure/terraform` contém a base de infraestrutura para execução do projeto na AWS:

* VPC
* Subnet pública
* Internet Gateway
* Route Table
* Security Group
* Instância EC2 Ubuntu

Variáveis principais:

* `aws_region`
* `project_name`
* `my_ip`
* `key_name`

---

## Roadmap

### Concluído

* [x] Backend com FastAPI
* [x] Cadastro e listagem de sites
* [x] Serviço de monitoramento periódico
* [x] Registro de verificações no PostgreSQL
* [x] Containerização com Docker Compose
* [x] Exportação de métricas para Prometheus
* [x] Dashboard no Grafana
* [x] Pipeline de deploy com GitHub Actions
* [x] Deploy em AWS EC2
* [x] Infraestrutura base com Terraform

### Próximas Evoluções

* [ ] Script de inicialização/migração do banco de dados
* [ ] Alertas com Alertmanager
* [ ] Notificações via Discord ou e-mail
* [ ] Monitoramento de certificados SSL
* [ ] Centralização de logs com Loki
* [ ] Dashboard dedicado de performance
* [ ] Deploy em Kubernetes
* [ ] GitOps

---

## Habilidades Demonstradas

* Desenvolvimento Backend
* Criação de APIs REST
* Persistência com banco relacional
* Containerização de aplicações
* Automação de deploy
* CI/CD
* Provisionamento de infraestrutura
* Observabilidade
* Coleta de métricas
* Troubleshooting em ambiente Linux
* Deploy de aplicação em cloud

---

## Autor

**Cassiano Marinho**

DevOps | Cloud | Observabilidade | Desenvolvimento Backend

Este projeto faz parte da minha jornada de evolução profissional nas áreas de Desenvolvimento Backend, DevOps, Cloud Computing, Monitoramento, Observabilidade e Site Reliability Engineering.
