from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from langchain_openai import ChatOpenAI

from ..constants import OPENAI_API_BASEURL
from ..services.grourmet import get_shops


def dateplan_view(request: HttpRequest) -> HttpResponse:
    shop_ids = request.GET.getlist("shop_ids")
    shops = get_shops({"id": shop_ids})

    model = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        streaming=True,
        openai_api_base=OPENAI_API_BASEURL,
    )

    prompt = f"あなたはデートプランナーです。以下のお店を参考にして、デートプランを提案してください。\n\n - {shops[0]['name']} - {shops[0]['address']}\n - {shops[1]['name']} - {shops[1]['address']}\n - {shops[2]['name']} - {shops[2]['address']}\n\nデートプラン："

    response = model.invoke(prompt)
    print(response)

    context = {
        "shops": shops,
        "message": response,
    }

    return render(request, "pages/dateplan.html", context)
