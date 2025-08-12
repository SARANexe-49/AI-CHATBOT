from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import google.generativeai as genai

# Initialize Flask App
app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

# Configure Gemini API
genai.configure(api_key="AIzaSyADRlLs6wPoTEgSxCP_ofixpatME9ZQxQY")  # ⚠️ Use your key securely in prod
model = genai.GenerativeModel("gemini-2.0-flash")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json.get("message", "")
    try:
        print(f"[User]: {user_msg}")
        response = model.generate_content(user_msg)
        full_text = response.parts[0].text.strip()

        # Split into parts for neat display
        parts = [p.strip() for p in full_text.split("\n\n") if p.strip()]
        if not parts:
            parts = [full_text]
    except Exception as e:
        parts = [f"⚠️ Error: {str(e)}"]
    return jsonify({"reply": parts})

if __name__ == "__main__":
    app.run(debug=True)
