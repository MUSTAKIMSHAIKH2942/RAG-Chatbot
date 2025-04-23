from flask import Flask, render_template, request, jsonify
from rag import RAGPipeline

app = Flask(__name__)
rag_pipeline = RAGPipeline()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_query = request.form.get("query", "")
        response = rag_pipeline.query(user_query)
        return render_template("index.html", query=user_query, response=response)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)



# import os
# import sys
# from rag import RAGPipeline

# def clear_screen():
#     """Clear the console screen based on the operating system"""
#     os.system('cls' if os.name == 'nt' else 'clear')

# def print_banner():
#     """Display the application banner"""
#     clear_screen()
#     print("""
#     ██████╗  █████╗  ██████╗      ██████╗██╗  ██╗ █████╗ ████████╗██████╗  ██████╗ ██████╗ 
#     ██╔══██╗██╔══██╗██╔════╝     ██╔════╝██║  ██║██╔══██╗╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗
#     ██████╔╝███████║██║  ███╗    ██║     ███████║███████║   ██║   ██████╔╝██║   ██║██████╔╝
#     ██╔══██╗██╔══██║██║   ██║    ██║     ██╔══██║██╔══██║   ██║   ██╔══██╗██║   ██║██╔══██╗
#     ██║  ██║██║  ██║╚██████╔╝    ╚██████╗██║  ██║██║  ██║   ██║   ██║  ██║╚██████╔╝██████╔╝
#     ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝      ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═════╝ 
#     """)
#     print("Welcome to the RAG Chatbot!")
#     print("Type your questions and press Enter. Type 'quit' or 'exit' to end the session.\n")

# def main():
#     try:
#         print("Initializing RAG pipeline... (This may take a moment)")
#         rag_pipeline = RAGPipeline()
#         print("System ready!")
        
#         print_banner()
        
#         while True:
#             try:
#                 user_input = input("\nYou: ").strip()
                
#                 if user_input.lower() in ['quit', 'exit', 'q']:
#                     print("\nGoodbye!")
#                     break
                
#                 if not user_input:
#                     print("Please enter a question.")
#                     continue
                
#                 print("\nThinking...", end='\r')
#                 response = rag_pipeline.query(user_input)
#                 print(f"Bot: {response}")
                
#             except KeyboardInterrupt:
#                 print("\n\nUse 'quit' or 'exit' to end the session properly.")
#                 continue
#             except Exception as e:
#                 print(f"\nError: {str(e)}")
#                 print("Please try again or restart the application.")
#                 continue
                
#     except Exception as e:
#         print(f"\nFatal Error during initialization: {str(e)}")
#         print("Please check your configuration and try again.")
#         sys.exit(1)

# if __name__ == "__main__":
#     main()