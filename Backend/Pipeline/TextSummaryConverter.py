import time
import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from transformers import PegasusForConditionalGeneration, PegasusTokenizer

def get_input_token_limit(model_name):
    match model_name:
        case "google-t5/t5-small":
            return 512
        case "google-t5/t5-base":
            return 512
        case "google/long-t5-tglobal-base":
            return 16384
        case "google/mt5-small":
            return 512
        case "google/pegasus-xsum":
            return 512
        case "google/bigbird-pegasus-large-bigpatent":
            return 4096
        case "facebook/bart-large-cnn":
            return 1024

def get_tokenizer_and_model(model_name):
    match model_name:
        case "google-t5/t5-small" | "google-t5/t5-base":
            t5_tokenizer = T5Tokenizer.from_pretrained(model_name)
            t5_model = T5ForConditionalGeneration.from_pretrained(model_name)
            return t5_tokenizer, t5_model
        case "google/long-t5-tglobal-base" | "google/mt5-small" | "facebook/bart-large-cnn":
            auto_tokenizer = AutoTokenizer.from_pretrained(model_name)
            model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
            return auto_tokenizer, model
        case "google/pegasus-xsum":
            peg_tokenizer = PegasusTokenizer.from_pretrained(model_name)
            peg_model = PegasusForConditionalGeneration.from_pretrained(model_name)
            return peg_tokenizer, peg_model

class Summarizer:
    def __init__(self, model_name):
        self.model_name = model_name
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        tokenizer, model = get_tokenizer_and_model(model_name)
        self.tokenizer = tokenizer
        self.model = model.to(self.device)


    def summarize_text(self, text, summary_max_tokens = 150, summary_min_tokens = 100):
        model_limit = get_input_token_limit(self.model_name)
        input_length = len(text.split(' '))
        print(f"Words of the Text: {input_length}\n")

        start_time = time.time()

        # chunk input and create summaries for each chunk
        chunks = self.chunk_input(text, model_limit, stride=100)
        summaries = []
        for chunk in chunks:
            max_len_of_summary = int(model_limit / 3)
            chunk_summary = self.text_to_summary(chunk, model_limit, max_len_of_summary, 60)
            summaries.append(chunk_summary)
            print(chunk_summary+"\n")

        final = summaries[0]
        if len(summaries) > 1:
            joined = " ".join(summaries)
            tokens = self.text_to_tokens(joined, model_limit)
            if len(tokens[0]) > model_limit:
                final = self.summarize_text(joined, summary_max_tokens, summary_min_tokens) # still too long -> recursive call
            else:
                final = self.text_to_summary(tokens, model_limit, summary_max_tokens, summary_min_tokens) # final summarization

        end_time = time.time()
        inference_time = end_time - start_time
        print(f"Inference time: {inference_time:.4f} seconds")
        return final

    def text_to_summary(self, input_ids, model_input_limit, summary_max_tokens, summary_min_tokens):
        # T5 models are trained on a specific prefix for summarization tasks.
        #preprocessed_text = "summarize: " + text

        # outputs a tensor of shape [batch_size, sequence_length] -> integers that represent the summary
        summary_ids = self.model.generate(
            input_ids,
            min_length=summary_min_tokens,  # minimum tokens for the summary
            max_length=summary_max_tokens,  # maximum tokens for the summary
            num_beams=4,  # higher more comp-cost, better quality
            no_repeat_ngram_size=3,  # repeating words are forbidden
            early_stopping=True
        )

        # Convert integers back to words, use the first
        summary = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        return summary

    def chunk_input(self, text, max_length, stride=0, minimal_chunk_size=100):
        tokens = self.text_to_tokens(text, max_length)[0]
        print("Chunking text (tokens: ", len(tokens))
        chunks = []
        for i in range(0, len(tokens), max_length - stride):
            if i + max_length <= len(tokens):
                chunk_tokens = tokens[i:i + max_length]  # substring from pos i to i + max_length
            else:
                chunk_tokens = tokens[i:]
                if len(chunk_tokens) < minimal_chunk_size:
                    break  # iscard chunk because it is too small

            chunks.append(chunk_tokens.unsqueeze(0))  # <-- Add batch dimension here
        return chunks

    def text_to_tokens(self, text, max_length):
        return self.tokenizer(text, return_tensors="pt", max_length=max_length, truncation=False)["input_ids"].to(self.device)


