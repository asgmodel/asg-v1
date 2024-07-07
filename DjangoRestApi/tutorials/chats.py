"""
At the command line, only need to run once to install the package via pip:

$ pip install google-generativeai
# """

# import google.generativeai as genai

# genai.configure(api_key="AIzaSyAH1b1v0_TB0IpoIRgPXMJZbwLV5TUFhf8")

# # Set up the model
# generation_config = {
#   "temperature": 0.9,
#   "top_p": 1,
#   "top_k": 1,
#   "max_output_tokens": 8192,
# }

# safety_settings = [
# ]

# model = genai.GenerativeModel(model_name="tunedModels/asgprompt-3s1ptug4v507",
#                               generation_config=generation_config,
#                               safety_settings=safety_settings)
import requests
def ask_api(text):
    try:
        url="https://wasmfw.pythonanywhere.com/todos/api"
        payload = {
            	"_content": text

        }
        response = requests.post(url, json=payload)

        # response = requests.post(url,txt)

        return response.json()['answer']
    except:
        return text

def  ask_ai(text=""):
    return ask_api(text)

