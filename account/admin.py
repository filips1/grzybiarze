from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import Moje_Konto
# Register your models here.


class Moje_Konto_Panel_Admina(UserAdmin):          # co ma być wyświetlone w panelu admina
    list_display = ( 'username', 'email', 'date_joined', 'last_login', 'is_admin')
    search_fields = ('email', 'username')
    readonly_fields = ('date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Moje_Konto, Moje_Konto_Panel_Admina)