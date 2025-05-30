from core.form import RendezvousForm
from django.shortcuts import render
def rendezvous(request):
    motif = request.GET.get("motif")
    if request.method == 'POST':
        form = RendezvousForm(request.POST)
        if form.is_valid():
            rendezvous_obj = form.save(commit=False)
            rendezvous_obj.motif = motif
            rendezvous_obj.save()
            return render(request, 'rendezvous/rendezvous_success.html')
    else:
        form = RendezvousForm()
    return render(request, 'rendezvous/rendezvous.html', {'form': form})