import UrlTextConverter
import TextSummaryConverter

URL = "https://www.handelsblatt.com/finanzen/maerkte/marktberichte/dax-aktuell-dax-legt-auf-ueber-24500-punkte-zu-und-baut-rekord-aus/100140427.html"
#URL = "https://en.wikipedia.org/wiki/Angela_Merkel"
#URL = "https://docs.godotengine.org/en/stable/about/introduction.html"
#URL = "https://www.michaellaitman.com/science/why-are-we-here-what-is-the-meaning-of-life-why-do-we-exist-why-am-i-asking-these-questions/"
#URL = "https://club.autodoc.co.uk/magazin/how-does-clutch-work"
#URL = "https://theengineeringblog.com/cylinders-basics-of-desing-function-and-construction/"

text = UrlTextConverter.extract_text_from_url(URL)
print(text)
print()
#
# summary_t5small = TextSummaryConverter.summarize_text(text, "google-t5/t5-small")
# print("t5small: ", summary_t5small)
# print()
#

# summary_pegasus = TextSummaryConverter.summarize_text(text, "google/pegasus-xsum")
# print("pegasus-xsum: ", summary_pegasus)
# print()

summary_bart_large_cnn = TextSummaryConverter.summarize_text(text, "facebook/bart-large-cnn")
print("pegasus-xsum: ", summary_bart_large_cnn)
print()