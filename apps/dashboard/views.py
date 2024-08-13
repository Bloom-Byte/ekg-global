from django.views import generic


class IndexView(generic.TemplateView):
    template_name = 'dashboard/index.html'


index_view = IndexView.as_view()
