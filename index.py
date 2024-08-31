from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os
import time
from dotenv import load_dotenv
import boto3
from botocore.exceptions import ClientError

app = Flask(__name__)

# Função para obter a chave da API do OpenAI do AWS Secrets Manager
def get_secret():
    secret_name = "OPENAI_API_KEY"
    region_name = "us-east-2"

    # Cria um cliente do Secrets Manager
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
        raise e

    secret = get_secret_value_response['SecretString']
    return secret

# Carrega a chave da API do OpenAI
client = OpenAI(api_key=get_secret)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/contatos")
def contatos():
    return render_template("contatos.html")

@app.route("/usuarios/<nome_usuario>")
def usuarios(nome_usuario):
    return render_template("usuarios.html", nome_usuario=nome_usuario)

@app.route("/chat")
def chat():
    return render_template("chat.html")

@app.route('/chat_api', methods=['POST'])
def chat_api():
    data = request.json
    user_message = data.get('message')

    response = OpenAI.Completion.create(
        engine="text-davinci-003",
        prompt=user_message,
        max_tokens=150
    )

    bot_reply = response.choices[0].text.strip()
    return jsonify({'reply': bot_reply})

if __name__ == "__main__":
    app.run(debug=True)