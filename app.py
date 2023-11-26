from flask import Flask, render_template, request, jsonify
import requests
import base64

app = Flask(__name__)

API_URL = "https://xdwvg9no7pefghrn.us-east-1.aws.endpoints.huggingface.cloud"
API_KEY = "VknySbLLTUjbxXAXCjyfaFIPwUTCeRXbFSOjwRiCxsxFyhbnGjSFalPKrpvvDAaPVzWEevPljilLVDBiTzfIbWFdxOkYJxnOPoHhkkVGzAknaOulWggusSFewzpqsNWM"

headers = {
    "Accept": "image/png",
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

# Function to generate comic panel using the API
def generate_panel(text_input):
    payload = {"inputs": text_input}
    response = requests.post(API_URL, headers=headers, json=payload)
    image_data = base64.b64encode(response.content).decode('utf-8')
    return image_data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_comic', methods=['POST'])
def generate_comic():
    panels = []
    for i in range(1, 11):
        panel_text = request.form.get(f'panel{i}', '')
        if panel_text:
            panel_image = generate_panel(panel_text)
            panels.append({'text': panel_text, 'image': panel_image})

    return render_template('comic.html', panels=panels)

@app.errorhandler(Exception)
def handle_error(error):
    return jsonify(error=str(error)), 500

if __name__ == '__main__':
    app.run(debug=True)
