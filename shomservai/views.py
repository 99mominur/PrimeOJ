from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
import openai, os, json
from .models import Chat

# OpenAI configuration
openai.api_base = "https://api.pawan.krd/pai-001/v1"
openai.api_key = "pk-YZFZebclSEGbOuyaNAmSyEysUAyfKjhVtKdiJLPPyyFFXpaK"
# openai.api_key = os.getenv("pk-YZFZebclSEGbOuyaNAmSyEysUAyfKjhVtKdiJLPPyyFFXpaK")


def ask_openai(request, question):
    # Fetch recent chats (limit to last 10 for context)
    chats = Chat.objects.filter(user=request.user).order_by("-created_at")[:10]

    # Prepare the context for the AI
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant. Your name is ShomserVai. You are a english man, who only speaks in english",
        }
    ]
    for chat in reversed(chats):
        messages.extend(
            [
                {"role": "user", "content": chat.question},
                {"role": "assistant", "content": chat.response},
            ]
        )
    messages.append({"role": "user", "content": question})

    try:
        # Call the OpenAI API
        response = openai.ChatCompletion.create(
            model="pai-001",
            messages=messages,
        )
        if response.get("choices"):
            return response["choices"][0]["message"]["content"].strip()
        else:
            return "Sorry, I couldn't generate a valid response."
    except openai.error.RateLimitError:
        return "The server is currently overloaded. Please try again in a few minutes."
    except Exception as e:
        print(f"OpenAI API Error: {e}")
        return "An error occurred while processing your request."


@login_required
def history(request):
    chats = Chat.objects.filter(user=request.user).order_by("created_at")
    messages = []
    for chat in chats:
        messages.append({"role": "user", "content": chat.question})
        messages.append({"role": "assistant", "content": chat.response})
    return JsonResponse({"messages": messages})


@csrf_exempt
@login_required
def chatbot(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            question = body.get("message") + " In English please."

            if not question:
                return JsonResponse({"error": "Question cannot be empty"}, status=400)

            # Generate response
            response = ask_openai(request, question)

            # Save the chat and return the response
            if response:
                Chat.objects.create(
                    user=request.user, question=question, response=response
                )
                return JsonResponse(
                    {"response": {"role": "assistant", "content": response}}
                )
            else:
                return JsonResponse(
                    {"error": "Failed to generate response."}, status=500
                )
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format."}, status=400)
        except Exception as e:
            print(f"Chatbot Error: {e}")
            return JsonResponse({"error": "An unexpected error occurred."}, status=500)
    return JsonResponse({"error": "Invalid HTTP method."}, status=405)
