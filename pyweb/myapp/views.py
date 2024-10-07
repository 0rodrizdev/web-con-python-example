from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import ChatRoom, Message
from .forms import MessageForm

class IndexView(View):
    """ Vista para la página principal """
    def get(self, request):
        return render(request, 'index.html')

@method_decorator(login_required, name='dispatch')
class ChatRoomView(View):
    """ Vista para una sala de chat específica """
    def get(self, request, room_name):
        messages = Message.objects.filter(room__name=room_name).order_by('-timestamp')
        form = MessageForm()
        return render(request, 'chat_room.html', {
            'room_name': room_name,
            'messages': messages,
            'form': form,
        })

    def post(self, request, room_name):
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.room = get_object_or_404(ChatRoom, name=room_name)
            message.user = request.user
            message.save()
            return redirect('chat_room', room_name=room_name)
        return render(request, 'chat_room.html', {
            'room_name': room_name,
            'messages': Message.objects.filter(room__name=room_name).order_by('-timestamp'),
            'form': form,
        })

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    """ Vista para el perfil del usuario """
    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        return render(request, 'profile.html', {
            'user': user,
        })

@method_decorator(login_required, name='dispatch')
class PrivateChatView(View):
    """ Vista para el chat privado entre usuarios """
    def get(self, request, username):
        other_user = get_object_or_404(User, username=username)
        messages = Message.objects.filter(
            room__participants__in=[request.user, other_user]
        ).order_by('-timestamp')
        return render(request, 'private_chat.html', {
            'other_user': other_user,
            'messages': messages,
        })

# Vistas adicionales
class AboutView(View):
    """ Vista para la página 'Acerca de' """
    def get(self, request):
        return render(request, 'about.html')

class ContactView(View):
    """ Vista para la página de contacto """
    def get(self, request):
        return render(request, 'contact.html')

    def post(self, request):
        # Aquí puedes manejar la lógica de envío del formulario de contacto
        return redirect('index')

@login_required
def send_message(request, room_name):
    """ Función para enviar un mensaje en la sala de chat """
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.room = get_object_or_404(ChatRoom, name=room_name)
            message.user = request.user
            message.save()
            return redirect('chat_room', room_name=room_name)
    return redirect('chat_room', room_name=room_name)
