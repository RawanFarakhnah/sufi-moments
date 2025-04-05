from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from .models import Memory
from .forms import MemoryForm

def memory_create(request):
    if request.method == 'POST':
        form = MemoryForm(request.POST, request.FILES)
        if form.is_valid():
            memory = form.save(commit=False)
            memory.user = request.user
            memory.save()
            messages.success(request, _('Memory created successfully!'))
            return redirect('list')
    else:
        form = MemoryForm()
    
    # Attach request to the form for user assignment in save()
    form.request = request
    return render(request, 'memories/memory_form.html', {'form': form})

def memory_update(request, pk):
    memory = get_object_or_404(Memory, pk=pk, user=request.user)
    if request.method == 'POST':
        form = MemoryForm(request.POST, request.FILES, instance=memory)
        if form.is_valid():
            form.save()
            messages.success(request, _('Memory updated successfully!'))
            return redirect('list')
    else:
        form = MemoryForm(instance=memory)
    
    form.request = request
    return render(request, 'memories/memory_form.html', {'form': form})

def memory_delete(request, pk):
    memory = get_object_or_404(Memory, pk=pk, user=request.user)
    if request.method == 'POST':
        memory.delete()
        messages.success(request, _('Memory deleted successfully!'))
        return redirect('list')
    return render(request, 'memories/memory_confirm_delete.html', {'memory': memory})

def memory_list(request):
    memories = Memory.objects.all().order_by('-created_at')
    return render(request, 'memories/list.html', {'memories': memories})

def memory_detail(request, pk):
    memory = get_object_or_404(Memory, pk=pk)
    return render(request, 'memories/detail.html', {'memory': memory})

def toggle_like(request, pk):
    memory = get_object_or_404(Memory, pk=pk)
    if request.user in memory.likes.all():
        memory.likes.remove(request.user)
    else:
        memory.likes.add(request.user)
    return redirect('memory_detail', pk=pk)