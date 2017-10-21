from django.contrib import admin

# Register your models here.
from admindb.models import Users, Domains, Aliases, Forwards, Masters

class UsersAdmin(admin.ModelAdmin):
    list_display = ('localpart', 'domain', 'enabled', 'remote_access')
    search_fields = ('localpart',)
    list_filter = ('domain','enabled','remote_access',)
class AliasesAdmin(admin.ModelAdmin):
    list_display = ('localpart', 'domain', 'recipients',)
    search_fields = ('localpart','recipients',)
    list_filter = ('domain',)
class ForwardsAdmin(admin.ModelAdmin):
    list_display = ('localpart', 'domain', 'recipient_localpart', 'recipient_domain', 'priority',)
    search_fields = ('localpart', 'domain', 'recipient_localpart', 'recipient_domain',)
    list_filter = ('domain','recipient_domain','priority',)
class DomainsAdmin(admin.ModelAdmin):
    list_display = ('domain', 'type',)
    search_fields = ('domain',)
    list_filter = ('type',)
class MastersAdmin(admin.ModelAdmin):
    list_display = ('user', 'enabled',)
    search_fields = ('user',)
    list_filter = ('enabled',)

admin.site.register(Users,UsersAdmin)
admin.site.register(Domains,DomainsAdmin)
admin.site.register(Aliases,AliasesAdmin)
admin.site.register(Forwards,ForwardsAdmin)
admin.site.register(Masters,MastersAdmin)
