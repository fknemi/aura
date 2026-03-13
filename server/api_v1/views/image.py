from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
import json
from utils.gen import gen_image

@require_POST
def generate_image(request):
    try:
        body = json.loads(request.body)

        prompt = body.get("prompt")
        if not prompt:
            return JsonResponse({"error": "prompt is required"}, status=400)

        image_bytes = gen_image(
            prompt=prompt,
            style=body.get("style", ""),
            width=body.get("width", 1024),
            height=body.get("height", 1024),
            seed=body.get("seed", -1),
            enhance=body.get("enhance", False),
            negative_prompt=body.get("negative_prompt", ""),
            safe=body.get("safe", False),
            model=body.get("model", "flux"),
        )

        return HttpResponse(image_bytes, content_type="image/png")

    except json.JSONDecodeError:
        return JsonResponse({"error": "invalid JSON"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
