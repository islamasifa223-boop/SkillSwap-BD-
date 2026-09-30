from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from .models import Profile
from .models import Skill
from .forms import SkillForm
from .models import ExchangeRequest
from .forms import ExchangeRequestForm
from .models import Like
from django.shortcuts import get_object_or_404, redirect
from .models import Notification
from .forms import ProfileForm
from .models import Follow
from .models import Message
from .models import Session
from .forms import SessionForm
from .models import Review
from .forms import ReviewForm


# Home Page
def home(request):
    return render(request, 'users/home.html')


# Register Page
def register(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        # check username exists
        if User.objects.filter(username=username).exists():

            return render(
                request,
                'users/register.html',
                {
                    'error': 'Username already exists'
                }
            )

        # create user
        user = User.objects.create_user(
            username=username,
            password=password
        )

        user.save()

        return redirect('login')

    return render(request, 'users/register.html')

# Login Page
def login_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect('dashboard')

    return render(request, 'users/login.html')


# Dashboard
@login_required
def dashboard(request):

    sent_requests = ExchangeRequest.objects.filter(
        sender=request.user
    )

    received_requests = ExchangeRequest.objects.filter(
        receiver=request.user
    )

    accepted_requests = ExchangeRequest.objects.filter(
        receiver=request.user,
        status='Accepted'
    ) | ExchangeRequest.objects.filter(
        sender=request.user,
        status='Accepted'
    )

    notifications = Notification.objects.filter(
        user=request.user
    ).order_by('-created_at')[:5]

    total_skills = Skill.objects.filter(
        user=request.user
    ).count()

    return render(
        request,
        'users/dashboard.html',
        {
            'sent_requests': sent_requests,
            'received_requests': received_requests,
            'accepted_requests': accepted_requests,
            'notifications': notifications,
            'total_skills': total_skills,
        }
    )


# Logout
def logout_view(request):

    logout(request)

    return redirect('home')
def create_profile(request):

    if request.method == 'POST':

        form = ProfileForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            profile = form.save(commit=False)

            profile.user = request.user

            profile.save()

            return redirect('dashboard')

    else:
        form = ProfileForm()

    return render(
        request,
        'users/create_profile.html',
        {'form': form}
    )

def add_skill(request):

    if request.method == 'POST':

        form = SkillForm(request.POST)

        if form.is_valid():

            skill = form.save(commit=False)

            skill.user = request.user

            skill.save()

            return redirect('skill_list')

    else:

        form = SkillForm()

    return render(
        request,
        'users/add_skill.html',
        {'form': form}
    )

def skill_list(request):

    skills = Skill.objects.all()

    query = request.GET.get('q')

    category = request.GET.get('category')

    if query:

        skills = skills.filter(
            title__icontains=query
        )

    if category:

        skills = skills.filter(
            category__icontains=category
        )

    return render(
        request,
        'users/skill_list.html',
        {
            'skills': skills
        }
    )

def send_request(request, skill_id):

    skill = Skill.objects.get(id=skill_id)

    if request.method == 'POST':

        form = ExchangeRequestForm(request.POST)

        if form.is_valid():

            exchange = form.save(commit=False)

            exchange.sender = request.user

            exchange.receiver = skill.user

            exchange.skill = skill

            exchange.save()

            return redirect('request_list')

    else:

        form = ExchangeRequestForm()

    return render(
        request,
        'users/send_request.html',
        {
            'form': form,
            'skill': skill
        }
    )

def request_list(request):

    requests = ExchangeRequest.objects.filter(
        receiver=request.user
    )

    return render(
        request,
        'users/request_list.html',
        {'requests': requests}
    )

def accept_request(request, request_id):

    exchange = ExchangeRequest.objects.get(id=request_id)

    exchange.status = 'Accepted'

    exchange.save()

    return redirect('request_list')

def reject_request(request, request_id):

    exchange = ExchangeRequest.objects.get(id=request_id)

    exchange.status = 'Rejected'

    exchange.save()

    return redirect('request_list')


def like_skill(request, skill_id):

    skill = get_object_or_404(Skill, id=skill_id)

    if request.user in skill.likes.all():

        skill.likes.remove(request.user)

    else:

        skill.likes.add(request.user)

        Notification.objects.create(
            user=skill.user,
            message=f"{request.user.username} liked your skill."
        )

    return redirect('skill_list')

def notifications(request):

    notifications = Notification.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(
        request,
        'users/notifications.html',
        {
            'notifications': notifications
        }
    )



@login_required
def edit_profile(request):

    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    if request.method == 'POST':

        form = ProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():

            form.save()

            return redirect('dashboard')

    else:

        form = ProfileForm(instance=profile)

    return render(
        request,
        'users/edit_profile.html',
        {
            'form': form
        }
    )

def follow_user(request, user_id):

    user_to_follow = User.objects.get(id=user_id)

    Follow.objects.get_or_create(
        follower=request.user,
        following=user_to_follow
    )

    return redirect('skill_list')



@login_required
def chat(request, user_id):

    other_user = User.objects.get(id=user_id)

    messages = Message.objects.filter(
        sender__in=[request.user, other_user],
        receiver__in=[request.user, other_user]
    ).order_by('timestamp')

    if request.method == 'POST':

        text = request.POST.get('message')

        if text:

            Message.objects.create(
                sender=request.user,
                receiver=other_user,
                message=text
            )

            return redirect('chat', user_id=user_id)

    return render(
        request,
        'users/chat.html',
        {
            'messages': messages,
            'other_user': other_user
        }
    )

@login_required
def edit_skill(request, skill_id):

    skill = get_object_or_404(
        Skill,
        id=skill_id,
        user=request.user
    )

    if request.method == 'POST':

        form = SkillForm(
            request.POST,
            instance=skill
        )

        if form.is_valid():
            form.save()
            return redirect('skill_list')

    else:
        form = SkillForm(instance=skill)

    return render(
        request,
        'users/edit_skill.html',
        {
            'form': form
        }
    )


@login_required
def delete_skill(request, skill_id):

    skill = get_object_or_404(
        Skill,
        id=skill_id,
        user=request.user
    )

    if request.method == 'POST':
        skill.delete()
        return redirect('skill_list')

    return render(
        request,
        'users/delete_skill.html',
        {
            'skill': skill
        }
    )


@login_required
def create_session(request, request_id):

    exchange = get_object_or_404(
        ExchangeRequest,
        id=request_id,
        status='Accepted'
    )

    if request.method == 'POST':

        form = SessionForm(request.POST)

        if form.is_valid():

            session = form.save(commit=False)

            session.exchange_request = exchange
            session.teacher = exchange.receiver
            session.learner = exchange.sender

            session.save()

            Notification.objects.create(
                user=exchange.sender,
                message='Your session has been scheduled.'
            )

            return redirect('session_list')

    else:
        form = SessionForm()

    return render(
        request,
        'users/create_session.html',
        {
            'form': form,
            'exchange': exchange
        }
    )


@login_required
def session_list(request):

    sessions = Session.objects.filter(
        teacher=request.user
    ) | Session.objects.filter(
        learner=request.user
    )

    return render(
        request,
        'users/session_list.html',
        {
            'sessions': sessions
        }
    )

@login_required
def add_review(request, session_id):

    session = get_object_or_404(
        Session,
        id=session_id
    )

    if request.user == session.teacher:
        reviewed_user = session.learner
    else:
        reviewed_user = session.teacher

    if request.method == 'POST':

        form = ReviewForm(request.POST)

        if form.is_valid():

            review = form.save(commit=False)
            review.session = session
            review.reviewer = request.user
            review.reviewed_user = reviewed_user
            review.save()

            Notification.objects.create(
                user=reviewed_user,
                message=f"{request.user.username} reviewed your session."
            )

            return redirect('session_list')

    else:
        form = ReviewForm()

    return render(
        request,
        'users/add_review.html',
        {
            'form': form
        }
    )
    
@login_required
def recommendations(request):

    my_skills = Skill.objects.filter(user=request.user)

    categories = my_skills.values_list(
        'category',
        flat=True
    )

    recommended_skills = Skill.objects.filter(
        category__in=categories
    ).exclude(
        user=request.user
    )

    trending_skills = Skill.objects.order_by('-id')[:5]

    return render(
        request,
        'users/recommendations.html',
        {
            'recommended_skills': recommended_skills,
            'trending_skills': trending_skills
        }
    )

@login_required
def ai_match(request):

    my_learn_skills = Skill.objects.filter(
        user=request.user,
        skill_type='Learn'
    )

    learn_titles = my_learn_skills.values_list(
        'title',
        flat=True
    )

    matched_users = Skill.objects.filter(
        skill_type='Teach',
        title__in=learn_titles
    ).exclude(
        user=request.user
    )

    return render(
        request,
        'users/ai_match.html',
        {
            'matched_users': matched_users
        }
    )