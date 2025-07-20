from flask import Flask, request, jsonify
from Pipeline import UrlSummaryPipeline

app = Flask(__name__)

@app.get("/healthCheck")
def get_healthCheck():
    return "Test", 200

@app.post("/summarize")
def convert_text_to_summary():
    data = request.get_json()

    if not data or 'Url' not in data or 'Min_Length' not in data:
        return jsonify({"error": "Missing 'Text' or 'Min_Length' in request"}), 400

    url = data['Url']
    min_length = int(data['Min_Length'])

    summary = UrlSummaryPipeline.summarize(url, min_length)
    return {'result': summary}, 200

if __name__ == '__main__':
    app.run(debug=True)