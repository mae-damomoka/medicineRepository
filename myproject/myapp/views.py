from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, View, TemplateView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.http import JsonResponse, HttpResponse, HttpRequest, HttpResponseNotFound, HttpResponseNotAllowed
from .models import Hospital, Medicine, Event, Department
from .forms import HospitalForm, SignUpForm, EventForm
from django.views.generic.list import ListView
from django.contrib.auth import authenticate, login
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required




# アプリの初期画面を表示するビュー
def start_screen(request):
    """アプリのスタート画面を表示"""
    return render(request, 'start_screen.html')




# ユーザー登録ビュー
def register(request):
    """ユーザー登録処理を行うビュー"""
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})




#ログイン
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not username or not password:
            return render(request, 'login.html', {'error': 'ユーザー名とパスワードを入力してください'})

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            print("Authentication successful for user: ", username)  # デバッグ出力
            return redirect('myapp:menu')  # 正しいリダイレクト先へ
        else:
            print("Authentication failed for user: ", username)  # デバッグ出力
            # 認証に失敗した場合、エラーメッセージを含めたコンテキストを返す
            return render(request, 'login.html', {'error': 'ユーザー名またはパスワードが正しくありません。'})
    else:
        # GETリクエストの場合、フォームのあるページを表示
        return render(request, 'login.html')
    
# 新しいログイン機能を追加する場合
def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            return render(request, 'login.html', {'error': 'ユーザー名とパスワードを入力してください'})

        if username == "正しいユーザー名" and password == "正しいパスワード":
            return HttpResponse("ログインに成功しました！")
        else:
            error_message = "ユーザー名かパスワードが間違っています"
            return render(request, 'login.html', {'error': error_message})




# サインアップビュー
class SignUpView(CreateView):
    """ユーザーのサインアップを処理するビュー"""
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'



# メニュー画面表示ビュー
def menu_view(request):
    return render(request, 'menu_template.html')
response = HttpResponse("Here's the text of the Web page.", content_type='text/html; charset=utf-8')




# カレンダー表示ビュー
def calendar_view(request):
    return render(request, 'calendar.html')

# イベントデータ取得ビュー
def get_events(request):
    """Eventモデルからイベントデータを取得し、JSONで返すビュー"""
    events = Event.objects.all()
    event_data = [{"title": event.title, "start": event.start_time.isoformat()} for event in events]
    return JsonResponse(event_data, safe=False)

# イベント一覧表示ビュー
def event_list(request):
    """イベント一覧を表示するビュー"""
    events = Event.objects.all().order_by('date', 'start_time')
    return render(request, 'event_list.html', {'events': events})

# イベント追加ビュー
def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('calendar')
    else:
        form = EventForm()
    return render(request, 'add_event.html', {'form': form})




# 病院一覧表示ビュー
def hospital_list(request):
    hospitals = Hospital.objects.all()
    response = render(request, 'hospital_list.html', {'hospitals': hospitals})
    response['Cache-Control'] = 'public, max-age=3600'
    return response

# 病院削除ビュー
@require_POST
def delete_hospital(request, hospital_id):  # hospital_id パラメータを追加
    print("delete_hospital was called")  # デバッグ出力
    # hospital_id = request.POST.get('hospital_id')  # URLパターンから渡されるので、この行は不要

    try:
        hospital = Hospital.objects.get(pk=hospital_id)  # Primary keyを使用してモデルインスタンスを取得
        hospital.delete()  # モデルインスタンスを削除
        return JsonResponse({'status': 'success', 'message': '病院が削除されました。'})  # 削除成功のレスポンス
    except Hospital.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': '病院が見つかりません。'}, status=404)  # エラーレスポンス

# お気に入り状態更新ビュー
@require_POST
def delete_favorite(request):
    hospital_id = request.POST.get('hospital_id')
    try:
        hospital = Hospital.objects.get(id=hospital_id)
        hospital.is_favorite = False
        hospital.save()
        return JsonResponse({'success': True})
    except Hospital.DoesNotExist:
        return JsonResponse({'error': 'Invalid request'}, status=400)

# 病院追加ビュー
@require_POST
def add_hospital(request):
    hospital_name = request.POST.get('hospital_name')
    department_name = request.POST.get('department_name')

    department, created = Department.objects.get_or_create(name=department_name)
    Hospital.objects.create(name=hospital_name, department=department)
    
    return redirect('myapp:hospital_list')

@require_POST
def toggle_favorite(request, hospital_id):
    hospital = get_object_or_404(Hospital, pk=hospital_id)
    hospital.is_favorite = not hospital.is_favorite  # 状態をトグル
    hospital.save()
    return JsonResponse({'success': True, 'is_favorite': hospital.is_favorite})
    
class AddHospitalView(CreateView):
    model = Hospital
    fields = ['name', 'department',]  # 必要なフィールドを追加
    template_name = 'hospital_form.html'  # 使用するテンプレートの名前
    success_url = '/hospital-list/'  # フォーム送信後のリダイレクト先
    



# 薬一覧表示ビュー
def medicines_view(request):
    """薬の一覧を表示するビュー"""
    medicines = Medicine.objects.all()
    return render(request, 'medicines_template.html', {'medicines': medicines})

def medicine_list(request):
    if request.method == 'POST':
        name = request.POST.get('medicine_name')
        effect = request.POST.get('medicine_effect')
        hospital = request.POST.get('prescribed_hospital')
        Medicine.objects.create(name=name, effect=effect, hospital=hospital)

    medicines = Medicine.objects.all()
    return render(request, 'medicines_template.html', {'medicines': medicines})

def delete_medicine(request, medicine_id):
    medicine = get_object_or_404(Medicine, pk=medicine_id)
    medicine.delete()
    return redirect('myapp:medicine_list')

def add_medicine(request):
    if request.method == 'POST':
        # ここで必要な処理（例えばフォームのバリデーションや薬の保存）を行う
        # ...
        return redirect('myapp:medicine_list')
    return render(request, 'add_medicine.html')  # フォームを含んだテンプレートを返す




# ログアウトビュー
@login_required
@require_POST 
def logout_view(request):
    logout(request)
    response = redirect('myapp:start_screen')  # スタート画面にリダイレクト
    response.delete_cookie('sessionid')  # Djangoのデフォルトセッションクッキー名を削除
    return response  

# ログアウト確認ビュー
def logout_confirm_view(request):
    return render(request, 'logout.html')



# テスト用ビュー
def some_view(request):
    return HttpResponse('Response content')




# バックビュー
def back_view(request):
    """テスト用または一時的なページを表示するビュー"""
    return HttpResponse("This is the back view.")




# テンプレートビュー
class MyTemplateView(TemplateView):
    """テンプレートを使用してページを表示するクラスベースのビュー"""
    template_name = 'my_template.html'

class SomeClassBasedView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('This is a class based view response')

class EventListView(ListView):
    model = Event  # Event モデルを指定
    template_name = 'calendar.html'  # 適切なテンプレートのパスを指定
    context_object_name = 'events'  # テンプレートで使用するコンテキスト変数の名前




def my_view(request):
    response = HttpResponse("ここにレスポンスの内容が入ります", content_type='text/html; charset=utf-8')
    return response

class MyLoginView(View):
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
def your_view_name(request):
    return redirect('add_hospital') 