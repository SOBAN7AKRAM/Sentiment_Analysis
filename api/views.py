from django.shortcuts import render
from django.http import JsonResponse
from .ml_model import predict_sentiment
from django.views.decorators.csrf import csrf_exempt
import json
# Create your views here.

def index(request):
    return render(request, 'api/index.html')

@csrf_exempt
def sentiment_analysis(request):
    if request.method == "POST":
        # Extract input text from the request
        data = json.loads(request.body.decode('utf-8'))
        text = data.get('text', '')
        platform = data.get('platform', '')
        if not text or not platform:
            return JsonResponse({'error': 'No input text or platform provided'}, status=400)

        # Predict sentiment
        sentiment = predict_sentiment(text, platform)

        # Return the prediction
        return JsonResponse({'sentiment': sentiment}, status = 200)

    return JsonResponse({'error': 'Invalid request method'}, status=405)