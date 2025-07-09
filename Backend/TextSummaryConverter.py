import time

from sympy.strategies.core import switch
from transformers import T5Tokenizer, T5ForConditionalGeneration
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

model_name = "google-t5/t5-small"
tokenizer_t5small = T5Tokenizer.from_pretrained(model_name)
model_t5small = T5ForConditionalGeneration.from_pretrained(model_name)

model_longt5_name = "google/long-t5-tglobal-base"
tokenizer_longt5 = AutoTokenizer.from_pretrained(model_name)
model_longt5 = AutoModelForSeq2SeqLM.from_pretrained(model_name)

def summarize_text(text, model_name, summary_max_tokens = 100, summary_min_tokens = 30):
    tokenizer, model = get_tokenizer_and_model(model_name)

    model_limit = get_input_token_limit(model_name)
    input_length = len(text.split(' '))
    print(f"Tokens of the Text: {input_length}\n")
    if input_length > model_limit:
        print(f"Input is too large for {model_name}. The input will be truncated after the {model_limit}th token.")

    start_time = time.time()

    # T5 models are trained on a specific prefix for summarization tasks.
    preprocessed_text = "summarize: " + text
    # For clarification: here words are mapped to integers -> the lookup for the embedding is done in the model itself
    input_ids = tokenizer.encode(
        preprocessed_text,
        return_tensors='pt',
        max_length=model_limit,
        truncation=True
    )

    # outputs a tensor of shape [batch_size, sequence_length] -> integers that represent the summary
    summary_ids = model.generate(
        input_ids,
        min_length=summary_min_tokens,  # minimum tokens for the summary
        max_length=summary_max_tokens,  # maximum tokens for the summary
        num_beams=4,                    # higher more comp-cost, better quality
        no_repeat_ngram_size=2,         # repeating words are forbidden
        early_stopping=True
    )

    # Convert integers back to words, use the first
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    end_time = time.time()
    inference_time = end_time - start_time
    print(f"Inference time: {inference_time:.4f} seconds")
    return summary

def get_input_token_limit(model_name):
    match model_name:
        case "google-t5/t5-small":
            return 512
        case "google-t5/t5-base":
            return 512
        case "google/long-t5-tglobal-base":
            return 16384

def get_tokenizer_and_model(model_name):
    match model_name:
        case "google-t5/t5-small":
            return tokenizer_t5small, model_t5small
        case "google-t5/t5-base":
            return tokenizer_t5small, model_t5small
        case "google/long-t5-tglobal-base":
            return tokenizer_longt5, model_longt5