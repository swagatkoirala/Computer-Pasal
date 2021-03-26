from django.shortcuts import render ,redirect
from django.views import View
from django.http import JsonResponse
from store.models.rating import Rating
from django.http import request

class RatingView( View ):
    def post(self, request):
        # import pdb ;pdb.set_trace()
        
        el_id = request.POST.get('el_id')
        val = request.POST.get('val')
        customer = request.session.get('customer')
        obj = Rating.objects.get(id=el_id)
        
        if obj:
            obj.score = val
            obj.save()
            import pdb ;pdb.set_trace()
            return JsonResponse({'success': 'true', 'score': val}, safe=False)
        return JsonResponse({'success': 'false'})

    def get(self, request):
        obj = Rating.objects.filter ( score=0 ).order_by ( "?" ).first ()
        context = {
            'product': obj
        }
        return render (request, 'rating.html', context)
    
