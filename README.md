# 📚 API de Atividade de Salas

Este repositório contém a **API de Atividade de Salas**, desenvolvida com **Flask** e **SQLAlchemy**, como parte de uma arquitetura baseada em **microsserviços**.

## 🧩 Arquitetura

A API de Atividade de Salas é um **microsserviço** que faz parte de um sistema maior chamado [School System](https://github.com/gortin1/ProjetoApi.git), sendo responsável exclusivamente pelo gerenciamento das atividades de um professor.

⚠️ **Importante:** Esta API **depende da API de Gerenciamento Escolar (School System)** rodando localmente, pois consome o endpoint `GET /professores/<id>` para validar se um **Professor** existe.

---

## 🚀 Tecnologias Utilizadas

- Python 3.x
- Flask
- SQLAlchemy
- SQLite (como banco de dados local)
- Requests (para consumo da API externa)
- Unittest (para testes unitários da API)

---

## ▶️ Como Executar a API

`Observação importante: Para melhor entendimento coloque ambas as pastas das APIs em uma só pasta!`

### 1º Passo - Crie uma network em Docker

``` bash
docker network create minha-network
```

### 2º Passo - Construa a imagem api-gestão-escolar da [api de gestão](https://github.com/gortin1/ProjetoApi.git) 

``` bash
cd projetoAPI
docker build -t api-gestao-escolar .
``` 

### 3º Passo - Rode a imagem criada na network que você criou

``` bash
docker run -d --name api-gestao-escolar --network minha-network api-gestao-escolar
cd ..
```

### 4º Passo - Construa a imagem atividade-salas da [api de atividade](https://github.com/gortin1/atividade-salas.git)

``` bash
cd atividade-salas
docker build -t atividade-salas atividade-salas
```

### 5º Passo - Rode a imagem criada na network que você criou

``` bash
docker run -d --name api-gestao-escolar --network minha-network api-gestao-escolar
cd ..
```

#### Pronto! Você já pode utilizar a api tranquilamente!

## 📡 Endpoints Principais

- `GET /atividades` – Lista todas as atividades
- `POST /atividades` – Cria uma nova atividade
- `GET /atividades/<id>` – Detalha uma atividade
- `PUT /atividades/<id>` – Atualiza uma atividade (é necessário preencher todos os campos para atualizar a atividade)
- `DELETE /atividades/<id>` – Remove uma atividade

### Exemplo de corpo JSON para criação:

```json
{
  "professor_id": 1,
  "titulo": "Api e Microsserviços",
  "descricao": "Desenvolver uma API completa para criar atividades com Python e Flask.",
  "disciplina": "Desenvolvimento de APIs e Microsserviços",
  "data_entrega": "2025-06-28",
  "hora_fim": "23:59"
}
```

---

## 🔗 Dependência Externa

📌 **Certifique-se de que a API de Gerenciamento Escolar esteja em execução** antes de criar uma atividade. Caso o endpoint de professor não retorne uma resposta válida (`200 OK`), a criação da reserva será negada.

Endpoint de professores:

```
http://localhost:5000/api/professores/{id}
```

---

## 📦 Estrutura do Projeto

```
atividade-salas/
│
├── api/                       
│   ├── atividade/               
│   │   ├── atividade_model.py   
│   │   └── atividade_route.py   
│   │
│   └── test/                  
│       └── test.py                     
├── app.py                     
├── database.py   
├── Dockerfile           
├── README.md                  
└── requirements.txt           
```

---

## 🛠️ Futuras Melhorias

- Validação de conflito de horário na sala
- Integração via fila (RabbitMQ) com outros microsserviços
- Autenticação de usuários
- Swagger

---

## 🧑‍💻 Autores

- [Camila Ribeiro](https://github.com/camilasribeiro)
- [Fernando Storel](https://github.com/Fernandostorel)
- [Gabriel Nathan](https://github.com/gortin1)
- [Nicolas Lima](https://github.com/nicolas-liima)


Projeto de arquitetura com Flask e microsserviços.
