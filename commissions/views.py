from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from accounts.mixins import RoleRequiredMixin
from .forms import CommissionForm, JobFormSet
from .models import Commission, Job, JobApplication


class CommissionListView(ListView):
    model = Commission
    template_name  = "commissions/commission_list.html"
    context_object_name = "all_commissions"

    def get_queryset(self):
        return Commission.objects.all().order_by("status", "-created_on")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            profile = self.request.user.profile

            created = Commission.objects.filter(
                maker=profile
            ).order_by("status", "-created_on")

            applied = Commission.objects.filter(
                jobs__applications__applicant=profile
            ).distinct().exclude(
               maker=profile
            ).order_by("status", "-created_on")

            excluded_ids = list(created.values_list("id", flat=True)) + list(
                applied.values_list("id", flat=True)
            )

            all_commissions = Commission.objects.exclude(
                id__in=excluded_ids
            ).order_by("status", "-created_on")

            context["created_commissions"] = created
            context["applied_commissions"] = applied
            context["all_commissions"] = all_commissions
        
        return context
    

class CommissionDetailView(DetailView):
    model = Commission
    context_object_name = "commission"
    template_name = "commissions/commission_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        commission = self.object
        jobs = commission.jobs.all()

        total_manpower = 0
        total_open = 0

        job_data = []

        for job in jobs:
            accepted = job.applications.filter(status="1").count()
            open_slots = max(job.manpower_required - accepted, 0)

            total_manpower += job.manpower_required
            total_open += open_slots

            already_applied = False
            if self.request.user.is_authenticated:
                already_applied = job.applications.filter(
                    applicant=self.request.user.profile
                ).exists()

            job_data.append({
                "job": job,
                "accepted": accepted,
                "open_slots": open_slots,
                "already_applied": already_applied,
                "can_apply": self.request.user.is_authenticated and open_slots > 0 and not already_applied,
            })

        context["job_data"] = job_data
        context["total_manpower"] = total_manpower
        context["total_open_manpower"] = total_open

        if self.request.user.is_authenticated:
            context["is_owner"] = (
                commission.maker == self.request.user.profile
            )
        else:
            context["is_owner"] = False

        return context
    

class CommissionCreateView(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    model = Commission
    form_class = CommissionForm
    template_name = "commissions/commission_form.html"
    required_role = "Commission Maker"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["job_formset"] = JobFormSet(self.request.POST)
        else:
            context["job_formset"] = JobFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        job_formset = context["job_formset"]

        form.instance.maker = self.request.user.profile

        if job_formset.is_valid():
            self.object = form.save()
            job_formset.instance = self.object
            job_formset.save()
            return redirect(self.object.get_absolute_url())
        return self.form_invalid(form)
    

class CommissionUpdateView(LoginRequiredMixin, RoleRequiredMixin, UpdateView):
    model = Commission
    form_class = CommissionForm
    template_name = "commissions/commission_form.html"
    required_role = "Commission Maker"
    context_object_name = "commission"

    def get_queryset(self):
        return Commission.objects.filter(maker=self.request.user.profile)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["job_formset"] = JobFormSet(
                self.request.POST, instance=self.object
            )
        else:
            context["job_formset"] = JobFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        job_formset = context["job_formset"]

        if job_formset.is_valid():
            self.object = form.save()
            job_formset.instance = self.object
            job_formset.save()

            jobs = self.object.jobs.all()
            if jobs.exists() and all(job.status == "1" for job in jobs):
                self.object.status = "1"
                self.object.save()

            return redirect(self.object.get_absolute_url())
        return self.form_invalid(form)
    
@login_required
def apply_to_job(request, pk):
    job = Job.objects.get(pk=pk)
    applicant = request.user.profile

    accepted_count = job.applications.filter(status="1").count()

    if accepted_count >= job.manpower_required:
        return redirect(job.commission.get_absolute_url())

    if JobApplication.objects.filter(job=job, applicant=applicant).exists():
        return redirect(job.commission.get_absolute_url())

    JobApplication.objects.create(
        job=job,
        applicant=applicant,
        status="0",
    )

    return redirect(job.commission.get_absolute_url())
