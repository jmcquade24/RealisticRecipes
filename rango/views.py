from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.models import login_required
from .models import Recipe

# Create your views here.
