import os
from dotenv import load_dotenv
import json
import openai
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings

client = openai.OpenAI(
    api_key=os.getenv('OPENAI_API_KEY'),
    base_url=os.getenv('OPENAI_BASE_URL')
)
PROMPT_FILE_PATH = os.path.join(settings.BASE_DIR, 'config', 'prompt.json')

# Load the JSON file containing system messages
def load_prompts():
    with open(PROMPT_FILE_PATH, "r") as file:
        return json.load(file)

# Load the system messages at runtime
prompts = load_prompts()

@csrf_exempt
def medical_chatbot(request):
    if request.method == 'POST':
        user_query = request.POST.get('query')
        
        try:
            # Determine the appropriate system message (default if no specific match)
            system_message = prompts.get("default")  # Default role
            
            # Example of dynamic behavior: choose a different persona based on query
            if "mental health" in user_query.lower():
                system_message = prompts.get("mental_health", system_message)
            elif "diet" in user_query.lower():
                system_message = prompts.get("diet_advice", system_message)
            
            # Include the user's query
            user_message = {"role": "user", "content": user_query}
            
            # Call GPT-4 API with persona definition
            response = client.chat.completions.create(
                model="gemini-2.0-flash-exp",
                messages=[system_message, user_message]
            )
            
            # Extract the bot's reply
            bot_reply = response.choices[0].message.content  # Correct access path
            return JsonResponse({'reply': bot_reply})
        
        except Exception as e:
            return JsonResponse({'reply': str(e)}, status=500)
    
    return JsonResponse({'reply': 'Invalid request.'}, status=400)
