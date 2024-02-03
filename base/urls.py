from django.contrib import admin
from django.urls import path,include

admin.site.site_title = "GBPUAT Attendance site admin (DEV)"
admin.site.site_header = "GBPUAT Attendance administration"
admin.site.index_title = "Api administration"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',include('api.urls')),
    path('auth/',include('account.urls'))
]
