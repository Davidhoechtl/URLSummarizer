import UrlTextConverter
import TextSummaryConverter

URL = "https://www.handelsblatt.com/finanzen/maerkte/marktberichte/dax-aktuell-dax-legt-auf-ueber-24500-punkte-zu-und-baut-rekord-aus/100140427.html"
URL = "https://de.wikipedia.org/wiki/Angela_Merkel"
URL = "https://docs.godotengine.org/en/stable/about/introduction.html"

text = UrlTextConverter.extract_text_from_url(URL)
print(text)
print()

summary_t5small = TextSummaryConverter.summarize_text(text, "google-t5/t5-small")
print("t5small: ", summary_t5small)
print()

summary_t5base= TextSummaryConverter.summarize_text(text, "google-t5/t5-base")
print("t5base: ", summary_t5base)
print()

summary_t5_long = TextSummaryConverter.summarize_text(text, "google/long-t5-tglobal-base")
print("t5_long: ", summary_t5_long)
print()
