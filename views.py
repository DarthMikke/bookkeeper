from django.shortcuts import render, redirect
from django.http import Http404
from django.views import View
from django.urls import reverse
from .forms import ReceiptForm, PayeeForm
from .models import Receipt, SpendingAccount, Profile
from datetime import datetime, timedelta


# Create your views here.
class add_receipt(View):
    # TODO: Add authentication here
    def get(self, request):
        # TODO: Add possibility for editing with the same view
        context = {'id': 0}
        if 'receipt' in request.GET.keys():
            print(f"Hentar kvittering {request.GET['receipt']}...")
            r = Receipt.objects.get(id=request.GET['receipt'])
            print(r)
            context['form'] = ReceiptForm({
                'from_account': r.from_account,
                'to_account': r.to_account,
                'date': r.date,
                'amount': r.amount
            })
            context['id'] = r.id
        else:
            context["form"] = ReceiptForm()
        return render(request, "add_receipt.html", context=context)

    def post(self, request):
        f = ReceiptForm(request.POST)
        if request.POST['id'] != "0":
            f.instance = Receipt.objects.get(id=int(request.POST['id']))
        if f.is_valid():
            new_receipt = f.save()
            return redirect('list_view')
        else:
            return render(request, "add_receipt.html", context={'form': f})


class delete_receipt(View):
    # TODO: Check that the receipt is user's. Return 404 otherwise
    def get(self, request):
        try:
            pk = int(request.GET['receipt'])
        except:
            return Http404("Receipt doesn't exist")

        receipt = Receipt.objects.get(id=pk)

        if 'confirmed' in request.GET.keys():
            if request.GET['confirmed'] == "1":
                receipt.delete()
                return redirect('list_view')

        return render(request, 'delete_receipt.html', {'receipt': receipt})


class list(View):
    def get(self, request):
        context = {}
        if 'day' in request.GET.keys():
            context['day'] = datetime.fromisoformat(request.GET['day'])
        else:
            context['day'] = datetime.now().date()
        weekdate = context['day'].isocalendar()
        context['prev_week'] = context['day'] - timedelta(7)
        context['next_week'] = context['day'] + timedelta(7)
        context['days'] = [datetime.fromisocalendar(weekdate[0], weekdate[1], i) for i in range(1, 8)]
        context['receipts'] = Receipt.objects.filter(date__gte=context['day'], date__lt=context['day']+timedelta(1))

        context['total'] = sum([x.amount for x in context['receipts']])

        return render(request, "list.html", context=context)


class payee_list(View):
    def get(self, request):

        ...


class add_payee(View):
    def get(self, request):
        context = {'id': 0}
        if 'payee' in request.GET.keys():
            p = SpendingAccount.objects.get(id=request.GET['payee'])
            f = PayeeForm({'name': p.name})
            context['form'] = f
            context['id'] = p.id
        else:
            context['form'] = PayeeForm()
        return render(request, "add_payee.html", context)

    def post(self, request):
        f = PayeeForm(request.POST)
        if request.POST['id'] != "0":
            f.instance = SpendingAccount.objects.get(id=int(request.POST['id']))
        f.instance.owner = Profile.objects.get(user=request.user)
        if f.is_valid():
            f.save()
            path = reverse('add_receipt')
            if 'receipt' in request.GET.keys():
                path += f"?receipt={request.GET['receipt']}"
            return redirect(path)
        return render(request, "add_payee.html", context={'form': f})
