from django.shortcuts import render, redirect
from django.views import View
from .forms import ReceiptForm


# Create your views here.
class add_receipt(View):
    # TODO: Add authentication here
    def get(self, request):
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
        ...
