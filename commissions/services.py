from django.db import transaction

from .models import Commission, Job, JobApplication


class CommissionService:
    @staticmethod
    @transaction.atomic
    def create_commission(author, data, jobs_data):
        commission = Commission.objects.create(
            type=data["type"],
            maker=author,
            title=data["title"],
            description=data["description"],
            people_required=data["people_required"],
            status=data["status"],
        )

        for job_data in jobs_data:
            if not job_data:
                continue

            role = job_data.get("role")
            manpower_required = job_data.get("manpower_required")
            status = job_data.get("status")

            if role and manpower_required:
                Job.objects.create(
                    commission=commission,
                    role=role,
                    manpower_required=manpower_required,
                    status=status,
                )

        return commission

    @staticmethod
    def apply_to_job(applicant, job):
        accepted_count = job.applications.filter(status="1").count()

        if JobApplication.objects.filter(job=job, applicant=applicant).exists():
            return None

        if accepted_count >= job.manpower_required:
            return None

        return JobApplication.objects.create(
            job=job,
            applicant=applicant,
            status="0",
        )

    @staticmethod
    def sync_commission_status(commission):
        jobs = commission.jobs.all()

        if jobs.exists() and all(job.status == "1" for job in jobs):
            commission.status = "1"
        else:
            commission.status = "0"
        
        commission.save()
        return commission

    @staticmethod
    def get_commission_summary(commission):
        total_manpower = 0
        open_manpower = 0

        for job in commission.jobs.all():
            accepted_count = job.applications.filter(status="1").count()
            total_manpower += job.manpower_required
            open_slots = max(job.manpower_required - accepted_count, 0)
            open_manpower += open_slots

        return {
            "total_manpower": total_manpower,
            "open_manpower": open_manpower,
        }
    
    @staticmethod
    def accept_job_application(application):
        job = application.job

        accepted_count = job.applications.filter(status="1").count()

        if application.status == "1":
            return application

        if accepted_count >= job.manpower_required:
            return None

        application.status = "1"
        application.save()

        if job.applications.filter(status="1").count() >= job.manpower_required:
            job.status = "1"
            job.save()

        CommissionService.sync_commission_status(job.commission)
        return application

    @staticmethod
    def reject_job_application(application):
        application.status = "2"
        application.save()

        job = application.job

        if job.applications.filter(status="1").count() < job.manpower_required:
            job.status = "0"
            job.save()

        CommissionService.sync_commission_status(job.commission)
        return application