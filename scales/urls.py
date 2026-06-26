from django.urls import path
from . import views
urlpatterns = [
    path('main/',views.show,name='show'),
    path('phq9/',views.phq9,name='phq9'),
    path('gad7/',views.gad7,name='gad7'),
    path("sign_up",views.sign_up,name="sign_up"),
    path("music",views.music_therapy,name="music"),
    path("docs/",views.doc_dash,name="docs")
]
