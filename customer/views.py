
import json

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.db.models import Q
from django.core.mail import send_mail

from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from .models import MenuItem, Category, OrderModel
from django.contrib.auth import logout

class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/index.html')



class SignupView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/new_signups.html')

    def post(self, request, *args, **kwargs):
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        if pass1 != pass2:
            return HttpResponse("Your password and confirm password are not the same!")
        else:
            my_user = User.objects.create_user(uname, email, pass1)
            my_user.save()
            return redirect('new_login')

class LoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/new_login.html')

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')
        user = authenticate(request, username=username, password=pass1)
        if user is not None:
            auth_login(request, user)
            return redirect('index')
        else:
            return HttpResponse("Username or Password is incorrect!")
        
class LogoutPage(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return render(request, 'customer/logout.html')

# ////////////////////////////////////////////////////////

class Order(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, *args, **kwargs):
        biriyani = MenuItem.objects.filter(category__name__contains='biriyani')
        kappa = MenuItem.objects.filter(category__name__contains='kappa')
        fish = MenuItem.objects.filter(category__name__contains='fish')
        chicken = MenuItem.objects.filter(category__name__contains='chicken')
        

        context = {
            'biriyani': biriyani,
            'kappa': kappa,
            'fish': fish,
            'chicken': chicken,
            
        }
        return render(request, 'customer/order.html', context)

    def post(self, request, *args, **kwargs):
        selected_items = request.POST.getlist('items[]')
        request.session['selected_items'] = selected_items
        return redirect('personal_details')
    





# ///////////////////////////////////////////////////////


class personal_order(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, *args, **kwargs):
        return render(request, 'customer/personal_details.html')

    def post(self, request, *args, **kwargs):
        selected_items = request.session.get('selected_items', [])
        order_items = {'items': []}

        for item in selected_items:
            menu_item = MenuItem.objects.get(pk=int(item))
            item_data = {'id': menu_item.pk, 'name': menu_item.name, 'price': menu_item.price}
            order_items['items'].append(item_data)

        price = sum(item['price'] for item in order_items['items'])
        item_ids = [item['id'] for item in order_items['items']]

        name = request.POST.get('name')
        email = request.POST.get('email')
        street = request.POST.get('street')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip')

        order = OrderModel.objects.create(
            price=price,
            name=name,
            email=email,
            street=street,
            city=city,
            state=state,
            zip_code=zip_code
        )
        order.items.add(*item_ids)

        body = (f'Thank you for your order! Your food is being made and will be delivered soon!\n'
                f'Your total: {price}\n'
                'Thank you again for your order!')

        send_mail(
            'Thank You For Your Order!',
            body,
            'example@example.com',
            [email],
            fail_silently=False
        )

        return redirect('order-confirmation', pk=order.pk)







    


    

class OrderConfirmation(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, pk, *args, **kwargs):
        order = OrderModel.objects.get(pk=pk)
        context = {'pk': order.pk, 'items': order.items, 'price': order.price}
        return render(request, 'customer/order_confirmation.html', context)

    def post(self, request, pk, *args, **kwargs):
        data = json.loads(request.body)
        if data.get('isPaid'):
            order = OrderModel.objects.get(pk=pk)
            order.is_paid = True
            order.save()
        return redirect('payment-confirmation')

class OrderPayConfirmation(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/order_pay_confirmation.html')

class Menu(View):
    def get(self, request, *args, **kwargs):
        menu_items = MenuItem.objects.all()
        context = {'menu_items': menu_items}
        return render(request, 'customer/menu.html', context)

class MenuSearch(View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get("q")
        menu_items = MenuItem.objects.filter(
            Q(name__icontains=query) |
            Q(price__icontains=query) |
            Q(description__icontains=query)
        )
        context = {'menu_items': menu_items}
        return render(request, 'customer/menu.html', context)






