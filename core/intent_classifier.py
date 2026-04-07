import json
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# Mapeamento de intenções (ajuste conforme suas FAQs)
INTENT_LABELS = [
    "compatibilidade", "pintura", "material", "break_light", "instalacao_furo",
    "instalacao_geral", "disponibilidade", "entrega_rapida", "instalacao_break_light",
    "preparacao_pintura", "instalar_sem_pintar", "garantia", "produto_novo",
    "fabricante", "retirar_fabrica", "desconto", "pagamento", "localizacao",
    "horario", "entrega", "frete_gratis", "adaptar", "entrega_fora_sp", "preco_fora_sp"
]

INTENT_TO_FAQ_ID = {
    "compatibilidade": "1",
    "pintura": "2",
    "material": "3",
    "break_light": "4",
    "instalacao_furo": "5",
    "instalacao_geral": "6",
    "disponibilidade": "7",
    "entrega_rapida": "8",
    "instalacao_break_light": "9",
    "preparacao_pintura": "10",
    "instalar_sem_pintar": "11",
    "garantia": "12",
    "produto_novo": "13",
    "fabricante": "14",
    "retirar_fabrica": "15",
    "desconto": "16",
    "pagamento": "17",
    "localizacao": "18",
    "horario": "19",
    "entrega": "20",
    "frete_gratis": "21",
    "adaptar": "22",
    "entrega_fora_sp": "23",
    "preco_fora_sp": "24"
}

# Carrega modelo BERTimbau (faça isso apenas uma vez)
tokenizer = AutoTokenizer.from_pretrained("neuralmind/bert-base-portuguese-cased")
model = AutoModelForSequenceClassification.from_pretrained(
    "neuralmind/bert-base-portuguese-cased",
    num_labels=len(INTENT_LABELS)
)

# Mapa de palavras-chave (seu dicionário KEYWORDS_MAP existente)
# Coloque aqui o dicionário completo que você já tinha
KEYWORDS_MAP = {
    "1": ["serve", "compativel", "modelo", "ano", "versao", "cabe", "meu carro", "funciona"],
    "2": ["pintura", "pintar", "pintado", "cor", "tinta", "voces pintam"],
    # ... complete com todas as outras palavras-chave
}

def classify_intent_bert(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)
    predicted_class = torch.argmax(probabilities, dim=-1).item()
    confidence = probabilities[0][predicted_class].item()
    if confidence > 0.7:
        return INTENT_LABELS[predicted_class], confidence
    return None, 0.0

def find_intent_by_keywords(text):
    """Busca intenção usando palavras-chave (já existente)."""
    text = text.lower()
    for numero, palavras in KEYWORDS_MAP.items():
        for palavra in palavras:
            if palavra in text:
                return numero
    return None