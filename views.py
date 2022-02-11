from django.shortcuts import render, redirect
from django.views import View
from .forms import ReceiptForm
from .models import Receipt
from datetime import datetime


# Create your views here.
class add_receipt(View):
    # TODO: Add authentication here
    def get(self, request):
        # TODO: Add possibility for editing with the same view
        context = {"form": ReceiptForm()}
        return render(request, "add_receipt.html", context=context)

    def post(self, request):
        f = ReceiptForm(request.POST)
        if f.is_valid():
            new_receipt = f.save()
            return redirect('list_view')
        else:
            return render(request, "add_receipt.html", context={'form': f})


class list(View):
    def get(self, request):
        context = {}
        if 'day' in request.GET.keys():
            context['day'] = datetime.fromisoformat(request['day'])
        else:
            context['day'] = datetime.now()
        weekdate = context['day'].isocalendar()
        context['days'] = [datetime.fromisocalendar(weekdate[0], weekdate[1], i) for i in range(1, 8)]
        context['receipts'] = Receipt.objects.filter(date__gte=context['day'], date__lte=context['day'])

        return render(request, "list.html", context=context)
