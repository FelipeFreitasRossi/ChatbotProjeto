import random
from datetime import datetime

def obter_saudacao():
    hora = datetime.now().hour
    if 5 <= hora < 12:
        return "Bom dia"
    elif 12 <= hora < 18:
        return "Boa tarde"
    else:
        return "Boa noite"

class PersonalityEngine:
    def __init__(self, style="professional_friendly"):
        self.style = style
        self.last_response_type = None
        self.templates = {
            "greeting": [
                "{saudacao}! Bem-vindo(a) à {empresa}. Como posso ajudar?",
                "{saudacao}! Que bom ter você por aqui. Em que posso ser útil hoje?",
                "{saudacao}! Sou o assistente virtual da {empresa}. Diga como posso te ajudar!",
            ],
            "unknown": [
                "Hmm, não entendi bem. Pode reformular sua pergunta?",
                "Desculpe, não consegui compreender. Poderia tentar de outra forma?",
                "Não tenho certeza se entendi... Pode me explicar melhor?",
            ],
            "farewell": [
                "Foi um prazer ajudar! Até a próxima.",
                "Obrigado pelo contato! Estamos à disposição.",
                "Qualquer outra dúvida, é só chamar. Tenha um ótimo dia!",
            ],
        }
    
    def get_response(self, response_type, **kwargs):
        templates = self.templates.get(response_type, ["{message}"])
        template = random.choice(templates)
        if self.last_response_type == response_type and len(templates) > 1:
            template = random.choice([t for t in templates if t != template])
        self.last_response_type = response_type
        return template.format(**kwargs)