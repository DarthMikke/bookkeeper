import math
from django.shortcuts import render, redirect
from django.http import Http404
from django.views import View
from django.urls import reverse
from .forms import ReceiptForm, PayeeForm, BankAccountForm
from .models import Receipt, SpendingAccount, Profile, BankAccount
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
    year = math.floor(total / 12)
    month = total % 12
    if month == 0:
        year -= 1
        month = 12
    return datetime(year, month, 1)


# Create your views here.
class ReceiptAdd(View):
    # TODO: Add authentication here
    def get(self, request):
        # TODO: Add possibility for editing with the same view
        context = {'id': 0, 'path': build_path_base64(request)}
        if 'receipt' in request.GET.keys():
            print(f"Hentar kvittering {request.GET['receipt']}...")
            r = Receipt.objects.get(id=request.GET['receipt'])
            print(r)
            context['form'] = ReceiptForm(Profile.objects.get(user=request.user), {
                'from_account': r.from_account,
                'to_account': r.to_account,
                'date': r.date,
                'amount': r.amount
            })
            context['id'] = r.id
        else:
            dt = request.GET['date'] if 'date' in request.GET.keys() else datetime.now()
            context["form"] = ReceiptForm(Profile.objects.get(user=request.user), {'date': dt})
        return render(request, "receipt_add.html", context=context)

    def post(self, request):
        f = ReceiptForm(Profile.objects.get(user=request.user), request.POST)
        if request.POST['id'] != "0":
            f.instance = Receipt.objects.get(id=int(request.POST['id']))
        if f.is_valid():
            new_receipt = f.save()
            return redirect('list_view')
        else:
            return render(request, "receipt_add.html", context={'form': f})


class ReceiptDelete(View):
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


class List(View):
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
        context['receipts'] = Receipt.objects.filter(date__gte=context['day'], date__lt=context['day'] + timedelta(1))

        context['total'] = sum([x.amount for x in context['receipts']])

        return render(request, "list.html", context=context)


class PayeeList(View):
    def get(self, request):
        payees = SpendingAccount.objects.filter(owner=Profile.objects.get(user=request.user))
        return render(request, 'payee_list.html', {'payees': payees})


class PayeeAdd(View):
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


class PayeeDelete(View):
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


class BankAccountList(View):
    def get(self, request):
        accounts = BankAccount.objects.filter(owner=Profile.objects.get(user=request.user))
        return render(request, 'bank_account_list.html', {'accounts': accounts})


class BankAccountAdd(View):
    def get(self, request):
        context = {'id': 0}
        if 'next' in request.GET.keys():
            context['next'] = request.GET['next']
        if 'account' in request.GET.keys():
            a = BankAccount.objects.get(id=request.GET['account'])
            f = BankAccountForm({'name': a.name, 'balance': a.balance})
            context['form'] = f
            context['id'] = a.id
        else:
            context['form'] = BankAccountForm()
        return render(request, "bank_account_add.html", context)

    def post(self, request):
        f = BankAccountForm(request.POST)
        if request.POST['id'] != "0":
            f.instance = BankAccount.objects.get(id=int(request.POST['id']))
        f.instance.owner = Profile.objects.get(user=request.user)
        # f.instance.currency = "NOK"
        if f.is_valid():
            f.save()
            path = "bank_account_list"
            if 'next' in request.GET.keys():
                path = b64decode(request.GET['next']).decode('utf-8')
            return redirect(path)
        return render(request, "bank_account_add.html", context={'form': f})


class BankAccountDelete(View):
    def get(self, request):
        try:
            pk = int(request.GET['account'])
        except:
            return Http404("Account doesn't exist")

        account = BankAccount.objects.get(id=pk)

        if 'confirmed' in request.GET.keys():
            if request.GET['confirmed'] == "1":
                account.delete()
                return redirect("bank_account_list")

        return render(request, 'bank_account_delete.html', {'account': account})


class MonthlyList(View):
    def get(self, request):
        context = {}
        if 'from' in request.GET.keys():
            context['current_date'] = datetime.fromisoformat(request.GET['from'])
        else:
            context['current_date'] = datetime.now()
        context['offset_from'] = datetime(context['current_date'].year, context['current_date'].month, 1)
        context['prev_month_from'] = offset_month(context['offset_from'], -1)
        context['prev_month_to'] = context['offset_from']
        context['next_month_from'] = offset_month(context['offset_from'], 1)
        context['next_month_to'] = offset_month(context['offset_from'], 2)
        context['current_date_verbose'] = context['current_date'].strftime("%B %Y")

        additional_query = "&".join([f"{x}={y}" for (x, y) in request.GET.items() if x in ['account', 'payee']])
        print(additional_query)
        context['prev_path'] = request.path + "?" + additional_query \
            + "&from=" + context['prev_month_from'].isoformat() \
            + "&to=" + context['prev_month_to'].isoformat()
        context['next_path'] = request.path + "?" + additional_query \
            + "&from=" + context['next_month_from'].isoformat() \
            + "&to=" + context['next_month_to'].isoformat()
        filters = {
            'date__gte': context['offset_from'],
            'date__lt': context['next_month_from'],
        }
        if 'account' in request.GET.keys():
            filters['from_account_id'] = request.GET['account']
            context['account'] = BankAccount.objects.get(id=request.GET['account'])
        if 'payee' in request.GET.keys():
            filters['to_account_id'] = request.GET['payee']
            context['payee'] = SpendingAccount.objects.get(id=request.GET['payee'])
        context['receipts'] = Receipt.objects.filter(**filters)
        context['total'] = sum([x.amount for x in context['receipts']])
        return render(request, 'monthly_list.html', context)
