from django.contrib import admin
from .models import Project, ProjectCategory, Favorite, ProjectReview, ProjectRating


class ProjectInline(admin.StackedInline):
    model = Project


class ProjectCategoryAdmin(admin.ModelAdmin):
    model = ProjectCategory
    inlines = [
        ProjectInline,
    ]
    ordering = ["name"]


class FavoriteAdmin(admin.ModelAdmin):
    model = Favorite


class ProjectReviewAdmin(admin.ModelAdmin):
    model = ProjectReview


class ProjectRatingAdmin(admin.ModelAdmin):
    model = ProjectRating


class ProjectAdmin(admin.ModelAdmin):
    model = Project
    ordering = ["-created_on"]
    search_fields = ("title", "description")
    list_display = ("title", "category", "description", "created_on", "updated_on")


admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectCategory, ProjectCategoryAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(ProjectRating, ProjectRatingAdmin)
admin.site.register(ProjectReview, ProjectReviewAdmin)
