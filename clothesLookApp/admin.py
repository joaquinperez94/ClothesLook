from django.contrib import admin

from clothesLookApp.models import User,Look,Comment,Category,Clothing

# Register your models here.
#admin.site.register(User)
admin.site.register(Look)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Clothing)

