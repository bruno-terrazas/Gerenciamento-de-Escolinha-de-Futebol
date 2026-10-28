# Gerenciamento de Escolinha de Futebol

Sistema web para gerenciar uma escolinha de futsal e futebol: cadastro de atletas, ficha individual, controle de mensalidades e acompanhamento de quem pagou e quem deve.

Projeto de estudo, desenvolvido durante o 2º semestre do curso de Ciência da Computação da UFMS. O sistema foi pensado a partir da necessidade real de uma escolinha, que hoje controla tudo em planilhas. Ele roda localmente, sem internet e sem login.

> **Status:** em desenvolvimento. Veja [o que já funciona](#funcionalidades) e [o que vem a seguir](#roadmap).

## Funcionalidades

**Atletas**
- Cadastro com dados pessoais, responsáveis, contato, escola, categoria e modalidades
- Lista de atletas, com acesso à ficha individual
- Ficha com dados completos, modalidades, mensalidade calculada e histórico de pagamentos
- Edição dos dados e das modalidades
- Inativar e reativar atleta (o histórico financeiro nunca é apagado)

**Pagamentos**
- Matrícula e primeira mensalidade geradas automaticamente no cadastro
- Geração das mensalidades do mês para todos os atletas ativos, sem duplicar cobranças
- Marcar cobrança como paga, pela tela de pagamentos ou pela ficha do atleta
- Filtros combináveis por mês, ano e categoria
- Resumo com total recebido, pendente e esperado, que acompanha os filtros

## Tecnologias

- **Python 3** e **Flask** (rotas e lógica)
- **SQLite** (banco de dados), com o módulo `sqlite3` da biblioteca padrão
- **HTML, CSS e Jinja2** (templates)

## Como rodar

Pré-requisito: Python 3 instalado.

```bash
# 1. Clonar o repositório
git clone https://github.com/bruno-terrazas/Gerenciamento-de-Escolinha-de-Futebol.git
cd Gerenciamento-de-Escolinha-de-Futebol

# 2. Criar e ativar o ambiente virtual (Windows)
python -m venv venv
venv\Scripts\activate

# 3. Instalar as dependências
pip install -r requirements.txt

# 4. Criar o banco de dados (gera o banco.db nesta pasta)
python banco.py

# 5. Iniciar o sistema
python main.py
```

Depois, acesse `http://localhost:5000/atletas` no navegador.

**Observações:**
- Rode os comandos **dentro da pasta do projeto**. O sistema procura o `banco.db` na pasta de onde é iniciado.
- O `banco.py` cria as tabelas e já insere as categorias (Sub-9 a Sub-17) e as modalidades (Futsal e Futebol de campo). Pode ser executado mais de uma vez sem duplicar esses dados.
- O `banco.db` não faz parte do repositório, pois armazena dados pessoais. Cada instalação cria o seu.
- Em Linux ou macOS, a ativação do ambiente é `source venv/bin/activate`.

## Estrutura do projeto

```
├── main.py            # rotas da aplicação e cálculo de valores
├── banco.py           # criação das tabelas e dados fixos
├── requirements.txt   # dependências
└── templates/
    ├── atletas.html
    ├── novo_atleta.html
    ├── ficha_atleta.html
    ├── editar_atleta.html
    └── pagamentos.html
```

## Banco de dados

| Tabela | Descrição |
|---|---|
| `categorias` | Sub-9, Sub-11, Sub-13, Sub-15 e Sub-17 |
| `modalidades` | Futsal e Futebol de campo |
| `atletas` | Dados do atleta e dos responsáveis, categoria, bolsa, desconto, equipe e status |
| `relacao_atletas` | Relação N:N entre atletas e modalidades |
| `pagamentos` | Cobranças: mês de referência, tipo (matrícula ou mensalidade), valor e status |

O valor de cada cobrança é gravado no momento em que ela é gerada. Assim, mudar os preços no futuro não altera o histórico.

## Regras de negócio

- **Mensalidade:** R$ 200 para uma modalidade e R$ 300 fixos para duas (não é a soma). Atleta com bolsa integral paga R$ 0. O desconto é subtraído do valor.
- **Matrícula:** taxa única de R$ 100.
- **Inativo:** atleta inativo não recebe novas cobranças, e o histórico é mantido.
- **Cobranças do mês:** são geradas manualmente, uma vez por mês. Quem não pagou continua com a cobrança pendente dos meses anteriores.

## Roadmap

Próximas etapas planejadas:

- [ ] Correções de validação nos formulários (CPF repetido, filtro só por ano)
- [ ] Matrícula com valor reduzido para alunos de uma escola parceira
- [ ] Relatórios financeiros gerais, por categoria e por modalidade, com gráfico
- [ ] Filtros na lista de atletas (categoria, modalidade, status e equipe)
- [ ] Contrato preenchido automaticamente, pronto para imprimir
- [ ] Template base e padronização visual
- [ ] Organização do código em módulos (Blueprints do Flask)

Ideias para o futuro: pagamento parcial, cancelamento de cobrança, backup do banco e acesso pela rede local.

## Sobre o desenvolvimento

Este é o meu primeiro projeto grande. Até aqui, minha base em programação vem das disciplinas de Algoritmos e Programação I e II.

Usei o **Claude** (IA da Anthropic) como apoio para aprender enquanto construo. O método que combinamos:

- Eu escrevo o **backend**: rotas em Flask, consultas SQL e regras de negócio.
- O Claude me explica os conceitos antes, revisa o meu código apontando os erros, mas sem entregar a solução pronta, e me ajuda com o **front-end** (HTML, CSS e Jinja2).

O objetivo é entender cada linha do projeto, e não só fazê-lo funcionar.

## Autor

Desenvolvido por [@bruno-terrazas](https://github.com/bruno-terrazas), estudante de Ciência da Computação na UFMS.
