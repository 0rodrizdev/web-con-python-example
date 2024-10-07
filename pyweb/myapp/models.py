from django.db import models
from django.contrib.auth.models import User

class ChatRoom(models.Model):
    """
    Modelo que representa una sala de chat.
    """
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ChatMessage(models.Model):
    """
    Modelo que representa un mensaje en un chat.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']  # Ordenar mensajes por tiempo de creación

    def __str__(self):
        return f"{self.user.username}: {self.message[:20]}..."  # Muestra los primeros 20 caracteres


class UserProfile(models.Model):
    """
    Modelo que extiende el modelo de usuario para añadir información adicional.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='default.jpg')
    last_seen = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


class MessageReaction(models.Model):
    """
    Modelo que representa las reacciones a un mensaje.
    """
    message = models.ForeignKey(ChatMessage, on_delete=models.CASCADE, related_name='reactions')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reaction_type = models.CharField(max_length=10)  # Ej: 'like', 'dislike', etc.
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('message', 'user', 'reaction_type')  # Cada usuario puede reaccionar solo una vez a un mensaje

    def __str__(self):
        return f"{self.user.username} reacted with {self.reaction_type} to {self.message}"


class PrivateMessage(models.Model):
    """
    Modelo para mensajes privados entre usuarios.
    """
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']  # Ordenar mensajes privados por tiempo de creación

    def __str__(self):
        return f"From {self.sender.username} to {self.recipient.username}: {self.message[:20]}..."  # Muestra los primeros 20 caracteres


class Group(models.Model):
    """
    Modelo que representa un grupo de usuarios.
    """
    name = models.CharField(max_length=100, unique=True)
    members = models.ManyToManyField(User, related_name='groups')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def add_member(self, user):
        self.members.add(user)

    def remove_member(self, user):
        self.members.remove(user)

    def get_members(self):
        return self.members.all()
