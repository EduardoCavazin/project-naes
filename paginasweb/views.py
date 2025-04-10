from django.views.generic import TemplateView

class IndexView(TemplateView):
    template_name = "paginasweb/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        return context

class AboutView(TemplateView):
    template_name = "paginasweb/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
