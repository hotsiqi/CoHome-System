from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseForbidden,HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import OwnerRegisterForm, SearcherRegisterForm, UserLoginForm, ContractForm, HouseUnitForm, HouseImageFormSet,HouseUnitSearchForm,ProfileEditForm ,PaymentProofForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django import forms
from .models import Notification
from django.db.models import Q
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect, get_object_or_404
from .models import HouseUnit, Contract,Favorite, Transaction
from .forms import TechnicianReportForm
from django.contrib.auth.models import User
from django.shortcuts import render
from django.utils import timezone
from django.http import Http404
from .models import Profile
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm





def register(request):
    if request.method == 'POST':
        form = SearcherRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            full_name = form.cleaned_data.get('full_name')
            # Create or update the profile with the full name
            profile, created = Profile.objects.get_or_create(user=user)
            profile.full_name = full_name
            profile.save()

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')

            group_name = 'Searcher'
            group, created = Group.objects.get_or_create(name=group_name)

            user = authenticate(request, username=username, password=password)
            user.groups.add(group)
            messages.success(request, 'Your account has been created! You are now able to login!')
            return redirect('login')
    else:
        form = SearcherRegisterForm()
    return render(request, 'users/register.html', {'form': form})

def owner_register(request):
    if request.method == 'POST':
        form = OwnerRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            full_name = form.cleaned_data.get('full_name')
            bank_account_number = form.cleaned_data.get('bank_account_number')
            profile = user.profile
            profile.full_name = full_name
            profile.bank_account_number = bank_account_number
            profile.save()

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')

            group_name = 'Owner'
            group, created = Group.objects.get_or_create(name=group_name)

            user = authenticate(request, username=username, password=password)
            user.groups.add(group)
            messages.success(request, 'Your account has been created! You are now able to log in!')
            return redirect('login')
    else:
        form = OwnerRegisterForm()
    return render(request, 'users/owner_register.html', {'form': form})



def login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                if user.groups.filter(name='Searcher').exists():
                    return redirect('searcher_main')
                elif user.groups.filter(name='technician').exists():
                    return redirect('technician_main')
                elif user.groups.filter(name='Tenant').exists():
                    return redirect('tenant_main')
                else: 
                    return redirect('owner_main')
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form})

@login_required
def posthome(request):
    return render(request, 'users/posthome.html')

@login_required
def owner_main(request):
    return render(request, 'users/owner_main.html')

@login_required
def searcher_main(request):
    return render(request, 'users/searcher_main.html')

@login_required
def technician_main(request):
    return render(request, 'users/technician_main.html')

@login_required
def tenant_main(request):
    return render(request, 'users/tenant_main.html')


def is_technician(user):
    return user.groups.filter(name='technician').exists()


def user_redirect(request):
    
    if request.user.groups.filter(name='Owner').exists():
        return redirect('owner_main')
    elif request.user.groups.filter(name='Searcher').exists():
        return redirect('searcher_main')
    elif request.user.groups.filter(name='Tenant').exists():
        return redirect('tenant_main') 
    elif request.user.groups.filter(name='technician').exists():
        return redirect('technician_main')
    else:
        return redirect('home')



@login_required
def post_unit(request):
    if request.method == 'POST':
        form = HouseUnitForm(request.POST)
        if form.is_valid():
            house_unit = form.save(commit=False)
            house_unit.owner = request.user
            house_unit.save()
            
            formset = HouseImageFormSet(request.POST, request.FILES, instance=house_unit)
            if formset.is_valid():
                formset.save()
                messages.success(request, 'House unit is now pending post.')
                return redirect('owner_main')
            
                
    else:
        form = HouseUnitForm()
        formset = HouseImageFormSet()
    return render(request, 'users/post_unit.html', {'form': form, 'formset': formset})


@login_required
def house_unit_list(request):
    search_form = HouseUnitSearchForm(request.GET or None)
    house_units = HouseUnit.objects.exclude(contracts__isnull=False)

    if search_form.is_valid():
        description = search_form.cleaned_data.get('description', '')
        house_type = search_form.cleaned_data.get('house_type', '')
        min_price = search_form.cleaned_data.get('min_price', None)
        max_price = search_form.cleaned_data.get('max_price', None)

        if description:
            house_units = house_units.filter(description__icontains=description)
        if house_type:
            house_units = house_units.filter(house_type=house_type)
        if min_price is not None:
            house_units = house_units.filter(price__gte=min_price)
        if max_price is not None:
            house_units = house_units.filter(price__lte=max_price)

    return render(request, 'users/contract.html', {
        'house_units': house_units,
        'search_form': search_form,
    })

@login_required
def house_unit_detail(request, house_unit_id):
    house_unit = get_object_or_404(HouseUnit, pk=house_unit_id)
    contracts = house_unit.contracts.all()

    is_tenant = request.user.groups.filter(name='Tenant').exists()
    is_searcher = request.user.groups.filter(name='Searcher').exists()
    is_technician = request.user.groups.filter(name='technician').exists()

    if is_searcher or is_tenant:
        # For Searcher or Tenant, use a different template or include logic in the template
        context = {
            'house_unit': house_unit,
            'is_tenant': is_tenant,
            'is_searcher': is_searcher,
            'is_technician': is_technician,
            'contracts': contracts,
        }
        return render(request, 'users/house_unit_detail_searcher.html', context)
    elif is_technician:
        # For Technician, additional functionality to upload contracts
        if request.method == 'POST':
            contract_form = ContractForm(request.POST, request.FILES, initial={'house_unit': house_unit})
            if contract_form.is_valid():
                contract = contract_form.save(commit=False)
                contract.uploaded_by = request.user
                contract.house_unit = house_unit
                contract.save()
                messages.success(request, 'Contract uploaded successfully.')
                return redirect('contract')
        else:
            contract_form = ContractForm(initial={'house_unit': house_unit})

        context = {
            'house_unit': house_unit,
            'contracts': contracts,
            'form': contract_form,
            'is_technician': is_technician,
            'is_tenant': is_tenant,
            'is_searcher': is_searcher,
        }
        return render(request, 'users/house_unit_detail.html', context)

    return HttpResponseForbidden("You do not have permission to view this page.")
@login_required
def submit_report(request):
    if request.method == 'POST':
        form = TechnicianReportForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.technician = request.user  # Assign the current user as the technician
            messages.success(request,f'Your report has been created !')
            form.save()
            return redirect('technician_main')  # Redirect to a success page or another appropriate page
    else:
        form = TechnicianReportForm()
    return render(request, 'users/submit_report.html', {'form': form})



@login_required
@user_passes_test(is_technician)
def users_list(request):
    users = User.objects.exclude(groups__name__in=['Admin', 'technician']).prefetch_related('groups')
    return render(request, 'users/users_list.html', {'users': users})


@login_required
def search_with_contracts(request):
    search_form = HouseUnitSearchForm(request.GET or None)
    house_units_with_contracts = HouseUnit.objects.filter(contracts__isnull=False).distinct()

    if search_form.is_valid():
        description = search_form.cleaned_data.get('description')
        house_type = search_form.cleaned_data.get('house_type')
        min_price = search_form.cleaned_data.get('min_price')
        max_price = search_form.cleaned_data.get('max_price')

        if description:
            house_units_with_contracts = house_units_with_contracts.filter(description__icontains=description)
        if house_type:
            house_units_with_contracts = house_units_with_contracts.filter(house_type=house_type)
        if min_price is not None:
            house_units_with_contracts = house_units_with_contracts.filter(price__gte=min_price)
        if max_price is not None:
            house_units_with_contracts = house_units_with_contracts.filter(price__lte=max_price)

    return render(request, 'users/search_with_contracts.html', {
        'house_units': house_units_with_contracts,
        'search_form': search_form,
    })

@login_required
def add_to_favorites(request, house_unit_id):
    if request.method == "POST":
        house_unit = get_object_or_404(HouseUnit, pk=house_unit_id)
        _, created = Favorite.objects.get_or_create(user=request.user, house_unit=house_unit)
        if created:
            messages.success(request,f'Done Added to Favourite !')
            pass
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    return HttpResponseForbidden("Invalid request")

@login_required
def favorites_view(request):
    favorites = Favorite.objects.filter(user=request.user)
    return render(request, 'users/favorites.html', {'favorites': favorites})

@login_required
def view_user_profile(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        # If no profile exists, you might want to handle it differently
        # For instance, you might redirect to a page to create a profile or show a custom error message
        raise Http404("Profile does not exist.")

    context = {
        'profile': profile,
    }
    return render(request, 'users/view_profile.html', context)


@login_required
def edit_profile(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile(user=request.user)

    profile_form = ProfileEditForm(instance=profile)
    password_form = PasswordChangeForm(user=request.user)

    if request.method == 'POST':
        if 'profile_form_submit' in request.POST:
            profile_form = ProfileEditForm(request.POST, instance=profile)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, 'Your profile has been updated successfully!')
                return redirect('view_profile')
        elif 'password_form_submit' in request.POST:
            password_form = PasswordChangeForm(user=request.user, data=request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)  # Important
                messages.success(request, 'Your password has been updated successfully!')
                return redirect('view_profile')
            else:
                messages.error(request, 'Please correct the error below.')

    return render(request, 'users/edit_profile.html', {
        'profile_form': profile_form,
        'password_form': password_form
    })
@login_required
def make_payment(request, house_unit_id):
    house_unit = get_object_or_404(HouseUnit, pk=house_unit_id)
    is_tenant_of_house = house_unit.transactions.filter(user=request.user, verified_at__isnull=False).exists()

    if house_unit.status == 'rented' and not is_tenant_of_house:   
        messages.error(request, "This house has been rented out and is no longer available for new payments.")
        return redirect('house_unit_detail', house_unit_id=house_unit_id)

    form = PaymentProofForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        transaction, created = Transaction.objects.get_or_create(
            user=request.user,
            house_unit=house_unit,
            defaults={'amount': house_unit.price}
        )
        payment_proof = form.save(commit=False)
        payment_proof.user = request.user
        payment_proof.transaction = transaction
        payment_proof.save()
        
        messages.success(request, "Payment proof uploaded successfully.")
        return redirect('house_unit_detail', house_unit_id=house_unit_id)
    
    context = {
        'house_unit': house_unit,
        'form': form,
        'company_bank_account': '123-456-789',  # Example bank account number
        'qr_code_image': 'path/to/your/qr_code.jpg'  # Relative path to the QR code image within your static files
    }
    return render(request, 'users/make_payment.html', context)


def is_tenant(user):
    return user.groups.filter(name='Tenant').exists()

@login_required
@user_passes_test(is_tenant)
def make_payment_for_tenant(request, house_unit_id):
    house_unit = get_object_or_404(HouseUnit, pk=house_unit_id, status='rented')

    # Ensure the current user is renting this house
    if not Transaction.objects.filter(user=request.user, house_unit=house_unit, verified_at__isnull=False).exists():
        messages.error(request, "You are not renting this house.")
        return redirect('tenant_rented_houses')

    form = PaymentProofForm(request.POST or None, request.FILES or None)
    
    if request.method == 'POST' and form.is_valid():
        # Always create a new transaction for each payment attempt
        transaction = Transaction.objects.create(
            user=request.user,
            house_unit=house_unit,
            amount=house_unit.price,  # Assuming the rental price does not change
            processed=False  # Mark the transaction as not processed initially
        )

        # Save the payment proof with the newly created transaction
        payment_proof = form.save(commit=False)
        payment_proof.user = request.user
        payment_proof.transaction = transaction
        payment_proof.save()

        messages.success(request, "Payment proof uploaded successfully. Awaiting verification.")
        return redirect('tenant_rented_houses')
    else:
        return render(request, 'users/tenant_make_payment.html', {
            'house_unit': house_unit,
            'form': form
        })


@login_required
@user_passes_test(is_technician)
def manage_transactions(request):
    transactions = Transaction.objects.filter(processed=False).prefetch_related('payment_proofs')
    return render(request, 'users/manage_transactions.html', {'transactions': transactions})

@login_required
@user_passes_test(lambda user: user.groups.filter(name='technician').exists())
def not_verify_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, pk=transaction_id)
    transaction.processed = True
    if transaction.house_unit:
        transaction.house_unit.status = 'available'
        transaction.house_unit.save()
    transaction.save()

    # Create a notification for the searcher indicating the payment was not verified
    Notification.objects.create(
        recipient=transaction.user,
        message="Your payment was not verified. Please make a payment again."
    )
    messages.info(request, "Transaction marked as not verified. The house unit is now available again.")
    return redirect('manage_transactions')


@login_required
@user_passes_test(is_technician)
def verify_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, pk=transaction_id)
    transaction.processed = True
    transaction.verified_at = timezone.now()
    transaction.save()
    transaction.house_unit.status = 'rented'
    transaction.house_unit.save()


    if not transaction.user.groups.filter(name='Tenant').exists():
        tenant_group, _ = Group.objects.get_or_create(name='Tenant')
        searcher_group = Group.objects.get(name='Searcher')
        transaction.user.groups.remove(searcher_group)
        transaction.user.groups.add(tenant_group)

    Notification.objects.create(
        recipient=transaction.user,
        message="Your payment has been verified. You are now the tenant."
    )
    Notification.objects.create(
        recipient=transaction.house_unit.owner,
        message=f"Your house has been rented out. You can contact {transaction.user.email}."
    )
    messages.success(request, "Transaction verified successfully, and the house unit is now marked as rented out.")
    return redirect('manage_transactions')




@login_required
def notifications(request):
    user_notifications = request.user.notifications.order_by('-created_at').all()
    return render(request, 'users/notifications.html', {'notifications': user_notifications})

@login_required
def view_transactions_for_owner(request):
    # Get all house units owned by the current user
    owned_house_units = HouseUnit.objects.filter(owner=request.user)
    transactions = Transaction.objects.filter(
        house_unit__in=owned_house_units, 
        verified_at__isnull=False
    ).select_related('house_unit', 'user').order_by('-transaction_date')
    
    return render(request, 'users/owner_transactions.html', {'transactions': transactions})


@login_required
def tenant_transactions(request):
    if not request.user.groups.filter(name='Tenant').exists():
        return HttpResponseForbidden("You are not authorized to view this page.")

    transactions = Transaction.objects.filter(user=request.user).order_by('-transaction_date')
    
    return render(request, 'users/tenant_transactions.html', {'transactions': transactions})


@login_required
def tenant_rented_houses(request):
    if not request.user.groups.filter(name='Tenant').exists():
        return HttpResponseForbidden("You are not authorized to view this page.")

    rented_houses = HouseUnit.objects.filter(
        transactions__user=request.user,
        transactions__verified_at__isnull=False
    ).distinct().order_by('location')
    
    return render(request, 'users/tenant_rented_houses.html', {'rented_houses': rented_houses})
