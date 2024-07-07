from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .tasks import test_func

from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from asgiref.sync import async_to_sync
import json


from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator



# Create your views here.
def test(request):
    test_func.delay()
    return HttpResponse("Done")






def home(request):
    return render(request, 'index.html')


from django.views.decorators.csrf import csrf_protect

@csrf_protect
def logoutPage(request):
    logout(request)
    return redirect('loginPage')

@csrf_protect
def loginPage(request):
    if request.method == 'POST':
        number = request.POST['number']
        password = request.POST['password']

        user = authenticate(request, username=number, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page or any other desired page
            return redirect('home')
    return render(request, 'login.html')

@csrf_protect
def registerPage(request):
    if request.method == "POST":
        number = request.POST['number']
        password = request.POST['password']
        con_password = request.POST['con_password']

        if password == con_password:
            if User.objects.filter(username=number).exists():
                return redirect('registerPage')
            else:    
                # Create a new user instance
                new_user = User(username=number)
                new_user.set_password(password)
                new_user.save()
                user = authenticate(request, username=number, password=password)
                if user is not None:
                    login(request, user)
                    code = 'MEM' + user.username
                    profile = Profile.objects.create(user=user, user_code=code)
                return redirect('/')
        else:
            return render(request, 'register.html')
    return render(request, 'register.html')

def refRegister(request, *args, **kwargs):
    code = str(kwargs.get('ref_code'))
    try:
        profile = Profile.objects.get(code=code)
        request.session['ref_profile'] = profile.id
        print('id', profile.id)
    except:
        pass
    print(request.session.get_expiry_date())
    return render(request, 'register.html')

def accountPage(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except:
        pass
    if request.user.is_authenticated:
        return render(request, 'account.html', {'proflie': profile})
    else:
        return redirect('/loginPage')

def depositePage(request):
    profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        amount = request.POST.get('amount')
        utr_no = request.POST.get('utr_no')
        payment_img = request.FILES.get('payment_screenshot')

        # Validate and process the data as needed
        if amount and utr_no and payment_img:
            # Create a Deposit object
            deposit = Deposit.objects.create(user=request.user, amount=amount, utr_no=utr_no, payment_img=payment_img)
            # Optionally, you can save additional information or perform further actions

            messages.success(request, "Deposit will be processed soon")
        else:
            messages.error(request, "Form submission error. Please check your inputs.")

    return render(request, 'deposite.html', {'profile': profile})

def withdrawPage(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == "POST":
        try:
            amount = float(request.POST['amount'])
            upi_id = request.POST['upi_id']

            profile = Profile.objects.get(user=request.user)

            if amount <= profile.total_balance:
                Withdraw.objects.create(user=request.user, amount=amount, upi_id=upi_id)
                profile.total_balance -= amount
                profile.save()
                messages.success(request, "Withdrawal successful.")
            else:
                messages.error(request, "Insufficient balance.")
        except Profile.DoesNotExist:
            messages.error(request, "Profile does not exist.")
        except ValueError:
            messages.error(request, "Invalid amount entered.")
        
        return redirect('withdrawPage')
    
    return render(request, 'withdraw.html', {'profile': profile}) 

def walletPage(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except:
        pass
    if request.user.is_authenticated:
        return render(request, 'wallet.html', {'profile': profile})
    else:
        return redirect('/loginPage')


def aboutPage(request):
    return render(request, "about.html")


def settingsPage(request):
    return render(request, "settings.html")

def guidePage(request):
    return render(request, "guide.html")

def feedbackPage(request):
    return render(request, "feedback.html")



# from .models import GameRound, Bet
@login_required
def wingoPage(request):
    profile = Profile.objects.get(user=request.user)
    round_results = RoundWinColor.objects.all()
    paginator = Paginator(round_results, 10)  # Show 10 round results per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.method=='POST':
        bet_amount = request.POST['total_amount']
        bet_color = request.POST['bet_color']
        round = latest_round
        user = request.user

    return render(request, 'wingo.html', {'profile': profile, 'page_obj': page_obj})



from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import GameRound, Bet
import json
# from decimal import Decimal
@csrf_exempt
def user_bet(request):
    if request.method == 'POST':
        try:
            user = request.user
            data = json.loads(request.body.decode('utf-8'))
            profile = Profile.objects.get(user=user)
            round_id = data.get('id')
            bet_color = data.get('bet_color')
            bet_amount = data.get('amount')
            bet_amount = float(bet_amount)

            game_round = GameRound.objects.get(game_id=round_id)
            
            if profile.user_balance >= bet_amount:
                bet = Bet.objects.create(user=user, round=game_round, color=bet_color, amount=bet_amount)
                bet.save()
                profile.user_balance -= bet_amount
                profile.save()
                roundWinColor = RoundWinColor.objects.get(round=game_round)
                if bet_color =="Green":
                    roundWinColor.green_bet_amount += bet_amount
                    roundWinColor.save()
                elif bet_color == "Violet":
                    roundWinColor.violet_bet_amount += bet_amount
                    roundWinColor.save()
                else:
                    roundWinColor.red_bet_amount += bet_amount
                    roundWinColor.save()
                
                return JsonResponse({'message': 'success'})
            else:
                return JsonResponse({'message': 'error insufficient balance'})
                print("insufficient balance")


        except GameRound.DoesNotExist:
            return JsonResponse({'error': 'Game round does not exist'}, status=404)
        
        except Exception as e:
            print(e)
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)
