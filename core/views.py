from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from dateutil.relativedelta import relativedelta
from datetime import date


from diag import settings

from .form import CustomUserCreationForm

