from openai import OpenAI
import os
import time
from dotenv import load_dotenv
import boto3
from botocore.exceptions import ClientError

def get_secret():

    secret_name = "OPENAI_API_KEY"
    region_name = "us-east-2"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    secret = get_secret_value_response['SecretString']

    print("Carregando variáveis de ambiente...")

    time.sleep(2)

    client = OpenAI(api_key=secret)

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