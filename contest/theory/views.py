from django.shortcuts import render


def theory_hash(request):
    template = 'theory/hash.html'
    return render(request, template,)
