from django.contrib import admin
from clothesLookApp.models import User,Look,Comment,Category,Clothing

from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .forms import UserCreateFormAdmin, UserCreationForm, UserChangeForm

from django.contrib.auth import get_user_model 

User=get_user_model()

# Register your models here.
#admin.site.register(User)
admin.site.register(Look)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Clothing)


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreateFormAdmin
    # form = UserCreateForm

    # The fields to be used in displaying the DecideUser model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.DecideDecideDecideDecide.
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
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('nickName', 'year_birth','sex', 'first_name','last_name', 'password1', 'password2')}
        ),
    )
    search_fields = ('nickName',)
    ordering = ('nickName',)
    filter_horizontal = ()

# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)

