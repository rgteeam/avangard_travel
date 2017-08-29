from rest_framework import viewsets
from avangard.chat.serializers import ChatRoomSerializer, MessageSerializer
from .models import ChatRoom, Message
from rest_framework.authentication import SessionAuthentication
from avangard.account.api import BearerAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q
from rest_framework.viewsets import generics
from django.http import JsonResponse
from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 1000

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'unread_ids': data["unread_ids"],
            'chat_id': data["chat_id"],
            'results': data["data"],
        })


class GetDialogsViewSet(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication, BearerAuthentication)
    serializer_class = ChatRoomSerializer
    permission_classes = (IsAuthenticated,)
    queryset = ChatRoom.objects.all()


    def list(self, request):
        print(request.user.pk)
        message_queryset = Message.objects.filter(Q(sender=request.user.pk) | Q(recipient=request.user.pk))
        for room in self.queryset:
            messages_for_room = message_queryset.filter(room=room)
            unread_count = len(messages_for_room.filter(status=1, recipient=request.user.pk))
            try:
                room.last_message = messages_for_room[0]
            except Exception:
                pass
            room.unread_count = unread_count
        serializer = ChatRoomSerializer(self.queryset, many=True)
        return Response(serializer.data)

# Обновление статуса сообщения

class MarkAsRead(generics.UpdateAPIView):
    serializer_class = MessageSerializer
    authentication_classes = (BearerAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = Message.objects.filter(pk__in=self.request.data['ids'])
        return queryset

    def update(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        response_dict = {}

        if len(queryset) == 0:
            response_dict["error"] =  "ids not found"
            return JsonResponse(response_dict)

        response_dict["success"] = []
        response_dict["failed"] = []
        for instance in queryset:
            if request.user.pk == instance.recipient.pk:
                response_dict["success"].append({"id": instance.pk})
                instance.status = 2
                instance.save()
            else:
                response_dict["failed"].append({"id": instance.pk, "error": "access error"})
        return JsonResponse(response_dict)


class MessageHistoryViewSet(viewsets.ModelViewSet):
    authentication_classes = (BearerAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = MessageSerializer
    pagination_class = StandardResultsSetPagination
    queryset = Message.objects.all()


    def get_queryset(self):
        room_id = self.request.query_params.get('room_id', None)
        chat_id = self.request.query_params.get('chat_id', None)
        if chat_id is not None and room_id is not None:
            queryset = Message.objects.filter(room=room_id)
            queryset = queryset.filter(Q(sender=chat_id) | Q(recipient=chat_id))
        elif room_id is not None:
            queryset = Message.objects.filter(room=room_id)
        else:
            queryset = Message.objects.all()
        return queryset, chat_id


    def list(self, request):
        queryset, chat_id = self.get_queryset()
        if queryset != None:
            queryset = queryset.filter(Q(sender=request.user.pk) | Q(recipient=request.user.pk))
            unread_queryset = queryset.filter(recipient=request.user.pk, status = 1).values_list('pk', flat=True)

            page = self.paginate_queryset(queryset)

            if page is not None:
                serializer = self.get_serializer(page, many=True)
            else:
                serializer = self.get_serializer(queryset, many=True)

            result = {}
            result["data"] = serializer.data
            result["unread_ids"] = unread_queryset
            if chat_id is not None:
                result['chat_id'] = chat_id
            else:
                result['chat_id'] = None

            return self.get_paginated_response(result)
        else:
            content = {
                'error': 'room_id not provided',
            }
        return Response(content)