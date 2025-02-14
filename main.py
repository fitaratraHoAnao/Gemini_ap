from flask import Flask, request, jsonify
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = Flask(__name__)

@app.route('/gemini', methods=['GET', 'POST'])
def gemini():
    prompt = request.args.get('prompt')
    pdf_file = request.args.get('pdf_file')
    url_img = request.args.get('url_img')
    uid = request.args.get('uid')
    
    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400
    
    model = genai.GenerativeModel("gemini-2.0-flash")
    chat_session = model.start_chat()
    
    files = []
    if pdf_file:
        file = genai.upload_file(pdf_file, mime_type="application/pdf")
        files.append(file)
    if url_img:
        file = genai.upload_file(url_img, mime_type="image/jpeg")
        files.append(file)
    
    parts = files + [prompt]
    response = chat_session.send_message(parts)
    
    return jsonify({"response": response.text, "uid": uid})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
