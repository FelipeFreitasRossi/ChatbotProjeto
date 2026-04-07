import json
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
import os

# Importações dos módulos do core
from core.preprocess import simple_spell_check, expand_query_with_synonyms
from core.intent_classifier import find_intent_by_keywords, classify_intent_bert, INTENT_TO_FAQ_ID
from core.memory import ConversationMemory
from core.personality import obter_saudacao, PersonalityEngine

load_dotenv()
app = Flask(__name__)

# Inicializa componentes
memory = ConversationMemory()
personality = PersonalityEngine()

# Carrega FAQs
with open('faq.json', 'r', encoding='utf-8') as f:
    faq_data = json.load(f)
faq_perguntas = {k: v for k, v in faq_data.items() if k != "respostas"}
faq_respostas = faq_data["respostas"]

def gerar_menu():
    saudacao = obter_saudacao()
    menu = f"{saudacao}! Bem-vindo(a) à PUNEWMAGAZINE. Como posso ajudar?\n\n"
    menu += "Escolha uma das opções abaixo digitando o número correspondente:\n"
    for chave in sorted(faq_perguntas.keys(), key=int):
        menu += f"{chave}. {faq_perguntas[chave]}\n"
    menu += "\n📞 Digite 'falar com atendente' para falar com um humano."
    return menu

@app.route("/whatsapp", methods=['POST'])
def whatsapp_reply():
    user_id = request.values.get('From', 'unknown')
    incoming_msg = request.values.get('Body', '').strip()
    
    # Verifica se é a primeira mensagem da sessão
    session = memory.get_session(user_id)
    is_first_message = len(session.get("history", [])) == 0
    
    # Adiciona ao histórico
    memory.add_message(user_id, "user", incoming_msg)
    
    # Pré-processamento
    corrected = simple_spell_check(incoming_msg)
    expanded = expand_query_with_synonyms(corrected)
    
    resp = MessagingResponse()
    msg = resp.message()
    
    # --- SAUDAÇÃO INICIAL (se for primeira mensagem) ---
    saudacao_inicial = ""
    if is_first_message:
        saudacao_inicial = (
            f"{obter_saudacao()}! Seja muito bem-vindo(a) à *PUNEWMAGAZINE*! 🏁\n"
            "Sou o assistente virtual e estou aqui para tirar todas as suas dúvidas sobre nossos aerofólios esportivos.\n\n"
        )
    
    # --- PROCESSAMENTO DA MENSAGEM ---
    if incoming_msg.lower() in ['menu', 'oi', 'ola', 'iniciar', 'comecar', 'help', 'ajuda']:
        resposta = gerar_menu()
    elif incoming_msg.lower() == 'falar com atendente':
        resposta = "Um de nossos atendentes irá falar com você em breve. Por favor, aguarde um momento. 😊"
    elif incoming_msg in faq_respostas:
        resposta = faq_respostas[incoming_msg]
    else:
        # Tenta palavras-chave primeiro
        intent_id = find_intent_by_keywords(expanded)
        confidence = 1.0 if intent_id else 0.0
        
        # Se não encontrou, usa BERT (opcional – comente se não quiser usar)
        if not intent_id:
            try:
                intent_label, confidence = classify_intent_bert(corrected)
                intent_id = INTENT_TO_FAQ_ID.get(intent_label) if intent_label else None
            except Exception as e:
                print(f"Erro no BERT: {e}")
                intent_id = None
        
        if intent_id and confidence > 0.6:
            resposta = faq_respostas.get(intent_id, "Desculpe, não tenho essa informação.")
        else:
            resposta = personality.get_response("unknown") + "\n\n" + gerar_menu()
    
    # Junta saudação inicial com a resposta (se for primeira mensagem)
    resposta_final = saudacao_inicial + resposta if is_first_message else resposta
    
    memory.add_message(user_id, "assistant", resposta_final)
    msg.body(resposta_final)
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True, port=5000)