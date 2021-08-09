from currency.forms import RateForm, SourceForm
from currency.models import ContactUs, Rate, Source

from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView


class IndexView(TemplateView):
    template_name = 'index.html'


class ContactUsListView(ListView):
    queryset = ContactUs.objects.all()
    template_name = 'contact_us.html'


class RateListView(ListView):
    queryset = Rate.objects.all()
    template_name = 'rate_list.html'


class RateCreateView(CreateView):
    queryset = Rate.objects.all()
    form_class = RateForm
    success_url = reverse_lazy('currency:rate-list')
    template_name = 'create_rate.html'


class RateDeleteView(DeleteView):
    queryset = Rate.objects.all()
    success_url = reverse_lazy('currency:rate-list')
    template_name = 'delete_rate.html'


class RateUpdateView(UpdateView):
    queryset = Rate.objects.all()
    form_class = RateForm
    success_url = reverse_lazy('currency:rate-list')
    template_name = 'update_rate.html'


class RateDetailView(DetailView):
    queryset = Rate.objects.all()
    template_name = 'rate_details.html'


class SourceListView(ListView):
    queryset = Source.objects.all()
    template_name = 'source_list.html'


class SourceCreateView(CreateView):
    queryset = Source.objects.all()
    form_class = SourceForm
    success_url = reverse_lazy('currency:source-list')
    template_name = 'create_source.html'


class SourceDeleteView(DeleteView):
    queryset = Source.objects.all()
    success_url = reverse_lazy('currency:source-list')
    template_name = 'delete_source.html'


class SourceUpdateView(UpdateView):
    queryset = Source.objects.all()
    form_class = SourceForm
    success_url = reverse_lazy('currency:source-list')
    template_name = 'update_source.html'


class SourceDetailView(DetailView):
    queryset = Source.objects.all()
    template_name = 'source_details.html'


class EmailCreateView(CreateView):
    model = ContactUs
    success_url = reverse_lazy('index')
    template_name = 'create_email.html'
    fields = (
            'email_from',
            'subject',
            'message',
    )

    # form.clean_data - провалидированные данные
    def form_valid(self, form):
        email = form.cleaned_data['email_from']
        subject = form.cleaned_data['subject']
        text = form.cleaned_data['message']

        full_email = f'''
        Email from: {email}
        Subject: {subject}
        Message: {text}

        '''

        send_mail(
            subject,
            full_email,
            settings.EMAIL_HOST,
            [settings.SUPPORT_EMAIL],
            fail_silently=False,
        )

        return super().form_valid(form)
