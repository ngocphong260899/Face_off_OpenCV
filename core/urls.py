from django.urls import path
from .views import Home
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('', Home.as_view(), name='index'),
    path('rollup/', Home.table, name='tables'),
    path('login/', Home.login, name='login'),
    path('register/', Home.register, name='register'),
    path('add/', Home.addstudent, name='addstudent'),
    path('insert/', Home.insert_student, name='insertstudent'),
    path('bodytable/', Home.body_tables, name='bodytable'),
    path('editrollup/', Home.edit_roll_up, name='editrollup'),
    path('delete/', Home.deleteStudent, name='deletestudent'),
    path('manager/', Home.manager, name='manager'),
    path('managerclass/', Home.manager_class, name='managerclass'),
    path('report/', Home.report, name='report'),
    path('bodyreport/', Home.body_report, name='bodyreport'),
    path('video_feed/',Home.video_feed, name="video-feed"),
    path('managerdelete', Home.manager_delete, name='managerdelete'),
    path('manageredit', Home.manager_edit, name='namageredit'),
    path('logout', Home.logout, name='logout')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)