from django.contrib import admin
from clothesLookApp.models import User,Look,Comment,Category,Clothing

from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserCreateFormAdmin, UserChangeForm

from django.contrib.auth import get_user_model 

User=get_user_model()

# Register your models here.
#admin.site.register(User)
admin.site.register(Look)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Clothing)


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreateFormAdmin

    SEX_OPTIONS = (
        ('M', 'Man'),
        ('W', 'Woman'),
    )
    list_display = ('nickName', 'first_name','last_name', 'sex', 'is_staff')
    list_filter = ('is_staff',)
    fieldsets = (
        (None, {'fields': ('nickName', 'password')}),
        ('Personal info', {'fields': ('year_birth','sex', 'first_name','last_name',),}),
        ('Permissions', {'fields': ('is_staff',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('nickName', 'year_birth','sex', 'first_name','last_name', 'password1', 'password2')}
        ),
    )
    search_fields = ('nickName',)
    ordering = ('nickName',)


admin.site.unregister(Group)
admin.site.register(User, UserAdmin)


