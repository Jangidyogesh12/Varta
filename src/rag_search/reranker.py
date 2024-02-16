import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Load pre-trained cross-encoder model
cross_encoder_model_name = "distilbert-base-uncased"
cross_encoder_tokenizer = AutoTokenizer.from_pretrained(cross_encoder_model_name)
cross_encoder_model = AutoModelForSequenceClassification.from_pretrained(
    cross_encoder_model_name
)


# Assuming your get_chunk_from_database returns a list of paragraphs
def rerank(query, paragraphs, k=5):
    # Prepare inputs for the cross-encoder
    inputs = [(query, paragraph[0][0]) for paragraph in paragraphs]
    tokenized_inputs = cross_encoder_tokenizer.batch_encode_plus(
        inputs, return_tensors="pt", pad_to_max_length=True
    )

    # Run cross-encoder model forward pass
    with torch.no_grad():
        logits = cross_encoder_model(**tokenized_inputs).logits

    # Compute relevance scores (you may need to adjust this depending on your model output)
    relevance_scores = torch.sigmoid(logits[:, 1])

    # Combine paragraphs with relevance scores
    reranked_paragraphs = list(zip(paragraphs, relevance_scores))

    # Sort paragraphs by relevance scores in descending order
    reranked_paragraphs = sorted(reranked_paragraphs, key=lambda x: x[1], reverse=True)

    # Return reranked paragraphs without relevance scores
    return [paragraph for paragraph, _ in reranked_paragraphs[:k]]
