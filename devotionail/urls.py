"""
URL configuration for devotionail project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from groq import Groq
from django.conf import settings
# devotionail/urls.py
from django.contrib import admin
from django.http import HttpResponse
from django.urls import path

client = Groq(
    api_key=settings.GROQ_API_KEY
)


def hello(request):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "Explain the importance of low latency LLMs, explain it in the voice of Jon Snow",
            }
        ],
        model="llama3-70b-8192",
    )
    return HttpResponse(chat_completion.choices[0].message.content)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", hello, name="hello"),  # ← Added!
]
