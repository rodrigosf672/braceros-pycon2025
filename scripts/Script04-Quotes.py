import pandas as pd
import re

# Load your interview file
df = pd.read_csv("data/bracero_archive_interviews.csv")

# Define the 20 topic categories and keywords
topics_keywords = {
    "Trabajo agrícola": ["algodón", "pisca", "betabel", "tractor", "campo", "sembrar", "cosecha", "cultivo"],
    "Dinero y pagos": ["dinero", "pagar", "salario", "cheque", "ahorrar", "centavo", "dólar", "pago"],
    "Discriminación": ["no mexicanos", "no negros", "güeros", "discriminación", "anuncios", "protestar"],
    "Comida": ["comida", "papas", "carne", "frijoles", "cerveza", "alimentación", "almuerzo"],
    "Migración y cruces": ["mojado", "Juárez", "El Paso", "migración", "puente", "migratorio", "camiones"],
    "Contratos y leyes": ["contrato", "trocadero", "número", "papeles", "legal", "cartilla", "reclamo", "documento"],
    "Transporte": ["camión", "tren", "viaje", "ferrocarril", "camioneta", "traslado", "transporte"],
    "Familia": ["familia", "padres", "hermanos", "hijos", "mamá", "papá", "esposa"],
    "Educación": ["escuela", "enseñanza", "estudiar", "maestro", "educación"],
    "Trabajo en EE.UU.": ["trabajo", "gringo", "ranchero", "rancho", "empleado"],
    "Vida cotidiana": ["ropa", "casa", "iglesia", "tienda", "baño", "misa", "fiesta"],
    "Reclamos y quejas": ["robar", "injusto", "quejar", "exigir", "fraude", "corrupción", "protesta"],
    "Condiciones laborales": ["duro", "calor", "cansado", "enfermo", "horas", "descanso"],
    "Interacción con patrones": ["patrón", "gringo", "trato", "relación", "amable", "escogía"],
    "Experiencias positivas": ["contento", "gustaba", "bueno", "me fue bien", "agradable"],
    "Experiencias negativas": ["malo", "me fue mal", "problema", "difícil", "triste"],
    "Religión y cultura": ["iglesia", "misa", "católico", "fiesta", "tradición", "costumbre"],
    "Idioma y comunicación": ["inglés", "idioma", "hablar", "entender", "traducción"],
    "Organización y política": ["panista", "sinarquista", "partido", "justicia", "derechos"],
    "Mujeres y género": ["mujer", "esposa", "chavala", "sobrina", "niña"]
}

# Extract interviewee quotes
def extract_quotes(text):
    return re.findall(r'([A-Z]{2}):\s*(.*?)(?=\s+[A-Z]{2}:|$)', text + " ")

# Classify each quote
def classify_topic(quote):
    for topic, keywords in topics_keywords.items():
        if any(k in quote.lower() for k in keywords):
            return topic  # Return first matched topic only (or change to multiple if desired)
    return None  # Exclude unclassified

# Gather results
all_data = []

for _, row in df.iterrows():
    interviewee = row["Title"]
    interview_num = row["Record Number"]
    dialogue = row["Interview Text"]
    
    for speaker, quote in extract_quotes(dialogue):
        if speaker not in ["MP", "INT", "UNKNOWN"]:  # Interviewee only
            clean_quote = quote.strip()
            topic = classify_topic(clean_quote)
            if topic:  # Skip if unclassified
                all_data.append({
                    "Quote": clean_quote,
                    "Speaker": speaker,
                    "Interviewee": interviewee,
                    "Interview #": interview_num,
                    "Topic": topic
                })

# Create and export final DataFrame
df_output = pd.DataFrame(all_data)
df_output.to_csv("data/classified_bracero_quotes.csv", index=False)

print("File saved as 'data/classified_bracero_quotes.csv'")
