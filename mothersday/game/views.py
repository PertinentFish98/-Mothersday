from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Puzzle, Message, UserProgress


# ─────────── Auth helpers ───────────
def register_view(request):
    if request.user.is_authenticated:
        return redirect("start_game")

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Conta criada! Você pode fazer sign in.")
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "register.html", {"form": form})

# ─────────── Final page ───────────
@login_required
def final_message_view(request):
    return render(request, 'final_message.html')


@login_required
def logout_view(request):
    auth_logout(request)
    return redirect("login")


# ─────────── Game logic ───────────
@login_required
def start_game(request):
    Message.objects.all().update(revealed=False)
    UserProgress.objects.all().delete()

    first_puzzle = Puzzle.objects.order_by("order").first()
    progress = UserProgress.objects.create(current_puzzle=first_puzzle)
    return redirect("puzzle_view", pk=first_puzzle.pk)


@login_required
def puzzle_view(request, pk):
    puzzle = get_object_or_404(Puzzle, pk=pk)
    progress, _ = UserProgress.objects.get_or_create(pk=1)
    next_puzzle = (
        Puzzle.objects.filter(order__gt=puzzle.order).order_by("order").first()
    )

    correct = False
    feedback = ""
    message = None

    if request.method == "POST":
        user_answer = request.POST.get("answer", "").strip().lower()

        if user_answer in puzzle.answer.lower():
            correct = True

            # mark message revealed (if one exists) and expose it immediately
            if puzzle.message:
                puzzle.message.revealed = True
                puzzle.message.save()
                message = puzzle.message

            # advance the user’s progress
            if next_puzzle:
                progress.current_puzzle = next_puzzle
                progress.save()
        else:
            feedback = "Oops! Tente novamente! Está quase lá."

    if message is None and puzzle.message and puzzle.message.revealed:
        message = puzzle.message

    return render(
        request,
        "puzzle.html",
        {
            "puzzle": puzzle,
            "message": message,
            "correct": correct,
            "next_puzzle": next_puzzle,
            "feedback": feedback,
        },
    )
