from django.db import models

class Puzzle(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    question = models.TextField()
    answer = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

class Message(models.Model):
    puzzle = models.OneToOneField(Puzzle, on_delete=models.CASCADE, related_name='message')
    content = models.TextField()
    image = models.ImageField(upload_to='message_images/', blank=True, null=True)
    revealed = models.BooleanField(default=False)

    def __str__(self):
        return f"Message for {self.puzzle.title}"

class UserProgress(models.Model):
    current_puzzle = models.ForeignKey(Puzzle, on_delete=models.SET_NULL, null=True, blank=True)