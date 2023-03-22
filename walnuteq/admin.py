from django.template.response import TemplateResponse
from django.urls import path

class ObservationAdmin(SimpleHistoryAdmin, SoftDeletionModelAdmin):
    change_list_template = 'export_link.html'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('export/', self.admin_site.admin_view(self.export_view), name='export')
        ]

        return custom_urls + urls

    def export_view(self, request):
        context = dict(
           self.admin_site.each_context(request),
        )

        return TemplateResponse(request, 'export.html', context)