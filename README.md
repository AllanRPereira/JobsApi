#Jobs-API
#### Sistema de Gerenciamento de Trabalhos e Tarefas
Essa api foi desenvolvida com a finalidade de estudo, de aperfeiçoamento das habilidades web e como prova de vaga de emprego.

##  Funcionamento
O sistema, como já dito, tem a finalidade de adicionar trabalhos, *jobs*, e dentro desses adicionar tarefas, *tasks*, em um banco de dados provido pelo sistema. Para posterior consulta ou demais tarefas.

Possuindo alguns requisitos no momento de criação desses *jobs* sendo eles:
- O nome de um *job* é único e obrigatório.
- Um *job* pode depender de outro *job*.
- Um *job* não pode ser dependente dele mesmo
- Dois *jobs* não podem ser dependentes entre si.
- Um *job* pode ter ou não ter uma lista de *tasks*

Não havendo outros requisitos como critérios para nomes de job, quantidade de tarefa e etc.

## Funcionalidades
O sistema possui duas interfaces de trabalho uma é a **API** propriamente dita e a outra é a interface padrão do usuário, **home**, acessível pelo navegador.
Possuindo as seguintes capacidades:
- Controle de usuários e suas permissões, já fixa e sendo *adm* e *teste*, **cada um possuindo suas permissões**, porém com facilidade de implantação de um sistema de adição.
- Possibilidade de Consulta, Edição, Inserção e Remoção de *tarefas* e *jobs* em ambas as interfaces atráves de **tokens de acesso**.

## Tecnologias Utilizadas
A prova foi escrita pedindo a utilização de tecnologias *java*, entretando nesse projeto utilizei as tecnologias as quais domino mais sendo as seguintes:
### Backend:
- **Python3**: Como linguagem principal do projeto, versão *3.7.5*
- **Flask**: Como microweb-framework para a construção do sistema web
- **Pytest**: Para a elaboração dos testes unitários do sistema de banco de dados e da *API* do sistema
- **Sqlalchemy**: Para a comunicação com o banco de dados utilizando sua forma mais simples, sem o uso de ORM's.
- **Sqlite**: No banco de dados, por se tratar de um banco de dados simples, leve e de fácil uso, e era um equivalente ao pedido no documento original.Originalmente no modo **In-memory**
- **Gunicorn**: Servidor WSGI para a aplicação

### Frontend:
- **Html5 e Css**: acredito que não precisa dos motivos, mas os usei por serem mais simples e não vi necessidade de utilização de outras tecnologias
- **Bootstrap**: por facilitar muito na hora da estilização e da ordenação dos elementos na tela
- **Javascript**: Sem o uso de outras bibliotecas pois não houve necessidade devido ao tamanho do projeto.

## Como utilizar na sua máquina
Como já mencionamos as tecnologias utilizadas, elas obviamente são os requisitos mínimos para a utilização da aplicação. Mas de forma mais explicativo temos que é somente necessário os seguintes programas:
1. Python3, de preferência a versão **3.7.5**.
2. O **pip** instalado para instalação das dependências no seu sistema.
3. Além do **git clone *EsseRepositório*** para ter os arquivos na sua máquina

Para a instalação das dependências basta utilizar o comando, após o pip instalado, acredito que a sintáxe é a mesma para windows e linux:

`pip3 install -r requirements.txt`

Após instaladas as dependências execute o comando para inicializar a aplicação, **todos os comandos a seguir são feitos na pasta raiz do projeto**:

- Para funcionar sem debug: `gunicorn --bind 127.0.0.1:5000 main:frontEnd` 
- Para funcionar com o debug do **flask**: `python3 -m docs.frontend.home`

*A porta 5000 é a utilizadas nos testes unitários da API*

E então rode os testes da aplicação:

`pytest docs/backend/tests -vv`

Se tudo ocorrer bem você não verá nenhum sinal vermelho e todos os testes irão passar, entretando se algo der errado não se atenha a abrir uma **issue** que consertarei o mais rápido possível

#### Detalhe importante:
Os arquivos referentes ao Jquery, *do bootstrap*, e ao próprio *bootstrap.min.css* serão anexados num zip na pasta **docs/frontend/static** para caso queira utilizar as depedências de forma offline. Sendo além disso necessário remover os comentários que deixei nos arquivos que abrem as dependências offline:
- **docs/frontend/templates/imports.html**
- **docs/frontend/templates/header.html**

## O que ainda pode ser melhorado
Há alguns detalhes que ainda podem ser melhorados nessa aplicação e que estou providenciando realizá-los:
- Uma melhor forma de manipulação dos erros que podem vir a ocorrer, tanto na API quanto no Home(*Interface Web*), como Method Not Allowed, ou outros tipos de exceção, já existe um contorno no Home para essas situações mas é muito simples.
- Mais testes garantindo a estabilidade em mais situações de erro.
- Uma interface simples para adição de usuário seria interessante.

###  O que aprendi com esse projeto e que você pode aprender também

Nesse projeto pude aprender muitas coisas novas, que de certa forma conhecia mas não possuia muita prática, como: 
- Manipulação de banco de dados utilizando o **Sqlalchemy**, provavelmente a biblioteca mais famosa em python para essa finalidade. 
- Ganhei muito mais confiança e habilidade na utilização das funcionalidades do **Flask**. Acredito sim que ainda falta bastante, mas já foram vários passos.
- **Determinação e foco**, pode parecer um projeto simples, e provavelmente é pra quem já tem certo domínio, mas foi demorado, exigiu paciência e dedicação para tentar fazer tudo da melhor forma possível. E como tal projeto visa o estudo provavelmente muitas outras coisas ainda podem ser melhoradas.

Como curiosidade e talvez critério de conhecimento entre quem vê esse projeto, o tempo que passei, *de acordo com o wakatime*, foi de **46 horas** ao longo de quase um mês, entretanto acredito que esse tempo seja maior devido aos momentos de não escrita de código.

Bons Estudos Pessoal!!

![Status](https://img.shields.io/badge/Working-Yes-Success "Status")