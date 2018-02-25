from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from avangard.chat.models import ChatRoom, Message
from django.db.models import Q


# Получение списка комнат
@login_required
def index(request):
    chat_list = ChatRoom.objects.all()
    context = {'chat_list': chat_list}
    return render(request, 'chat_list.html', context)


# Рендеринг шаблона чата
@login_required
def chat_room(request, room_id):
    museum = ChatRoom.objects.get(pk=room_id)
    context = {'room_id': room_id, 'user_id': request.user.id, 'museum': museum}
    return render(request, 'dialog_list.html', context)


# Получение диалогов для комнаты
@login_required
def get_dialogs(request, room_id):
    dialogs = Message.objects.filter(room_id=room_id).exclude(sender=request.user).values('sender').order_by().distinct()
    dialogs_dict = {"dialogs": []}
    for dialog in dialogs:
        message = Message.objects.filter(Q(room_id=room_id), Q(sender=dialog['sender']) | Q(recipient=dialog['sender'])).first()
        if message.sender != request.user:
            message.user = message.sender
            message.out = False
        else:
            message.user = message.recipient
            message.out = True
        record = {"user_id": message.user.id, "name": message.user.get_full_name(), "text": message.text,
                  "status": message.status, "out": message.out,
                  "timestamp": message.timestamp}
        dialogs_dict["dialogs"].append(record)
    return JsonResponse(dialogs_dict)
