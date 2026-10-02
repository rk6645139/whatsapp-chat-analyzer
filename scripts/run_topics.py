from src.parser import parse_whatsapp_chat
from src.preprocessing import preprocess_messages
from src.topics import (
    prepare_topic_text,
    create_tfidf_matrix,
    perform_kmeans,
    get_cluster_keywords,
    calculate_silhouette_score
)


df = parse_whatsapp_chat(
    "data/chat.txt"
)

df = preprocess_messages(df)

texts = prepare_topic_text(df)

print("Number of messages:", len(texts))

vectorizer, matrix = create_tfidf_matrix(
    texts
)

print(
    "TF-IDF matrix shape:",
    matrix.shape
)

model, labels = perform_kmeans(
    matrix,
    n_clusters=5
)

print(
    "Number of clusters:",
    len(set(labels))
)

keywords = get_cluster_keywords(
    model,
    vectorizer,
    top_n=10
)

print("\nCluster Keywords:")

for cluster_id, words in keywords.items():

    print(
        f"Cluster {cluster_id}:",
        ", ".join(words)
    )

score = calculate_silhouette_score(
    matrix,
    labels
)

print(
    "\nSilhouette Score:",
    score
)
