import pandas as pd
import re
import nltk
import os
from collections import defaultdict
from sklearn.feature_extraction.text import CountVectorizer
from bertopic import BERTopic
from sentence_transformers import SentenceTransformer
from nltk.corpus import stopwords

# Download stopwords if needed
nltk.download("stopwords")
stop_words = set(stopwords.words("english") + stopwords.words("spanish"))

# Step 1: Load data
df = pd.read_csv("data/bracero_archive_interviews.csv")

# Step 2: Preprocess text
def preprocess(text):
    text = re.sub(r"[^\w\s]", "", text)
    text = text.lower().strip()
    return " ".join([word for word in text.split() if word not in stop_words])

sentences = []
orig_sentences = []
for text in df["Interview Text"].dropna():
    for sentence in re.split(r"[.!?]", text):
        clean = preprocess(sentence)
        if clean and len(clean.split()) > 5:
            sentences.append(clean)
            orig_sentences.append(sentence.strip())

# Step 3: Define bilingual predefined topics
target_topics = {
    "Background / Antecedentes": [
        "born", "family", "parents", "grew up", "childhood", "siblings", "origin", "hometown", "birthplace", "education",
        "nacido", "familia", "padres", "infancia", "hermanos", "origen", "pueblo natal", "lugar de nacimiento", "educación"
    ],
    "Migration Motivation / Motivación para migrar": [
        "migrated", "migration", "bracero program", "motivation", "job opportunity", "work prospects", "poverty", "godfather", "decision to migrate", "contract",
        "migró", "migración", "programa bracero", "motivación", "oportunidad de trabajo", "pobreza", "compadre", "decisión de migrar", "contrato"
    ],
    "Labor Experiences / Experiencias laborales": [
        "worked", "labor", "fields", "job", "hours", "tasks", "agriculture", "crops", "beets", "celery", "cotton", "tomatoes", "soybeans",
        "trabajó", "labor", "campos", "empleo", "horas", "tareas", "agricultura", "cultivos", "betabel", "apio", "algodón", "tomates", "soya"
    ],
    "Living Conditions / Condiciones de vida": [
        "housing", "living", "food", "meal", "bunk", "quarters", "room", "accommodations", "sanitation", "daily routine",
        "vivienda", "alojamiento", "comida", "alimentos", "litera", "cuarto", "condiciones", "higiene", "rutina diaria"
    ],
    "Challenges and Discrimination / Discriminación y dificultades": [
        "discrimination", "difficulties", "challenges", "struggle", "issues", "racism", "exploitation", "prejudice", "unfair treatment",
        "discriminación", "dificultades", "retos", "lucha", "problemas", "racismo", "explotación", "prejuicio", "trato injusto"
    ],
    "Violence / Violencia": [
        "beat", "beaten", "violence", "abuse", "harass", "hit", "punish", "injury", "conflict", "guard", "confrontation",
        "golpear", "golpeado", "violencia", "abuso", "acosar", "herir", "castigar", "conflicto", "guardia", "confrontación"
    ],
    "Return and Reflections / Retorno y reflexiones": [
        "return", "reflect", "thoughts", "life after", "impact", "reminisce", "changes", "conclusions", "pride", "legacy",
        "regreso", "reflexión", "pensamientos", "vida después", "impacto", "rememorar", "cambios", "conclusiones", "orgullo", "legado"
    ]
}

# Step 4: Assign predefined topic
def categorize_sentence(sentence):
    for topic, keywords in target_topics.items():
        if any(k in sentence.lower() for k in keywords):
            return topic
    return "Other"

predefined_labels = [categorize_sentence(s) for s in orig_sentences]

# Step 5: Create DataFrame
df_sentences = pd.DataFrame({
    "Original Sentence": orig_sentences,
    "Cleaned Sentence": sentences,
    "Predefined Topic": predefined_labels
})

# Step 6: Train BERTopic
embedding_model = SentenceTransformer("distiluse-base-multilingual-cased-v2")
vectorizer_model = CountVectorizer(stop_words=list(stop_words))
topic_model = BERTopic(embedding_model=embedding_model,
                       vectorizer_model=vectorizer_model,
                       verbose=True)
topics, probs = topic_model.fit_transform(sentences)
df_sentences["BERTopic Topic"] = topics
df_sentences["Topic Probability"] = probs

# Step 7: Rename BERTopic topic labels (optional)
topic_names = {}
for topic_num in df_sentences["BERTopic Topic"].unique():
    words = topic_model.get_topic(topic_num)
    if words:
        label = ", ".join([w[0] for w in words[:3]])
        topic_names[topic_num] = f"{topic_num}: {label}"
topic_model.set_topic_labels([topic_names.get(i, f"Topic {i}") for i in range(len(topic_names))])

# Step 8: Save results
df_sentences.to_csv("data/detailed_bracero_topics.csv", index=False)

# Step 9: Save CSVs per Predefined Topic
os.makedirs("predefined_topics", exist_ok=True)
for topic in df_sentences["Predefined Topic"].unique():
    df_sentences[df_sentences["Predefined Topic"] == topic]\
        .to_csv(f"data/predefined_topics/{topic.replace(' ', '_').replace('/', '').lower()}.csv", index=False)

# Step 10: Keyword counts per predefined topic
rows = []
for topic, keywords in target_topics.items():
    subset = df_sentences[df_sentences["Predefined Topic"] == topic]
    for k in keywords:
        count = subset["Original Sentence"].str.lower().str.count(rf"\b{k.lower()}\b").sum()
        if count > 0:
            rows.append({"Predefined Topic": topic, "Keyword": k, "Count": int(count)})
df_keywords = pd.DataFrame(rows).sort_values(["Predefined Topic", "Count"], ascending=[True, False])
df_keywords.to_csv("data/bracero_topic_keyword_counts.csv", index=False)

# Step 11: Save visualizations
topic_model.visualize_topics().write_html("output/topics_overview.html")
topic_model.visualize_barchart(top_n_topics=20).write_html("output/top20_topics_barchart.html")
topic_model.visualize_hierarchy().write_html("output/topic_hierarchy.html")

print("All topic files, keyword counts, and visualizations saved.")
