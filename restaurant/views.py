from django.shortcuts import render, redirect, HttpResponse
import random

# Create your views here.

daily_special = [
    'Roasted Carrots - $27',
    'Unroasted Carrots - $15',
    'Medium Rare Carrots - $93',
    'Well Done Carrots - $38',
    'Baked Carrots - $543',
    'Underbaked Carrots - $234',
    'Refrigerated Carrots - $1000',
    'Frozen Carrots - $100',
    'Room Temperature Carrots - $291',
    'Blended Carrots - $58',
    'Baby Carrots - $47',
    '30lb Carrots - $37'
]

special = random.choice(daily_special)

def main(request):
    template_name = 'restaurant/main.html'
    context = {
        "img": "/restaurant/images/taqueria.jpg"
    }
    return render(request, template_name, context)

def order(request):
    '''
    order page, for initial display of page
    '''
    template_name = 'restaurant/order.html'
    if request.method == 'POST':
        # redirect to confirmation view
        return redirect('confirmation')
    context = {
        "special": special
    }
    return render(request, template_name, context)

def confirmation(request):
    '''
    Confirmation page, goes through all selected choices
    '''
    template_name = 'restaurant/confirmation.html'

    if request.method == 'POST':
        menu_choices = request.POST.getlist('menu_choice')

        burrito_choices = []
        if 'Burrito - $8' in menu_choices:
            burrito_choices = request.POST.getlist('burrito_choice')

        total = 0
        for item in menu_choices:
            name, price = item.split('$')
            total += float(price)

        for item in burrito_choices:
            name, price = item.split('$')
            total += float(price)
        

        name = request.POST['customer_name']
        number = request.POST['customer_number']
        email = request.POST['customer_email']
        instructions = request.POST['instructions']
        context = {
            'name': name,
            'number': number,
            'email': email,
            'instructions': instructions,
            'menu_choices': menu_choices,
            'burrito_choices': burrito_choices,
            'total': int(total)
        }

        return render(request, template_name, context)
    return redirect("order")