from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User

import forms

from models import Paper, PaperVersion

def register_account(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect("index")

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(username=request.POST['username'],
                         password=request.POST['password1'])
            login(request, user)
            return HttpResponseRedirect("index")
    else:
        form = UserCreationForm()

    return render_to_response("registration/account.html", RequestContext(request, {'form' : form}))

@login_required
def index(request):
    return render_to_response("index.html", RequestContext(request))

@login_required
def paper_view(request):
    try:
        paper = Paper.objects.filter(id=int(request.GET['id'])).get()
        paper_versions = list(PaperVersion.objects.filter(paper=paper).order_by('-time').all())
        authors = paper.authors.all()
        latest_abstract = paper_versions[-1]
    except Paper.DoesNotExist:
        paper = None
        paper_versions = []
        authors = []
        latest_abstract = None

    return render_to_response("paper.html", RequestContext(request, {
        'paper' : paper,
        'paper_versions' : paper_versions,
        'authors' : authors,
    }))

@login_required
def submit_view(request):
    if request.method == 'POST':
        form = forms.SubmitForm(request.POST, request.FILES)
        if form.is_valid():
            paper = form.save(request.user)
            return HttpResponseRedirect("paper?id=%d" % paper.id)
    else:
        form = forms.SubmitForm()

    return render_to_response("profile.html", RequestContext(request, {'form' : form}))

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = forms.ProfileForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("accounts/profile")
    else:
        form = forms.ProfileForm()

    return render_to_response("profile.html", RequestContext(request, {'form' : form}))