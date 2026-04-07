import spacy
import re

# Carrega modelo de língua portuguesa
nlp = spacy.load("pt_core_news_lg")

# Dicionário de sinônimos e gírias
SLANG_DICT = {
    "serve": ["compatível", "cabe", "funciona", "encache", "encaixa", "dá", "presta"],
    "carro": ["veículo", "automóvel", "viatura", "possante", "nave", "carrão"],
    "modelo": ["versão", "tipo", "ano"],
    "pintura": ["pintar", "pintado", "cor", "tinta", "verniz"],
    "pintar": ["pintura", "envernizar", "laquear"],
    "material": ["feito", "composição", "fibra", "abs", "plástico", "carbono"],
    "fabricado": ["feito", "produzido", "confeccionado", "manufaturado"],
    "break": ["brake", "freio", "luz", "led", "terceira", "sinaleira"],
    "fura": ["furo", "perfura", "broca", "parafuso", "drill"],
    "instalação": ["instalar", "montagem", "colocar", "fixar", "pôr", "botar"],
    "garantia": ["defeito", "cobertura", "validade", "reclamação", "problema"],
    "desconto": ["abatimento", "promoção", "barato", "negociar", "chorar"],
    "pagamento": ["pagar", "parcela", "cartão", "boleto", "pix", "dinheiro"],
    "à vista": ["avista", "a vista", "pix", "dinheiro"],
}

def simple_spell_check(text):
    corrections = {
        r'\b(voce|vc|voc)\b': 'você',
        r'\b(nao|n)\b': 'não',
        r'\b(pq|porq|por que)\b': 'porque',
        r'\b(aki)\b': 'aqui',
        r'\b(tbm|tb)\b': 'também',
        r'\b(q|k)\b': 'que',
        r'\b(blz)\b': 'beleza',
        r'\b(obg|obrigado)\b': 'obrigado',
        r'\b(airfoil|aerofolio)\b': 'aerofólio',
        r'\b(breik|luz de freio)\b': 'break light',
        r'\b(garatia)\b': 'garantia',
    }
    corrected = text.lower()
    for pattern, replacement in corrections.items():
        corrected = re.sub(pattern, replacement, corrected)
    return corrected

def expand_query_with_synonyms(text):
    text_lower = text.lower()
    expanded_words = set(text_lower.split())
    for word in text_lower.split():
        if word in SLANG_DICT:
            expanded_words.update(SLANG_DICT[word])
    return ' '.join(expanded_words)