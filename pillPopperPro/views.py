from django.shortcuts import render

  
def home_page(request):
    # render takes: (1) the request,
    #               (2) the name of the view to generate, and
    #               (3) a dictionary of name-value pairs of data to be
    #                   available to the view.
    #context = {}
    #context['status'] = "welcome to wordish :) ;)"
    #if request.user != "":
        #return render(request, 'globalStreamPage.html', context)
    return render(request, 'home.html', {})

def dispense(request):
    # render takes: (1) the request,
    #               (2) the name of the view to generate, and
    #               (3) a dictionary of name-value pairs of data to be
    #                   available to the view.
    #context = {}
    #context['status'] = "welcome to wordish :) ;)"
    #if request.user != "":
        #return render(request, 'globalStreamPage.html', context)
    return render(request, 'dispense.html', {})

def pill_box(request):
    # render takes: (1) the request,
    #               (2) the name of the view to generate, and
    #               (3) a dictionary of name-value pairs of data to be
    #                   available to the view.
    #context = {}
    #context['status'] = "welcome to wordish :) ;)"
    #if request.user != "":
        #return render(request, 'globalStreamPage.html', context)
    return render(request, 'pillBox.html', {})