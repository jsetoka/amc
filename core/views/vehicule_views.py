from django.contrib.auth.decorators import login_required
from core.models import Vehicule
from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import Paginator
from core.form import VehicleForm

################################################################################
@login_required
def vehicle_list(request):
    vehicles = Vehicule.objects.filter(utilisateur=request.user).order_by('marque','modele')
    paginator = Paginator(vehicles, 10 )  # 5 abonnements par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'vehicules/list.html', {
      'vehicles': page_obj,
      'page_obj': page_obj
    })  

#@user_passes_test(is_client, login_url='login')
def vehicle_detail(request, pk):
    vehicle = get_object_or_404(Vehicule, pk=pk, utilisateur=request.user)
    return render(request, 'vehicules/detail.html', {'vehicle': vehicle})

@login_required
def vehicle_create(request):
    form = VehicleForm(request.POST or None)
    if form.is_valid():
        vehicle = form.save(commit=False)
        vehicle.utilisateur = request.user
        vehicle.save()
        return redirect('vehicle_list')
    form.initial['utilisateur'] = request.user
    return render(request, 'vehicules/form.html', {'form': form})

def vehicle_update(request, pk):
    vehicle = get_object_or_404(Vehicule, pk=pk, utilisateur=request.user)
    form = VehicleForm(request.POST or None, instance=vehicle)
    if form.is_valid():
        form.save()
        return redirect('vehicle_detail', pk=pk)
    return render(request, 'vehicules/form.html', {'form': form})

def vehicle_delete(request, pk):
    vehicle = get_object_or_404(Vehicule, pk=pk, utilisateur=request.user)
    if request.method == 'POST':
        vehicle.delete()
        return redirect('vehicle_list')
    return render(request, 'vehicules/confirm_delete.html', {'vehicle': vehicle})
