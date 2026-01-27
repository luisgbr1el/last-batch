# Last.Batch

Aplicação desktop para envio em lote de scrobbles para o Last.fm. Permite processar arquivos CSV com históricos de reprodução e enviá-los para sua conta do Last.fm de forma automatizada.

## Funcionalidades

- **Autenticação com Last.fm**: Integração direta com a API do Last.fm
- **Processamento em Lote**: Carregue arquivos CSV, TXT ou JSON com histórico de reprodução
- **Visualização de Dados**: Prévia dos scrobbles antes do envio
- **Remoção Seletiva**: Remova itens individuais da lista antes de enviar
- **Progresso em Tempo Real**: Acompanhe o envio dos scrobbles com barra de progresso
- **Gerenciamento de Sessão**: Mantenha-se autenticado entre sessões

## Requisitos

- Python 3.7 ou superior
- Conta no Last.fm
- API Key e API Secret do Last.fm

## Configuração

### 1. Obter credenciais do Last.fm

1. Acesse [https://www.last.fm/api/account/create](https://www.last.fm/api/account/create)
2. Crie uma aplicação e obtenha sua **API Key** e **API Secret**

### 2. Configurar variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
API_KEY=sua_api_key_aqui
API_SECRET=seu_api_secret_aqui
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

## Executar localmente

```bash
python main.py
```

## Formato do arquivo de entrada

O arquivo deve ser um CSV com o seguinte formato:

```
Artista,Música,Timestamp
The Beatles,Yesterday,2024-01-01 12:00:00
Pink Floyd,Wish You Were Here,2024-01-01 13:30:00
```

**Estrutura esperada:**
- Coluna 1: Nome do artista
- Coluna 2: Nome da música
- Coluna 3: Timestamp (qualquer formato, será convertido para timestamp Unix atual)

## Como usar

1. Execute a aplicação
2. Clique em **Autenticar-se** para conectar sua conta do Last.fm
3. Clique em **Enviar arquivo** e selecione seu arquivo CSV/TXT/JSON
4. Revise a lista de scrobbles carregados
5. (Opcional) Remova itens indesejados selecionando-os e pressionando **Delete**
6. Clique em **Scrobblar** para enviar os dados para o Last.fm

## Estrutura do projeto

```
last-batch/
├── main.py           # Interface gráfica e lógica principal
├── auth.py           # Autenticação com Last.fm
├── requirements.txt  # Dependências do projeto
├── .env              # Variáveis de ambiente (não versionado)
└── README.md         # Este arquivo
```

## Tecnologias utilizadas

- **Tkinter**: Interface gráfica
- **pylast**: Biblioteca para API do Last.fm
- **python-dotenv**: Gerenciamento de variáveis de ambiente

## Autor

Desenvolvido por [luisgbr1el](https://github.com/luisgbr1el)

## Licença

Este projeto é de código aberto e está disponível para uso pessoal.
