from django.shortcuts import get_object_or_404, render,redirect
from .models import *
from .forms import *



# Create your views here.
def Address(request):
    

    context=AddressDetails.objects.filter(id=id)

    return render(request,'manageaddress.html',{'addr':context})


def manageaddress(request):
    user=request.user
    
    add=AddressDetails.objects.filter(user_id=user.id)

    
    return render(request,'manageaddress.html',locals())


def edit_address(request,id):
    address = get_object_or_404(AddressDetails, id=id, user=request.user)

    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            return redirect('manageaddress')
    else:
        form = AddressForm(instance=address)

    return render(request, 'edit_address.html', {'form': form})



def deleteaddress(request,id):
    dele=AddressDetails.objects.get(id=id)
    dele.delete()
    return redirect(manageaddress)


def add_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            return redirect('manageaddress')
    else:
        form = AddressForm()
    return render(request, 'add_address.html', {'form': form})
