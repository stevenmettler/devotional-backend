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
from devotionail import settings
# devotionail/urls.py
from django.contrib import admin
from django.http import HttpResponse
from django.urls import path

client = Groq(
    api_key=settings.GROQ_API_KEY
)


def topic(request, topic):
    chat_completion = client.chat.completions.create(
        #
        # Required parameters
        #
        messages=[
            # Set an optional system message. This sets the behavior of the
            # assistant and can be used to provide specific instructions for
            # how it should behave throughout the conversation.
            {
                "role": "system",
                "content": "you are a Christian. You believe in the Bible as the supreme authority of truth in all things and you submit to the teachings of Jesus Christ. Your one goal is to accept a topic and generate a Bible study with three scriptures as well as three contemplative questions as your output. I will ask you to give me personal Bible studies on a specific topic, and you will return concise studies with 3 or so scriptures and 3 contemplative questions at the end that aims to help a user get a closer relationship with God. You believe that faith, repentance, and baptism are necessary for salvation. The output should be in JSON format. Please do not output anything beside the JSON formatted response. Please use the JSON template below to format the response as well as the topic provided below: **Json template:** {  study: [    {      scripture: Scripture1,      text: Text1    },    {      scripture: Scripture2,      text: Text2    },    {      scripture: Scripture3,      text: Text3    }  ],  questions: [    Contemplative Question 1,    Contemplative Question 2,    Contemplative Question 3  ]}"
            },
            # Set a user message for the assistant to respond to.
            {
                "role": "user",
                "content": f"Topic: {topic}",
            }
        ],

        # The language model which will generate the completion.
        model="llama3-70b-8192",

        #
        # Optional parameters
        #

        # Controls randomness: lowering results in less random completions.
        # As the temperature approaches zero, the model will become deterministic
        # and repetitive.
        temperature=0.5,

        # The maximum number of tokens to generate. Requests can use up to
        # 2048 tokens shared between prompt and completion.
        max_tokens=1024,

        # Controls diversity via nucleus sampling: 0.5 means half of all
        # likelihood-weighted options are considered.
        top_p=1,

        # A stop sequence is a predefined or user-specified text string that
        # signals an AI to stop generating content, ensuring its responses
        # remain focused and concise. Examples include punctuation marks and
        # markers like "[end]".
        stop=None,

        # If set, partial message deltas will be sent.
        stream=False,
    )
    return HttpResponse(chat_completion.choices[0].message.content)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("topic/<str:topic>", topic, name="topic"),  # ← Added!
]
