from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.core.paginator import Paginator
from .models import Question, Answer, Comment, UserProfile, Tag
from .forms import QuestionForm, AnswerForm, CommentForm, UserProfileForm



@login_required
def add_question(request):
    tags = Tag.objects.all()
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.save()
            form.save_m2m()  # Save the many-to-many relationships
            return redirect('home')
    else:
        form = QuestionForm()
    return render(request, 'add_question.html', {'form': form, 'tags': tags})




@login_required
def answer_question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.question = question
            answer.save()
            return redirect('home')
    else:
        form = AnswerForm()
    return render(request, 'answer_question.html', {'form': form, 'question': question})

@login_required
def add_comment(request, question_id=None, answer_id=None):
    question = None
    answer = None
    if question_id:
        question = get_object_or_404(Question, pk=question_id)
    if answer_id:
        answer = get_object_or_404(Answer, pk=answer_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.question = question
            comment.answer = answer
            comment.save()
            return redirect('home')
    else:
        form = CommentForm()
    return render(request, 'add_comment.html', {'form': form, 'question': question, 'answer': answer})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user_profile)
    return render(request, 'profile.html', {'form': form})



def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')


def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


@login_required
def home(request):
    questions = Question.objects.all().order_by('-created_at')
    tags = Tag.objects.all()

    # Handle the question form submission
    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        if question_form.is_valid():
            new_question = question_form.save(commit=False)
            new_question.author = request.user
            new_question.save()
            return redirect('home')

    else:
        question_form = QuestionForm()

    # Handle the answer form submission
    if request.method == 'POST':
        answer_form = AnswerForm(request.POST)
        if answer_form.is_valid():
            new_answer = answer_form.save(commit=False)
            new_answer.author = request.user
            new_answer.question = Question.objects.get(pk=request.POST.get('question_id'))
            new_answer.save()
            return redirect('home')

    else:
        answer_form = AnswerForm()

    # Handle the comment form submission
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.author = request.user
            new_comment.answer = Answer.objects.get(pk=request.POST.get('answer_id'))
            new_comment.save()
            return redirect('home')

    else:
        comment_form = CommentForm()

    # Handle the user profile form submission
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('home')

    else:
        profile_form = UserProfileForm(instance=user_profile)

    context = {
        'questions': questions,
        'tags': tags,
        'question_form': question_form,
        'answer_form': answer_form,
        'comment_form': comment_form,
        'profile_form': profile_form,
    }

    return render(request, 'home.html', context)

def welcome(request):
    return render(request, 'welcome.html')