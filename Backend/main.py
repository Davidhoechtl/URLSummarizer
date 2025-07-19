import UrlSummaryPipeline

URL = "https://www.handelsblatt.com/finanzen/maerkte/marktberichte/dax-aktuell-dax-legt-auf-ueber-24500-punkte-zu-und-baut-rekord-aus/100140427.html"
#URL = "https://en.wikipedia.org/wiki/Angela_Merkel"
#URL = "https://docs.godotengine.org/en/stable/about/introduction.html"
#URL = "https://www.michaellaitman.com/science/why-are-we-here-what-is-the-meaning-of-life-why-do-we-exist-why-am-i-asking-these-questions/"
#URL = "https://club.autodoc.co.uk/magazin/how-does-clutch-work"
URL = "https://www.bbc.com/news/articles/c0m87d4p9gvo"
# URL = "https://en.wikipedia.org/wiki/Socrates"
URL = "https://www.bbc.com/news/articles/cy8ge7vllw9o"

summary = UrlSummaryPipeline.summarize(URL, min_length=50)
print(f"summary of {URL}: {summary}")