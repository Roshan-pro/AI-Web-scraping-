# from langchain_ollama import OllamaLLM
# from langchain_core.prompts import ChatPromptTemplate
# template = (
#     "You are tasked with extracting specific information from the following text content: {dom_content}. "
#     "Please follow these instructions carefully: \n\n"
#     "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
#     "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
#     "3. **Empty Response:** If no information matches the description, return an empty string ('')."
#     "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
# )
# model=OllamaLLM(model="llama3")
# def parse_with_ollama(dom_chunks,parse_description):
#     prompt=ChatPromptTemplate.from_template(template)
#     chain=prompt | model
#     parsed_result=[]
    
#     for i,chunk in enumerate(dom_chunks,start=1):
#         response=chain.invoke({
#             "dom_content":chunk,"parse_description":parse_description
#         })
#         print(f"Parsed barch {i} of {len(dom_chunks)}")
#         parsed_result.append(response)
#     return "\n".join(parsed_result)
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")
genai.configure(api_key=API_KEY)
flash=genai.GenerativeModel("gemini-1.5-flash")
template = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully:\n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}.\n"
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response.\n"
    "3. **Empty Response:** If no information matches the description, return an empty string ('').\n"
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
)

def parse_with_gemini(dom_chunks, parse_description):
    parsed_result = []

    for i, chunk in enumerate(dom_chunks, start=1):
        # Fill in the prompt
        full_prompt = template.format(dom_content=chunk, parse_description=parse_description)

        # Generate response from Gemini
        response = flash.generate_content(contents=full_prompt)

        # Extract and store result
        result = response.text.strip() if hasattr(response, "text") else str(response)
        parsed_result.append(result)

        print(f"Parsed batch {i} of {len(dom_chunks)}")

    return "\n".join(parsed_result)

