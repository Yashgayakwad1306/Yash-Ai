from django.db import models

# Create your models here.


class ChatMessage(models.Model):
    user_message = models.TextField()
    bot_response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True) # Automatically sets the time when saved

    def __str__(self):
        return f"User: {self.user_message[:20]}... | Bot: {self.bot_response[:20]}..."