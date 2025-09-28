# Desafio ClinicAI
Este é o repositório contendo os códigos da atividade proposta pela Equipe ClinicAI

# Propósito do Projeto
O propósito foi criar um agente de IA para triagens de pacientes em uma clínica fictícia.
O agente:
 - Receberia mensagens de um usuário
 - Responderia com ajuda de uma LLM
 - Armazenaria interações em um Banco de Dados.

# Configuração do projeto
Para rodar o projeto você precisa possuir o Python na sua máquina. Se já tem, basta seguir os passos abaixo. Se não, instale primeiro e após isso, siga os passos:

1 - No terminal, entre na pasta backend:
```
cd backend
```

2 - Ative o Ambiente Virtual do Python:
```
python -m venv venv
```

3 - Chame o Ambiente Virtual do Python:
- No Mac ou Linux:
```
source venv/bin/activate
```

- No Windows:
```
.\venv\Scripts\activate
```

- **OBS.:** Após a ativação da venv, o nome do ambiente deve ficar como:
```
(venv) C:\caminho\projeto
```

4 - Instale as dependências necessárias como requisitos pra rodar o projeto:
```
pip install -r requirements.txt
```

5 - Rode o back-end e deixe ativo:
```
python -m uvicorn app.main:app --reload
```

6 - Abra um novo terminal na sua IDE

7 - No terminal, entre na pasta frontend:
```
cd frontend
```

8 - Inicie o frontend:
```
python -m http.server 8080
```

**Após isso, o servidor iniciará e você poderá testar normalmente. Lembre-se de utilizar a sua key do API Gemini e do MongoDB.**