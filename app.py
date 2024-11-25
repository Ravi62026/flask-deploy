from flask import Flask, request, jsonify
from flask_cors import cross_origin
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
# Explicitly enable CORS for your frontend domain
CORS(app)


class BNSAdvisor:
    def __init__(self):
        """Initialize the Google Gemini model with the API key."""
        api_key = "AIzaSyAEuC2MmuM83A-LsCffx5FoMwhmgGkadus"  # Replace with your actual API key

        # Configure the Gemini API client with the API key
        genai.configure(api_key=api_key)

        # Initialize both models
        self.model_flash = genai.GenerativeModel("gemini-1.5-flash")
        self.model_pro = genai.GenerativeModel("gemini-1.5-pro-002")

    def analyze_crime(self, crime_details: str):
        """Provide advice based on crime details using the new BNS system."""
        prompt = f"""
You are an expert in the Indian Judiciary System and an advisor specializing in the new laws introduced under the Bharatiya Nayay Sanhita (BNS), Bharatiya Nagarik Suraksha Sanhita (BNSS), and Bharatiya Sakshya Adhiniyam (BSA).

Your task is to advise users who are unaware of the new sections and terminologies. Based on the crime details provided, you should:
1. Identify the applicable BNS sections for the given crime and explain why it is applicable for the given crime.
2. Map these BNS sections to their previous IPC counterparts and just write the IPC sections for better understanding, Don't combine both IPC and BNS sections for confusion to users.
3. Mention the applicable BNSS sections (replacing the CrPC) if procedural aspects are involved.
4. Mention the applicable BSA sections (replacing the Indian Evidence Act) if evidentiary aspects are involved.
5. Include details about imprisonment, fines, or other punishments as per the BNS sections.

Ensure the advice is clear, detailed, and easily understandable for both lawpersons and legal professionals.

Input:
Crime Details: {crime_details}

Provide a structured, detailed response with legal clarity and practical advice.
"""
        try:
            # Generate content using the flash model
            response_flash = self.model_flash.generate_content(prompt)
            flash_text = response_flash.text.strip() if response_flash.text else "No response from flash model."

            # Generate content using the pro model
            response_pro = self.model_pro.generate_content(prompt)
            pro_text = response_pro.text.strip() if response_pro.text else "No response from pro model."

            # Combine the results
            combined_analysis = {
                "flash": flash_text,
                "pro": pro_text
            }

            # Return the combined advice
            return combined_analysis

        except Exception as e:
            return {"error": f"Error in analyzing crime: {str(e)}"}

    @staticmethod
    def format_to_points(text):
        """Convert paragraph text into a numbered list for better readability."""
        if text:
            return [f"{i + 1}. {line.strip()}" for i, line in enumerate(text.split("\n")) if line.strip()]
        return ["No details provided."]

# Initialize the advisor instance
advisor = BNSAdvisor()

@app.route("/analyze", methods=["POST"])
@cross_origin()
def analyze():
    """Endpoint to analyze crime details."""
    try:
        # Parse the incoming JSON request
        data = request.get_json()
        crime_details = data.get("crime_details", "")

        if not crime_details:
            return jsonify({"error": "Crime details are required."}), 400

        # Analyze the crime details
        results = advisor.analyze_crime(crime_details)

        if "error" in results:
            return jsonify({"error": results["error"]}), 500

        return jsonify(results)

    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


@app.route("/analyze_points", methods=["POST"])
@cross_origin()
def analyze_points():
    """Endpoint to analyze crime details and return the response in point-wise format."""
    try:
        # Parse the incoming JSON request
        data = request.get_json()
        crime_details = data.get("crime_details", "")

        if not crime_details:
            return jsonify({"error": "Crime details are required."}), 400

        # Analyze the crime details
        results = advisor.analyze_crime(crime_details)

        if "error" in results:
            return jsonify({"error": results["error"]}), 500

        # Convert the results to point-wise format
        formatted_results = {
            "flash": advisor.format_to_points(results["flash"]),
            "pro": advisor.format_to_points(results["pro"])
        }

        return jsonify(formatted_results)

    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


@app.route("/", methods=["GET"])
@cross_origin()
def home():
    """Home route to check API status."""
    return jsonify({"message": "BNS Advisor API is running."})