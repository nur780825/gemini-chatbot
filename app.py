import os
from flask import Flask, jsonify, render_template, request
from google import genai

app = Flask(__name__)

# Render-এর Environment Variable থেকে API Key রিড করবে
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))


@app.route("/")
def home():
  return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
  user_message = request.json.get("message")
  if not user_message:
    return jsonify({"error": "No message provided"}), 400

  try:
    # জেমিনি মডেল আপডেট করে gemini-3.8-flash দেওয়া হলো
    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=user_message,
    )
    bot_reply = response.text
    return jsonify({"reply": bot_reply})
  except Exception as e:
    return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
