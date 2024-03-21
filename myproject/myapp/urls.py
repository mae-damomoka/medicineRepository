from django.urls import include, path
from . import views
from django.conf import settings
from .views import calendar_view
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from .views import MyLoginView
from django.conf.urls.static import static
from .views import toggle_favorite
from .views import add_hospital
from .views import delete_hospital, delete_favorite
from django.conf.urls.static import static
from .views import your_view_name
from django.contrib.auth import views as auth_views
from .views import login_view, custom_login

# アプリケーションの名前空間を定義しています。これにより、テンプレートで 'myapp:view_name' のように名前空間を使用できます。
app_name = 'myapp'

urlpatterns = [
    # ルートURL（スタート画面）へのマッピング。ビュー関数とURLの名前を指定
    path('', views.start_screen, name='start_screen'),



    # ユーザー登録画面へのマッピング
    path('register/', views.register, name='register'),

    # ユーザーサインアップ画面（クラスベースビューを使用）へのマッピング
    path('signup/', views.SignUpView.as_view(), name='signup'),



    # メインメニュー画面へのマッピング
    path('menu-url/', views.menu_view, name='menu'),



    # カレンダー機能へのマッピング
    path('calendar/', views.calendar_view, name='calendar'),



    # 病院追加機能へのマッピング
    path('add_hospital/', views.add_hospital, name='add_hospital'),
    
    # 病院削除機能へのマッピング（病院IDをパラメータとして受け取る）
    path('delete_hospital/<int:hospital_id>/', views.delete_hospital, name='delete_hospital'),
    
    # お気に入り機能の切り替え機能へのマッピング（病院IDをパラメータとして受け取る）
    path('toggle_favorite/<int:hospital_id>/', views.toggle_favorite, name='toggle_favorite'),
    
    # 病院一覧画面へのマッピング
    path('hospital_list/', views.hospital_list, name='hospital_list'),



    # 薬の一覧表示機能へのマッピング
    path('medicine-list/', views.medicine_list, name='medicine_list'),

    # 薬削除機能へのマッピング（薬IDをパラメータとして受け取る）
    path('medicine/delete/<int:medicine_id>/', views.delete_medicine, name='delete_medicine'),
    
    # 薬追加機能へのマッピング
    path('medicine-submit/', views.add_medicine, name='add_medicine'),



    # イベントデータをJSON形式で取得するAPIへのマッピング
    path('api/get_events/', views.get_events, name='get_events'),

    # イベント一覧表示機能へのマッピング（クラスベースビューを使用）
    path('events/', views.EventListView.as_view(), name='event_list'),



    # ログインページへのマッピング
    path('login/', views.login_view, name='login'),
    
    # Djangoの管理画面へのマッピング
    path('admin/', admin.site.urls),
    
    # ログインページへのマッピング（クラスベースビューを使用）
    path('accounts/login/', views.MyLoginView.as_view(), name='login_view'),
        
        

    # ログアウトページへのマッピング
    path('logout/', views.logout_view, name='logout'),
    
    # ログアウト確認画面へのマッピング
    path('logout-confirm/', views.logout_confirm_view, name='logout_confirm'),
    


    # スタート画面への追加のマッピング
    path('start_screen/', views.start_screen, name='start_screen'),
    
    path('custom-login/', custom_login, name='custom_login'), 
]

# DEBUGモードが有効な場合の追加設定。デバッグツールバーのURLと静的ファイルのサービング設定を含む
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)