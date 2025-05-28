from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from core.models import Message

@login_required
def chat_view(request, username=None):
    users = User.objects.exclude(username=request.user.username)
    recipient = User.objects.get(username=username) if username else None

    if request.method == "POST" and request.headers.get("x-requested-with") == "XMLHttpRequest":
        content = request.POST.get("message", "")
        fichier = request.FILES.get("fichier")
        parent_id = request.POST.get("parent_id")

        parent = Message.objects.filter(id=parent_id).first() if parent_id else None

        message = Message.objects.create(
            sender=request.user,
            recipient=recipient,
            content=content,
            fichier=fichier,
            parent=parent  # ✅ lien vers le message auquel on répond
       )

        return JsonResponse({
            "sender": request.user.username,
            "content": message.content,
            "file_url": message.fichier.url if message.fichier else "",
            "timestamp": message.timestamp.strftime('%d/%m/%Y %H:%M'),
            "parent_id": message.parent.id if message.parent else "",
            "parent_content": message.parent.content if message.parent else "",
        })

    # messages à afficher
    messages = []
    if recipient:
        messages = Message.objects.filter(
            sender__in=[request.user, recipient],
            recipient__in=[request.user, recipient]
        )

    return render(request, "chat/chat.html", {
        "users": users,
        "recipient": recipient,
        "messages": messages,
    })
