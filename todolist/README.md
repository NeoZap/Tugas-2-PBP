# Tugas 4
### [Klik disini untuk mengakses :)](https://tugas-2-pbp-neozap.herokuapp.com/todolist)
## Apa kegunaan `{% csrf_token %}` pada elemen <form>? Apa yang terjadi apabila tidak ada potongan kode tersebut pada elemen <form>?
Berguna untuk menggenerate CSRF (Cross Site Request Forgery) token yang **unik** pada website kita. Jika sebuah client melakukan request kepada webserver kita tanpa mencantumkan token tersebut, maka request tersebut dianggap invalid dan tidak diproses. Dengan kata lain, token ini berfungsi sebagai validator bahwa suatu request benar-benar berasal dari client yang mengakses aplikasi kita. Hal ini tentunya sangat berguna sebagai proteksi untuk mencegah berbagai serangan siber dari oknum jahat maupun yang tidak disengaja.

## Apakah kita dapat membuat elemen <form> secara manual? Jelaskan secara gambaran besar bagaimana cara membuat <form> secara manual.
Sangat bisa, karena pada dasarnya generator form django (`{{form.as_table}}`) ada dengan tujuan untuk mempermudah kita agar tidak harus membuat `<form>` secara manual.
    
Untuk membuatnya secara manual, bisa dengan menambahkan elemen `<form>`, diikuti dengan `<label>` yang berguna sebagai identifier inputan dan `<input>` sebagai tempat user memberi input. Jangan lupa diakhiri dengan `<submit>` agar data yang telah diinput user dapat terkirim.

##  Jelaskan proses alur data dari submisi yang dilakukan oleh pengguna melalui HTML form, penyimpanan data pada database, hingga munculnya data yang telah disimpan pada template HTML.
Form inputan akan dibuat oleh django dengan label yang sesuai dengan model `TaskForm`. Setelah user memencet tombol submit pada form tersebut, input dari user akan dimasukkan kepada atribut model Task dengan potongan kode dibawah ini:
```python
task = Task.objects.create(user=request.user, title=form.cleaned_data['title'], description=form.cleaned_data['description'])
```
Lalu dengan menerapkan method `save()` pada task, data pada task akan disimpan pada database.

Karena data sudah disimpan pada database, maka data tersebut akan dimunculkan pada template HTML.

## Implementasi
- Buat app `todolist`
- Tambahkan ke INSTALLED_APPS dan urlpattern di `project_django`
- Membuat model Task pada aplikasi todolist sebagai berikut:
```python
class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    date = models.DateTimeField(default=datetime.now)
    description = models.TextField()
    is_finished = models.BooleanField(default=False)
```
- Menggunakan `UserCreationForm` untuk register dan fungsi `authenticate` untuk login serta `logout` untuk logout untuk menerapkan register, login, dan logout.
```python
def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Akun telah berhasil dibuat!')
            return redirect('todolist:login')
    
    context = {'form':form}
    return render(request, 'register.html', context)

def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            response = HttpResponseRedirect(reverse("todolist:show_todolist")) # membuat response
            return response
        else:
            messages.info(request, 'Username atau Password salah!')
    context = {}
    return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('todolist:login'))
    return response
```
- Membuat fungsi pada `todolist/views.py` untuk menampilkan todolist dan pembuatan task.
```python
@login_required(login_url='/todolist/login/')
def show_todolist(request):
    user = request.user
    context = {
        "todo_list": Task.objects.filter(user=user),
        "name": user.username,
    }
    return render(request, 'todolist.html', context=context)

@login_required(login_url='/todolist/login/')
def create_task(request):
    form = TaskForm();
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = Task.objects.create(user=request.user, title=form.cleaned_data['title'], description=form.cleaned_data['description'])
            task.save()
            return redirect('todolist:show_todolist')
    return render(request, "create_task.html", {"form" : form})
```
Jangan lupa untuk menambahkan decorator `@login_required` yang menandakan bahwa user harus login terlebih dahulu sebelum dapat mengakses fungsionalitas terkait.
- Tambahkan routing pada `todolist/urls.py`
```python
urlpatterns = [
    path('', show_todolist, name='show_todolist'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('create-task/', create_task, name='create_task'),
    path('change-task/<int:task_id>', change_task, name='change_task'),
    path('delete-task/<int:task_id>', delete_task, name='delete_task'),
]
```
- Push ke github dan akan dideploy ke heroku secara otomatis oleh `dpl.yml`
