from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from store.models.rating import Rating
from django.http import request

class Rating ( View ):
    def post(self, request):
        el_id = request.POST.get('el_id')
        val = request.POST.get('val')
        obj = Rating.objects.get(id=el_id)
        if obj:
            obj.score = val
            obj.save()
            return JsonResponse({'success': 'true', 'score': val}, safe=False)
        return JsonResponse({'sucess': 'false'})

    def get(self, request):
        obj = Rating.objects.filter ( score=0 ).order_by ( "?" ).first ()
        context = {
            'product': obj
        }
        return render (request, 'product-details.html', context)
    
