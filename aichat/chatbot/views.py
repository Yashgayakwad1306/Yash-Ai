from django.shortcuts import render
from django.http import JsonResponse
from google import genai
from .models import ChatMessage

client = genai.Client()

def chat_home(request):
    if request.method == 'POST':
        user_message = request.POST.get('message', '')
        
        try:
            # 1. Fetch the LAST 5 chat messages from SQLite to use as memory
            # We order by '-created_at' to get the newest ones first, then reverse them
            past_chats = ChatMessage.objects.all().order_by('-created_at')[:5]
            past_chats = reversed(past_chats)

            # 2. Build a history log string for Gemini
            conversation_history = "You are a helpful AI assistant. Here is the recent conversation history for context:\n"
            
            for chat in past_chats:
                conversation_history += f"User: {chat.user_message}\n"
                conversation_history += f"Model: {chat.bot_response}\n"
            
            # 3. Append the current message to the history block
            full_prompt = f"{conversation_history}\nUser: {user_message}\nModel:"

            # 4. Send the combined prompt to Gemini
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=full_prompt,
            )
            bot_response = response.text
            
            # 5. Save the new message pair to SQLite
            ChatMessage.objects.create(
                user_message=user_message,
                bot_response=bot_response
            )
            
        except Exception as e:
            bot_response = "Oops! I ran into an error connecting to the AI."

        return JsonResponse({'response': bot_response})

    # For GET requests: Fetch all records to display on page reload
    history = ChatMessage.objects.all().order_by('created_at')
    return render(request, 'chatbot/chat.html', {'history': history})