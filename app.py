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
# The API key is loaded from the .env file automatically by the SDK
# However, we check for it explicitly for good measure.
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("FATAL: GEMINI_API_KEY not found in environment variables. Bot will be disabled.")
    gemini_client = None
else:
    try:
        gemini_client = genai.Client(api_key=GEMINI_API_KEY)
    except Exception as e:
        print(f"Error initializing Gemini client: {e}")
        gemini_client = None

# --- Application Routes ---

# Route for the Home page
@app.route("/")
def home():
    return render_template("home.html")

# Route for the Marketplace page
@app.route("/marketplace")
def marketplace():
    return render_template("marketplace.html")

# Route for the Complaint page
@app.route("/complain")
def complain():
    return render_template("complain.html")

# Route for the Educational Library page
@app.route("/library")
def library():
    return render_template("library.html")

# New route for the WasteBot page
@app.route("/wastebot")
def wastebot():
    return render_template("wastebot.html")

# New API route to handle the chat interaction
@app.route("/api/wastebot", methods=["POST"])
def api_wastebot():
    if not gemini_client:
        return jsonify({"error": "AI service is currently unavailable. Please check the API key."}), 503

    try:
        data = request.get_json()
        user_message = data.get("message")
        
        if not user_message:
            return jsonify({"error": "No message provided."}), 400

        # Define the system instruction for the bot
        system_instruction = (
            "You are the WasteWise Bot, an expert AI assistant focused on waste management, "
            "recycling, and sustainability. Your goal is to provide accurate, helpful, and "
            "actionable advice based on general best practices. Keep answers concise, informative, "
            "and encourage sustainable behavior. Do not respond to non-waste related topics."
        )

        # Generate the content using the specified model
        response = gemini_client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_message,
            config=genai.types.GenerateContentConfig(
                system_instruction=system_instruction
            )
        )

        return jsonify({"response": response.text})

    except APIError as e:
        # Handle specific API errors (e.g., authentication, rate limits)
        print(f"Gemini API Error: {e}")
        return jsonify({"error": "A service error occurred while contacting the AI model."}), 500
    except Exception as e:
        # Handle other internal server errors
        print(f"Internal Server Error: {e}")
        return jsonify({"error": "An internal error occurred."}), 500

if __name__ == "__main__":
    app.run(debug=True)