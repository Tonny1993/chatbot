from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("CHAVE_API")
client = OpenAI(api_key = api_key)

QtdPerguntas = 0

with open('contexto/informacoes.txt', 'r',encoding='windows-1252') as f:
    informacoes = f.read()

lista_mensagens = [{'role': 'system', 'content':informacoes}]

def enviar_mensagem(mensagem, lista_mensagens = []):
    lista_mensagens.append({"role": "user", "content": mensagem})
    resposta = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=lista_mensagens,
    )
    return resposta.choices[0].message.content

while True:
    texto = input("Em que posso ajudar?")
    lista_mensagens.append({'role': 'user', 'content': f"{texto}"})
    resposta = enviar_mensagem(texto, lista_mensagens)
    lista_mensagens.append({'role': 'assistant', 'content': f"{resposta}"})
    print(resposta)
    QtdPerguntas += 1
    if QtdPerguntas == 3:
        resumo = "Resuma as 3 respostas anteriores."
        lista_mensagens.append({'role': 'user', 'content': resumo})
        resposta = enviar_mensagem(texto, lista_mensagens)
        print(resposta)
        QtdPerguntas = 0
        lista_mensagens.clear()
        lista_mensagens.append({'role': 'system', 'content': informacoes})