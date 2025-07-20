from .UrlTextConverter import extract_text_from_url
from .TextSummaryConverter import Summarizer

Summarizer_BartCnn = Summarizer("facebook/bart-large-cnn")

def summarize(url, min_length):
    print("extracting text from", url)
    text = extract_text_from_url(url)
    print("extracted text: ", text)
    summary = Summarizer_BartCnn.summarize_text(text, summary_max_tokens = min_length+20, summary_min_tokens = min_length)
    return summary
