from django.shortcuts import render
import random

# Create your views here.

quotes = [
    "Life is so much more rewarding if you strive for something, rather than take what's given to you on a plate.",
    "Music is the only thing that will give and give and give and not take.",
    "Every bad situation is a blues song waiting to happen.",
    "Life's short. Anything could happen, and it usually does, so there is no point in sitting around thinking about all the ifs, ands and buts.",
    "I don’t need help because if I can’t help myself I can’t be helped.",
    "If you don't throw yourself into something, you'll never know what you could have had.",
    "I love to live and I live to love.",
    "Life happens. There is no point in being upset or down about things we can't control or change.",
    "There's no point in saying anything but the truth."
]

img_path = "/quotes/images"
imgs = [
    "/quotes/images/img1.jpg",
    "/quotes/images/img2.jpg",
    "/quotes/images/img3.jpg",
    "/quotes/images/img4.jpg"
]

def quote(request):
    template_name = 'quotes/quote.html'
    context = {
        "quote": random.choice(quotes),
        "img": random.choice(imgs)
    }
    return render(request, template_name, context)

def show_all(request):
    template_name = 'quotes/show_all.html'
    context = {
        'quotes': quotes,
        'imgs': imgs,
    }
    return render(request, template_name, context)

def about(request):
    template_name = 'quotes/about.html'
    return render(request, template_name)