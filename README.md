# artist-api
[![License: MIT](https://img.shields.io/github/license/alessandroHenrique/catalogo-discos.svg)](LICENSE.txt)

API que consome dados da [Genius](https://docs.genius.com/) que baseado num artista, pega suas 10 músicas mais populares utilizando Flask rest.

## Rodando o projeto localmente
As seguintes instruções vão lhe guiar para instalar o projeto e suas dependências.

### Instalando dependências
É necessário primeiramente instalar o [docker](https://docs.docker.com/engine/install/) e [docker-compose](https://docs.docker.com/compose/install/) para rodar o projeto.

No root do projeto, crie um arquivo .env e pegue as informações do arquivo env.example e complete-as de acordo com suas configurações.
`AWS_ACCESS_KEY_ID` e `AWS_SECRET_ACCESS_KEY` você vai obter quando criar um usuário na sua conta AWS. Já o `CLIENT_ACCESS_TOKEN` você adquire quando
cria uma conta no [Genius](https://docs.genius.com/) e solicita uma chave de acesso.

Após configurar o arquivo .env, rodar o comando no root do projeto:

```
docker-compose up -d --build
```

Agora tanto o serviço Redis quando a aplicação flask estão rodando, só utilizar alguma ferramenta como o [Postman](https://www.postman.com/) para acessar os endpoints
em `http://0.0.0.0/`

Por fim, basta criar o banco no dynamo na sua conta amazon via endpoint:

```
http://0.0.0.0/api/create-table
```

Com a tabela no dynamo criada, você já pode pesquisar qualquer artista utilizando a API.

## Endpoints da Api

# /api/artist
Esse recurso diz respeito aos artistas musicais.

## GET
Parâmetros query string:
- q (representa nome do artista)
- cache (representa se músicas do respectivo artista devem ser cacheadas ou não. Padrão é True em caso de não passar valor)

Exemplo de requisição:
- http://0.0.0.0/api/artist?q=sia&cache=False

Exemplo de response:
+ Response 200

```
{
    "songs": [
        "Chandelier",
        "The Greatest",
        "Cheap Thrills",
        "Snowman",
        "Helium",
        "Cheap Thrills (Remix)",
        "Elastic Heart (Hunger Games Version)",
        "Elastic Heart",
        "Bird Set Free",
        "Alive"
    ]
}
```

# /api/create-table
Esse recurso diz respeito a tabela Artist do dynamo.

## GET

Exemplo de requisição:
- http://0.0.0.0/api/create-table

Exemplo de response:
+ Response 200

```
{
    "message": "Table created"
}
```
