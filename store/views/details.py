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
            # context ={'obj':obj }

            
            
            return JsonResponse({'success': 'true', 'score': val}, safe=False)
        else:
            form=RatingForm()
        return JsonResponse({'success':'false'})

    def get_context_data(self, **kwargs):
        context = super(Details, self).get_context_data(**kwargs)
        customer = self.request.session.get('customer')
        # import pdb ;pdb.set_trace()
        obj = Rating.objects.filter ( customer=customer , product =context['product'].id ).order_by ( "id" ).last ()
        rams=str(obj)
        # my_list=[{'v0': [0, 0]}]
        my_dict={}
        my_list=[]
        for z in Rating.objects.exclude ( product =context['product'].id ).order_by ( "id" ):
            zz=z.id
            my_list.append(zz)
        
        # my=iter(my_list)
        # import pdb ;pdb.set_trace()

        # vari=Rating.objects.all().order_by ( "id" ).last ().id

        for x in iter(my_list):
            # Rating.objects.exclude ( product =context['product'].id ).order_by ( "id" )
            a=Rating.objects.filter ( product =context['product'].id ).order_by ( "id" ).last()
            
            if str(a)!= 'None' and x == Rating.objects.filter(product=context['product'].id).order_by ( "id" ).last ().id :
                continue
            objs = Rating.objects.filter (  product =x ).order_by ( "id" ).last ()
            s=str(objs)
            # import pdb ;pdb.set_trace()
            if s=='None': 
                first = 1
                last = 5
            else:
                first = Rating.objects.filter (  product = x ).order_by ( "id" ).first().score
                last= Rating.objects.filter (  product = x ).order_by ( "id" ).last().score
            this =[first,last]
            # d = {'v'+str(x): this}
            # # print(d)
            # check =dict(d)
            # my_list.append(check)
            my_dict[str(x)]= this
        # import pdb ;pdb.set_trace()
        objts = Rating.objects.filter (  product =context['product'].id ).order_by ( "id" ).last ()
        o=str(objts)
        if o=='None': 
            first = 5
            last = 1
        else:
            first = Rating.objects.filter (  product = context['product'].id ).order_by ( "id" ).first().score
            last= Rating.objects.filter (  product = context['product'].id ).order_by ( "id" ).last().score
        v1 = [first,last]
        # v2=my_dict['5']
        # import pdb ;pdb.set_trace()
        sim_dict ={}
        ram=[]
        for y in iter(my_list):
            b=Rating.objects.filter ( product =context['product'].id ).order_by ( "id" ).last()
            if str(b) != 'None' and y == Rating.objects.filter ( product =context['product'].id ).order_by ( "id" ).last().id :
                continue
            v2 = my_dict[str(y)]
            # ob = Rating.objects.filter (  product =y ).order_by ( "id" ).last ()
            # r=str(ob)
            # # import pdb ;pdb.set_trace()
            if v1 == v2 :
                rate=0.00
                    
            else:
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

            # print(v1,v2,rate)
            sim_dict[str(y)]=rate
            ram.append(rate)
            # def closest(lst, K): 
            #     return lst[min(range(len(lst)), key = lambda i: abs(lst[i]-K))]
            ram.sort(reverse=True)
            close=ram[0:4]
            qwerty=len(ram)-1


        
        # for d in sim_dict:
        #     if sim_dict[d] != ram[0]:
        #         continue
        #     else:
        #         recommend_id_one = d
                

        # for d in sim_dict:
        #     if sim_dict[d] != ram[1]:
        #         continue
        #     else:
        #         recommend_id_two = d
               

        # for d in sim_dict:
        #     if sim_dict[d] != ram[2]:
        #         continue
        #     else:
        #         recommend_id_three = d
        # for d in sim_dict:
        #     if sim_dict[d] != ram[3]:
        #         continue
        #     else:
        #         recommend_id_four = d
                
        
        
        rates=[]
        for aa in range(0,qwerty):
            
            for d in sim_dict:
                if sim_dict[d] == ram[aa]:
                    recommend_id = d
                    rates.append(recommend_id)
        irates=list(set(rates))
        asdf=len(irates)-1
                
        # import pdb ;pdb.set_trace()
        prod=[]
        prods=[]
        for bb in range(1,asdf):
            product_recommend=Rating.objects.filter (  id=irates[bb] ).last().product
            prod.append(product_recommend)
        # ilist = list(set(prod))
        for l in prod:
            if l not in prods:
                prods.append(l)

        # import pdb ;pdb.set_trace()
        if rams =='None' :
            context['score'] = 0
            context['product_recommend_one']=prods[0]
            context['product_recommend_two']=prods[1]
            context['product_recommend_three']=prods[2]
            context['product_recommend_four']=prods[3]
            return context
        else:
            context['score'] = obj.score
            context['product_recommend_one']=prods[0]
            context['product_recommend_two']=prods[1]
            context['product_recommend_three']=prods[2]
            context['product_recommend_four']=prods[3]
            return context



    # def get(self, request,*args,**kwargs):
    #     # el_id = request.GET.get('el_id')
    #     # el_ids = request.session.get('el_id')
        
    #     obj = Rating.objects.filter ( product=1 ).order_by ( "id" ).last ()
        
    #     objs= Product.get_products_by_id
    #     # import pdb ;pdb.set_trace()
    #     context = {
    #         'score': obj.score,
    #         'product':objs
    #     }
    #     return render (request, 'product-details.html' ,context)

