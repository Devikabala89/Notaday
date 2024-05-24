
from django.urls import path
from notaday_app import views
from notaday import settings
from django.conf.urls.static import static 
 

urlpatterns = [
    path('intro/',views.intro),
    path('about/',views.about),
    path('contactUs/',views.contact),
    path('login/',views.user_login),
    path('register/',views.register),
    path('features/',views.features),
    path('index',views.index),
    path('shop',views.shop),
    path('details_product/<pid>',views.details_product),
    path('cart',views.Cart),
    path('calorie',views.calorie),
    path('logout/',views.ulogout),
    path('addtocart/<sid>',views.addtocart),
    path('remove/<rid>',views.removefromcart),
    path('removeorder/<rid>',views.removefromorder),
    path('updateqty/<wid>/<cid>',views.updateqty),
    path('placeorder/',views.placeorder),
    path('addtask/',views.addtask),
    path('taskcomplete/<tid>',views.taskcomplete),
    path('deletetask/<tid>',views.deletetask),
    path('notes/',views.notes),
    path('addnotes/',views.addnotes),
    path('viewnotes/<nid>',views.viewnotes),
    path('updatenotes/<nid>',views.updatenotes),
    path('deletenote/<tid>',views.deletenote),
    path('makepayment',views.makepayment),
    path('loadfood/<pid>',views.loadfood),
    path('sendusermail',views.sendusermail),
    path('orderhistory',views.orderhistory),
    path('wentwrong/',views.wentwrong)

    #path('catfilter/<cv>',views.catfilter)

]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
