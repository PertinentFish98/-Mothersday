from django.contrib import admin
from .models import Puzzle, Message, UserProgress

admin.site.register(Puzzle)
admin.site.register(Message)
admin.site.register(UserProgress)
