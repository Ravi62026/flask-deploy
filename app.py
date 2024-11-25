# from flask import Flask, request, jsonify
# from flask_cors import cross_origin
# from flask_cors import CORS
# import google.generativeai as genai

# app = Flask(__name__)
# # Explicitly enable CORS for your frontend domain
# CORS(app)


# class BNSAdvisor:
#     def __init__(self):
#         """Initialize the Google Gemini model with the API key."""
#         # api_key = "AIzaSyAEuC2MmuM83A-LsCffx5FoMwhmgGkadus"  # Replace with your actual API key
#         api_key = "AIzaSyCACbv1JwayclRi6RDRNkC_Ho6RtJy63a4"  # Replace with your actual API key

#         # Configure the Gemini API client with the API key
#         genai.configure(api_key=api_key)

#         # Initialize both models
#         self.model_flash = genai.GenerativeModel("gemini-1.5-flash")
#         self.model_pro = genai.GenerativeModel("gemini-1.5-pro-002")

#     def analyze_crime(self, crime_details: str):
#         """Provide advice based on crime details using the new BNS system."""
#         prompt = f"""
# You are an expert in the Indian Judiciary System and an advisor specializing in the new laws introduced under the Bharatiya Nayay Sanhita (BNS), Bharatiya Nagarik Suraksha Sanhita (BNSS), and Bharatiya Sakshya Adhiniyam (BSA).

# Your task is to advise users who are unaware of the new sections and terminologies. Based on the crime details provided, you should:
# 1. Identify the applicable BNS sections for the given crime and explain why it is applicable for the given crime.
# 2. Map these BNS sections to their previous IPC counterparts and just write the IPC sections for better understanding, Don't combine both IPC and BNS sections for confusion to users.
# 3. Mention the applicable BNSS sections (replacing the CrPC) if procedural aspects are involved.
# 4. Mention the applicable BSA sections (replacing the Indian Evidence Act) if evidentiary aspects are involved.
# 5. Include details about imprisonment, fines, or other punishments as per the BNS sections.

# Ensure the advice is clear, detailed, and easily understandable for both lawpersons and legal professionals.

# Input:
# Crime Details: {crime_details}

# Provide a structured, detailed response with legal clarity and practical advice.
# """
#         try:
#             # Generate content using the flash model
#             response_flash = self.model_flash.generate_content(prompt)
#             flash_text = response_flash.text.strip() if response_flash.text else "No response from flash model."

#             # Generate content using the pro model
#             response_pro = self.model_pro.generate_content(prompt)
#             pro_text = response_pro.text.strip() if response_pro.text else "No response from pro model."

#             # Combine the results
#             combined_analysis = {
#                 "flash": flash_text,
#                 "pro": pro_text
#             }

#             # Return the combined advice
#             return combined_analysis

#         except Exception as e:
#             return {"error": f"Error in analyzing crime: {str(e)}"}

#     @staticmethod
#     def format_to_points(text):
#         """Convert paragraph text into a numbered list for better readability."""
#         if text:
#             return [f"{i + 1}. {line.strip()}" for i, line in enumerate(text.split("\n")) if line.strip()]
#         return ["No details provided."]

# # Initialize the advisor instance
# advisor = BNSAdvisor()

# @app.route("/analyze", methods=["POST"])
# @cross_origin()
# def analyze():
#     """Endpoint to analyze crime details."""
#     try:
#         # Parse the incoming JSON request
#         data = request.get_json()
#         crime_details = data.get("crime_details", "")

#         if not crime_details:
#             return jsonify({"error": "Crime details are required."}), 400

#         # Analyze the crime details
#         results = advisor.analyze_crime(crime_details)

#         if "error" in results:
#             return jsonify({"error": results["error"]}), 500

#         return jsonify(results)

#     except Exception as e:
#         return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


# @app.route("/analyze_points", methods=["POST"])
# @cross_origin()
# def analyze_points():
#     """Endpoint to analyze crime details and return the response in point-wise format."""
#     try:
#         # Parse the incoming JSON request
#         data = request.get_json()
#         crime_details = data.get("crime_details", "")

#         if not crime_details:
#             return jsonify({"error": "Crime details are required."}), 400

#         # Analyze the crime details
#         results = advisor.analyze_crime(crime_details)

#         if "error" in results:
#             return jsonify({"error": results["error"]}), 500

#         # Convert the results to point-wise format
#         formatted_results = {
#             "flash": advisor.format_to_points(results["flash"]),
#             "pro": advisor.format_to_points(results["pro"])
#         }

#         return jsonify(formatted_results)

#     except Exception as e:
#         return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


# @app.route("/", methods=["GET"])
# @cross_origin()
# def home():
#     """Home route to check API status."""
#     return jsonify({"message": "BNS Advisor API is running."})

# if __name__ == "__main__":
#     app.run(debug=True, port = 8000)







from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_cors import cross_origin
import google.generativeai as genai
from typing import Dict




app = Flask(__name__)
CORS(app)


class LegalCaseAnalyzer:
    def __init__(self):
        """Initialize the Google Gemini model with the API key."""
        # api_key = os.getenv('GOOGLE_API_KEY')  # Get API key from environment variable
        api_key = "AIzaSyAEuC2MmuM83A-LsCffx5FoMwhmgGkadus"
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set")
            
        genai.configure(api_key=api_key)
        self.model_flash = genai.GenerativeModel("gemini-1.5-flash")
        self.model_pro = genai.GenerativeModel("gemini-1.5-pro-002")

    def analyze_case(self, case_description: str) -> Dict:
        """Analyze a legal case by combining responses from two models."""
        prompt = f"""You are a seasoned legal expert tasked with providing an extensive, structured breakdown of arguments for both the plaintiff's and the defendant's advocates in a high level of debate between 2 senior lawyer in high court, and provided section in both ipc and bns . This analysis should be detailed, using legal reasoning suitable for those without legal representation, and should provide insightful guidance.

For 3 round of argument between the plaintiff's and the defendant's advocates, provide the following structured details for each side in atleast 5 points for each structured details, specially for supporting evidence and section and act:

1. **Legal Claims and Defenses**:
   - Outline the primary legal claims, defenses, and rights each side is asserting.
   - Reference relevant acts, laws, and sections that support each argument.
   - Ensure each claim or defense is well-explained to clarify its legal standing.

2. **Supporting Evidence and its Relevance**:
   - List and describe specific types of evidence (e.g., witness testimony, physical evidence, digital records) that support each claim or defense.
   - Explain how each piece of evidence strengthens the advocate's position and its potential impact on the court’s perspective.

3. **Landmark Judgments and Precedents**:
   - Include 5-8 high-profile judgments and legal precedents from similar cases.
   - For each precedent, provide a brief summary and explain its relevance to the current case.
   - Discuss how these judgments support the advocate's argument or establish a relevant legal principle.

4. **Counterarguments and Rebuttals**:
   - Respond directly to the opposing advocate’s points, addressing weaknesses or inconsistencies in their claims.
   - Use legal principles or evidence to counter the other side’s arguments effectively.

5. **Potential Legal Outcomes and Consequences**:
   - Describe the legal consequences and possible outcomes if each side’s arguments are upheld.
   - Discuss both immediate legal implications (e.g., penalties, fines) and long-term consequences (e.g., criminal records, civil liabilities).

Each advocate should respond directly to the previous argument made by the opposing side, attempting to refute or strengthen their case with additional points. Ensure that each round of argument is detailed, precise, and labeled clearly.

Case Description:
{case_description}

Please ensure the analysis is comprehensive and structured, offering a full view of the strengths and weaknesses of each side’s case through a high level of debate between 2 senior lawyer in high court. Present the arguments in a way that is both educational and actionable for someone without legal representation."""

        try:
            # Generate content using both models
            response_flash = self.model_flash.generate_content(prompt)
            flash_text = response_flash.text.strip() if response_flash.text else "No response from flash model."

            response_pro = self.model_pro.generate_content(prompt)
            pro_text = response_pro.text.strip() if response_pro.text else "No response from pro model."

            return {
                "success": True,
                "flash_analysis": flash_text,
                "pro_analysis": pro_text
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

# Initialize the analyzer
try:
    analyzer = LegalCaseAnalyzer()
except ValueError as e:
    print(f"Error initializing analyzer: {e}")
    exit(1)

@app.route('/api/analyze', methods=['POST'])
@cross_origin()
def analyze_case():
    """API endpoint to analyze a legal case."""
    if not request.is_json:
        return jsonify({"success": False, "error": "Content-Type must be application/json"}), 400

    data = request.get_json()
    case_description = data.get('caseDescription')
    
    if not case_description:
        return jsonify({"success": False, "error": "Case description is required"}), 400

    result = analyzer.analyze_case(case_description)
    print(result)
    return jsonify(result)

@app.route('/', methods=['GET'])
@cross_origin()
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "healthy"})

@app.route('/api/formatted-analyze', methods=['POST'])
@cross_origin()
def formatted_analyze_case():
    if not request.is_json:
        return jsonify({"success": False, "error": "Content-Type must be application/json"}), 400

    data = request.get_json()
    case_description = data.get('caseDescription')
    
    if not case_description:
        return jsonify({"success": False, "error": "Case description is required"}), 400

    result = analyzer.analyze_case(case_description)
    
    if not result.get("success"):
        return jsonify(result), 500

    flash_analysis = result.get("flash_analysis", "No Flash Analysis Found")
    pro_analysis = result.get("pro_analysis", "No Pro Analysis Found")

    formatted_response = {
        "success": result.get("success"),
        "formatted_flash_analysis": f"Flash Analysis:\n{flash_analysis}",
        "formatted_pro_analysis": f"Pro Analysis:\n{pro_analysis}"
    }

    return jsonify(formatted_response)

@app.route('/api/point-analyze', methods=['POST'])
@cross_origin()
def point_analyze_case():
    """API endpoint to analyze a legal case and provide a point-wise formatted response."""
    if not request.is_json:
        return jsonify({"success": False, "error": "Content-Type must be application/json"}), 400

    data = request.get_json()
    case_description = data.get('caseDescription')
    
    if not case_description:
        return jsonify({"success": False, "error": "Case description is required"}), 400

    result = analyzer.analyze_case(case_description)
    
    if not result.get("success"):
        return jsonify(result), 500

    flash_analysis = result.get("flash_analysis", "No Flash Analysis Found")
    pro_analysis = result.get("pro_analysis", "No Pro Analysis Found")

    # Function to convert text into a point-wise format
    def format_into_points(text: str) -> str:
        lines = text.split('\n')
        formatted_lines = [f"{i+1}. {line.strip()}" for i, line in enumerate(lines) if line.strip()]
        return "\n".join(formatted_lines)

    formatted_flash_points = format_into_points(flash_analysis)
    formatted_pro_points = format_into_points(pro_analysis)

    point_formatted_response = {
        "success": result.get("success"),
        "point_formatted_flash_analysis": formatted_flash_points,
        "point_formatted_pro_analysis": formatted_pro_points
    }
    
    print(point_formatted_response)

    return jsonify(point_formatted_response)



# if __name__ == '__main__':
#     port = int(os.getenv('PORT', 5000))
#     debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
#     app.run(host='0.0.0.0', port=port)