import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from .chatbot_service import diagnose_structured


@ensure_csrf_cookie
def chat_page(request):
    return render(request, "enduser/chatbot/chatbot.html")


def chat_api(request):

    if request.method == "POST":

        try:
            data = json.loads(request.body)
        except Exception:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        message = (data.get("message") or "").strip()
        if not message:
            return JsonResponse({"error": "Missing message"}, status=400)

        response = diagnose_structured(message)
        
        print(response)

        return JsonResponse({"reply": response})

    return JsonResponse({"reply": "Method not allowed"}, status=405)
