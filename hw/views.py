## hw/views.py
## description: write view functions to handle URL requests for the hw app

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import random
import time

# Create your views here.

""" def home(request):
    '''Handle the main URL for the hw app'''

    response_text = '''
    <html>
    <h1>Hello, world!</h1>
    <p>this is our first django web application</p>
    <hr>
    This page was generated at {time.ctime()}.
    </html>
    '''

    # create and return a response to the client:
    return HttpResponse(response_text) """

def home(request):
    '''
    Function to handle the url request for /hw (main page).
    Delegate rendering to the template hw/home.html
    '''

    # use this template to render the response
    template_name = 'hw/home.html'

    # dict of context variables for the templates
    context = {
        "current_time": time.ctime(),
        "letter1": chr(random.randint(65, 90)), # letter from a-z
        "letter2": chr(random.randint(65, 90)),
        "number": random.randint(1, 10) # random number from 1-10
    }

    # delegate rending work to the template
    return render(request, template_name, context)
