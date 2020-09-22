from django.shortcuts import render
from django.views import View
from django.urls import reverse
from .models import UserCart
from django.http import HttpResponseRedirect
from app.models import Bestdeal
from django.db.models import Sum
import pickle

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
class CartView(View):
    def get(self, request):
        context = {}
        if request.user.is_authenticated:
            items = UserCart.objects.filter(user = request.user)
            total = items.aggregate(Sum('total'))['total__sum']
            categories = Bestdeal.objects.values_list('category',flat=True).distinct()
            context = {'items': items, 'length': len(items),'total':total,'product_categories':list_display}
        return render(request, 'cart.html', context)
    def post(self,request,*args, **kwargs):
        if request.user.is_authenticated:
            action = request.POST.get('action')
            product_id = request.POST.get('product_id')
            product = Bestdeal.objects.filter(id=product_id).first()
            next_url = request.POST.get('next')
            if action =='add_new':
                obj, created = UserCart.objects.get_or_create(user=request.user,
                                                            product=product) 
                if created:
                    
                    obj.count = request.POST.get('qty')
                    obj.total = int(obj.count)*int(obj.product.price)
                    obj.save()

            if action == 'add':
                obj = UserCart.objects.filter(product=product).first()
                if obj:
                    obj.count +=1
                    obj.total = obj.count*obj.product.price
                    obj.save()
            if action == 'subtract':
                obj = UserCart.objects.filter(product=product).first()
                if obj and obj.count >=2:
                    obj.count -=1
                    obj.total = obj.count*obj.product.price
                    obj.save()
            if action == 'delete':
                obj = UserCart.objects.filter(product=product).first()
                obj.delete()
            if next_url:
                return HttpResponseRedirect(next_url)             
        return HttpResponseRedirect(reverse('cart'))

            
