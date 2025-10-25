import os
import json
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from google import genai
from google.genai.errors import APIError

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# --- Gemini API Configuration ---
# API key setup for the WasteBot route
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
gemini_client = None
if GEMINI_API_KEY:
    try:
        gemini_client = genai.Client(api_key=GEMINI_API_KEY)
    except Exception as e:
        print(f"Error initializing Gemini client: {e}")

# --- Application Routes ---

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/marketplace")
def marketplace():
    return render_template("marketplace.html")

@app.route("/complain")
def complain():
    return render_template("complain.html")

@app.route("/library")
def library():
    return render_template("library.html")

@app.route("/wastebot")
def wastebot():
    return render_template("wastebot.html")

# New route for the Team page
@app.route("/team")
def team():
    return render_template("team.html")

# API route to handle the chat interaction
@app.route("/api/wastebot", methods=["POST"])
def api_wastebot():
    if not gemini_client:
        return jsonify({"error": "AI service is currently unavailable. Please check the API key."}), 503

    try:
        data = request.get_json()
        user_message = data.get("message")
        
        if not user_message:
            return jsonify({"error": "No message provided."}), 400

        system_instruction = (
            "You are the WasteWise Bot, an expert AI assistant focused on waste management, "
            "recycling, and sustainability. Your goal is to provide accurate, helpful, and "
            "actionable advice based on general best practices. Keep answers concise, informative, "
            "and encourage sustainable behavior. Do not respond to non-waste related topics."
        )

        response = gemini_client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_message,
            config=genai.types.GenerateContentConfig(
                system_instruction=system_instruction
            )
        )

        return jsonify({"response": response.text})

    except APIError as e:
        print(f"Gemini API Error: {e}")
        return jsonify({"error": "A service error occurred while contacting the AI model."}), 500
    except Exception as e:
        print(f"Internal Server Error: {e}")
        return jsonify({"error": "An internal error occurred."}), 500

if __name__ == "__main__":
    app.run(debug=True)