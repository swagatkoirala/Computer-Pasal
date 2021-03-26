from django.shortcuts import render ,redirect
from django.views import View
from django.http import JsonResponse ,HttpResponse
from django.http import request

from django.views.generic import DetailView
import math

from store.models.product import Product
from store.models.category import Category
from store.models.customer import Customer
from store.models.rating import Rating
from store.forms import RatingForm
from django.contrib.auth.decorators import login_required
import random


class Details(DetailView):
    model = Product
    template_name = "product-details.html"
    
    # @login_required
    def post(self,request,*args,**kwargs):
        form = RatingForm(request.POST)
        

        if form.is_bound==True:
            el_id = request.POST.get('el_id')
            val = request.POST.get('val')
            customer = request.session.get('customer')
            el_ids=int(el_id)
            vals=int(val)

            obj = Rating(product=Product.objects.get(id=el_ids),customer=Customer.objects.get(id=customer),score=vals)
            obj.save()
            return JsonResponse({'success': 'true', 'score': val}, safe=False)
        else:
            form=RatingForm()
        return JsonResponse({'success':'false'})

    def get_context_data(self, **kwargs):
        context = super(Details, self).get_context_data(**kwargs)
        customer = self.request.session.get('customer')
        # SHOWING THE RATING OF THE PRODUCTS
        obj = Rating.objects.filter ( customer=customer , product =context['product'].id ).order_by ( "id" ).last ()
        index=str(obj)

        my_dict={}
        my_list=[]
        # FOR THE LIST OF PRODUCT EXCLUDING OWN PRODUCT
        for z in Product.objects.exclude ( id =context['product'].id ):
            zz=z.id
            my_list.append(zz)
        # STORING THE SCORE OF ALL OTHER PRODUCTS WITH THEIR PROD_ID IN DICTIONART
        for x in iter(my_list):
            objs = Rating.objects.filter (  product = x ).last ()
            s=str(objs)
            if s=='None': 
                first = random.randint(1,5)
                last = random.randint(1,5)
            else:
                first = Rating.objects.filter (  product = x ).order_by ( "id" ).first().score
                last= Rating.objects.filter (  product = x ).order_by ( "id" ).last().score
            this =[first,last]
            my_dict[str(x)]= this
        # FOR FINDING SCORE OF OWN PRODUCT   
        objts = Rating.objects.filter (  product =context['product'].id ).order_by ( "id" ).last ()
        o=str(objts)
        if o=='None': 
            first = random.randint(1,5)
            last = random.randint(1,5)
        else:
            first = Rating.objects.filter (  product = context['product'].id ).order_by ( "id" ).first().score
            last= Rating.objects.filter (  product = context['product'].id ).order_by ( "id" ).last().score
        v1 = [first,last]
        # CALCULATING THE COSINE SIMILARITY OF OWN PRODUCT WITH ALL PRODUCT 
        sim_dict ={}
        for y in iter(my_list):
            v2 = my_dict[str(y)]
            def cosine_similarity(v1,v2):
                sumxx,sumxy,sumyy = 0,0,0
                for i in range(len(v1)):
                    x= v1[i]
                    y= v2[i]
                    sumxx += x*x
                    sumyy += y*y
                    sumxy += x*y
                return sumxy/math.sqrt(sumxx*sumyy)
            rate = cosine_similarity(v1,v2)
            sim_dict[str(y)]=rate
        # SORTING THE PRODUCT ACCORDING TO THE COSINE SIMILARITY SCORE
        sorted_dict={}
        sorted_values=sorted(sim_dict.values(),reverse=True)
        for i in sorted_values:
            for k in sim_dict.keys():
                if sim_dict[str(k)] == i:
                    sorted_dict[k] = sim_dict[str(k)]
                    break
        # LIST OF PRODUCTS OF SORTED DICTIONARY
        sorted_dictionary=[*sorted_dict]
        # EXTRACTING THE PRODUCT OBJECT FROM THE PROD_ID INORDER TO SEND TO FRONTEND
        prods=[]
        for l in sorted_dictionary:
            product_recommend=Product.objects.get(id=int(l))
            prods.append(product_recommend)
        # EXTRACTING SIMILARITY SCORES
        sim_score=sorted_dict.values()
        ss=[*sim_score]
        # import pdb ;pdb.set_trace()
        # SENDING RATING AND RECOMMENDED PRODUCT TO THE FRONTEND
        if index =='None' :
            context['score'] = 0
            context['product_recommend_one']=prods[0]
            context['product_recommend_two']=prods[1]
            context['product_recommend_three']=prods[2]
            context['product_recommend_four']=prods[3]
            context['one_ss']=ss[0]
            context['two_ss']=ss[1]
            context['three_ss']=ss[2]
            context['four_ss']=ss[3]
            return context
        else:
            context['score'] = obj.score
            context['product_recommend_one']=prods[0]
            context['product_recommend_two']=prods[1]
            context['product_recommend_three']=prods[2]
            context['product_recommend_four']=prods[3]
            context['one_ss']=ss[0]
            context['two_ss']=ss[1]
            context['three_ss']=ss[2]
            context['four_ss']=ss[3]
            return context

