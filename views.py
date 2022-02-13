import math
from django.shortcuts import render, redirect
from django.http import Http404
from django.views import View
from django.urls import reverse
from .forms import ReceiptForm, PayeeForm
from .models import Receipt, SpendingAccount, Profile
from datetime import datetime, timedelta
from base64 import b64encode, b64decode


def build_path(request):
    return request.META['PATH_INFO'] + "?" + request.META['QUERY_STRING']


def build_path_base64(request):
    return b64encode(build_path(request).encode('utf-8')).decode('utf-8')


def offset_month(dt, offset):
    """
    Return datetime containing 1st day of month offset by `offset` months
    from the given datetime `dt`.
    """
    if offset == 0:
        return datetime(dt.year, dt.month, 1)
    total = dt.year * 12 + dt.month + offset
    year = math.floor(total/12)
    month = total % 12
    if month == 0:
        year -= 1
        month = 12
    return datetime(year, month, 1)


# Create your views here.
class add_receipt(View):
    # TODO: Add authentication here
    def get(self, request):
        # TODO: Add possibility for editing with the same view
        context = {'id': 0, 'path': build_path_base64(request)}
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
        return render(request, "receipt_add.html", context=context)

    def post(self, request):
        f = ReceiptForm(request.POST)
        if request.POST['id'] != "0":
            f.instance = Receipt.objects.get(id=int(request.POST['id']))
        if f.is_valid():
            new_receipt = f.save()
            return redirect('list_view')
        else:
            return render(request, "receipt_add.html", context={'form': f})


class receipt_delete(View):
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

        return render(request, 'receipt_delete.html', {'receipt': receipt})


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
        payees = SpendingAccount.objects.filter(owner=Profile.objects.get(user=request.user))
        return render(request, 'payee_list.html', {'payees': payees})


class payee_add(View):
    def get(self, request):
        context = {'id': 0}
        if 'next' in request.GET.keys():
            context['next'] = request.GET['next']
        if 'payee' in request.GET.keys():
            p = SpendingAccount.objects.get(id=request.GET['payee'])
            f = PayeeForm({'name': p.name})
            context['form'] = f
            context['id'] = p.id
        else:
            context['form'] = PayeeForm()
        return render(request, "payee_add.html", context)

    def post(self, request):
        f = PayeeForm(request.POST)
        if request.POST['id'] != "0":
            f.instance = SpendingAccount.objects.get(id=int(request.POST['id']))
        f.instance.owner = Profile.objects.get(user=request.user)
        if f.is_valid():
            f.save()
            path = "payee_list"
            if 'next' in request.GET.keys():
                path = b64decode(request.GET['next']).decode('utf-8')
            return redirect(path)
        return render(request, "payee_add.html", context={'form': f})


class payee_delete(View):
    # TODO: Check that the payee is user's. Return 404 otherwise
    def get(self, request):
        try:
            pk = int(request.GET['payee'])
        except:
            return Http404("Payee doesn't exist")

        payee = SpendingAccount.objects.get(id=pk)

        if 'confirmed' in request.GET.keys():
            if request.GET['confirmed'] == "1":
                payee.delete()
                return redirect("payee_list")

        return render(request, 'payee_delete.html', {'payee': payee})


class payee_transactions(View):
    def get(self, request):
        context = {
            'payee': SpendingAccount.objects.get(id=request.GET['payee']),
        }
        if 'from' in request.GET.keys():
            context['current_date'] = datetime.fromisoformat(request.GET['from'])
        else:
            context['current_date'] = datetime.now()
        offset_from = datetime(context['current_date'].year, context['current_date'].month, 1)
        context['prev_month_from'] = offset_month(offset_from, -1)
        context['prev_month_to'] = offset_month(offset_from, 0) - timedelta(1)
        context['next_month_from'] = offset_month(offset_from, 1)
        context['next_month_to'] = offset_month(offset_from, 2) - timedelta(1)
        context['current_date_verbose'] = context['current_date'].strftime("%B %Y")
        context['receipts'] = Receipt.objects.filter(
            to_account=context['payee'],
            date__gte=offset_from,
            date__lt=context['next_month_from']
        )
        context['total'] = sum([x.amount for x in context['receipts']])
        return render(request, 'payee_transactions.html', context)
