from django.contrib import admin
from skillucketApp.models.profile import Profile
from skillucketApp.models.skill import Skill
from skillucketApp.models.user_skill import UserSkill
from skillucketApp.models.bucket_skill import BucketSkill
from skillucketApp.models.category import Category


# Register your models here.
admin.site.register(Profile)
admin.site.register(Skill)
admin.site.register(UserSkill)
admin.site.register(BucketSkill)
admin.site.register(Category)
