from django.shortcuts import render, redirect
from django.views import View
from .forms import LoginForm, RegistrationForm
from .models import Bestdeal
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.core.paginator import Paginator
import pickle



User = get_user_model()


product_categories = ['Computing',
                      'Phones & Tablets',
                      "Grocery"]

objects_per_page = 24

try:
    list_display = pickle.load('data.pkl','rb')
except:
    product_categories = Bestdeal.objects.order_by().values_list('category',flat=True).distinct()
    list_display = []
    for p in product_categories:
        qs = Bestdeal.objects.filter(category=p)
        sub_categories=qs.order_by().values_list('sub_category',flat=True).distinct()
        list_display.append({'category':p,'sub_categories':sub_categories})
    pickle.dump(list_display,open('data.pkl','wb'))

def from_slug(slug):
    return slug.replace('-', ' ')

class HomeView(View):
    def get(self, request, *args,**kwargs):
        query = Bestdeal.objects.filter(sub_category='Computers').order_by('id')
        paginator = Paginator(query, objects_per_page)
        page_number = request.GET.get('page')
        products = paginator.get_page(page_number)
        context = {
            'product_categories': list_display,
            'products': products
        }
        return render(request, 'home.html', context)


class ListView(View):
    def get(self, request, subcategory,*args, **kwargs):
        print(from_slug(subcategory))
        query = Bestdeal.objects.filter(sub_category=from_slug(subcategory)).order_by('id')
        paginator = Paginator(query, objects_per_page)
        page_number = request.GET.get('page')
        products = paginator.get_page(page_number)
        context = {
            'product_categories': list_display,
            'products': products,
            'category':from_slug(subcategory),
            'items_found':len(query)
        }
        return render(request, 'products.html', context)


class DetailView(View):
    def get(self, request, subcategory, id, *args, **kwargs):
        #query = product.objects.all()
        query = Bestdeal.objects.filter(id=id).first()
        related_products = Bestdeal.objects.filter(sub_category=from_slug(subcategory))
        context = {
            'product_categories': list_display,
            'product': query,
            'related_products': related_products[:5]
        }
        return render(request, 'product_details.html', context)

class ContactView(View):
    def get(self, request):
        return render(request, 'contacts.html')


class AboutView(View):
    def get(self, request):
        return render(request, 'about.html')


