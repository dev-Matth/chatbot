from openai import OpenAI
import os
import time
from dotenv import load_dotenv

print("Carregando variáveis de ambiente...")

time.sleep(2)

caminho_arquivo_env = os.path.join('config', '.env')
load_dotenv(dotenv_path=caminho_arquivo_env)
chave_api = os.getenv('CHATBOT_API_KEY')
client = OpenAI(api_key=chave_api)

print("Variáveis de ambiente carregadas com sucesso!")

time.sleep(2)

print("Bem-vindo ao ChatGPT (Coded by Matth)! Digite 'sair' para encerrar a conversa.")

def enviar_mensagem(mensagem, Lista_mensagens=[]):
    Lista_mensagens.append(
        {"role": "user", "content": mensagem}
    )

    response = client.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages = Lista_mensagens,
    )

    return response.choices[0].message

lista_mensagens = []

while True:
    texto = input("Você: ")

    if texto.lower() == "sair":
        print("Encerrando a conversa...")
        time.sleep(1)
        break
    else:
        resposta = enviar_mensagem(texto, lista_mensagens)
        lista_mensagens.append(resposta)
        print("ChatGPT: " + resposta["content"])