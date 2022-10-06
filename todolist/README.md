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

# Tugas 5
### Apa perbedaan dari Inline, Internal, dan External CSS? Apa saja kelebihan dan kekurangan dari masing-masing style?
- **Inline**
    CSS diletakkan sebaris atau lebih tepatnya didalam suatu elemen HTML.
    contoh:
    ```html
    <p style="text-color: red">
        Ini inline
    </p>
    ```
    Pros: Cepat dan praktis
    Cons: Tidak dapat styling banyak elemen sekaligus
- **Internal**
    CSS diletakkan pada elemen `<style>` pada file HTML.
    contoh:
    ```html
    <!DOCTYPE html>
    <html>
    <head>
    <style>
    body {
      background-color: linen;
    }

    h1 {
      color: maroon;
      margin-left: 40px;
    }
    </style>
    </head>
    <body>

    <h1>This is a heading</h1>
    <p>This is a paragraph.</p>

    </body>
    </html>
    ```
    Pros: Cukup optimal untuk file HTML berukuran kecil-sedang.
    Cons: File HTML agak kurang sedap dipandang karena linenya akan membengkak. Susah untuk styling karena harus scroll untuk bisa styling.
- **External**
    CSS diletakkan di file berbeda dengan format `.css`. Pada contoh dibawah styling diterapkan pada file `mystyle.css`.
    ```html
    <!DOCTYPE html>
    <html>
    <head>
    <link rel="stylesheet" href="mystyle.css">
    </head>
    <body>

    <h1>This is a heading</h1>
    <p>This is a paragraph.</p>

    </body>
    </html>
    ```
    
    Pros: Rapi, dalam artian tidak memperbanyak line pada file HTML. Selain itu style akan lebih mudah dipakai lagi (reusable). Juga bisa memisah css dalam beberapa file (misal per fungsionalitas) sehingga lebih rapi.
    Cons: Agak cukup susah tracing jika terdapat bug karena styling terletak pada  file yang berbeda. Untuk kode HTML yang kecil agak tidak optimal. Memperlambat loading time.
     
## Jelaskan tag HTML5 yang kamu ketahui.
- `<p>` untuk membuat paragraf.
- `<h1>` untuk membuat heading 1.
- `<h2>` untuk membuat heading 2.
- `<h3>` untuk membuat heading 3.
- `<h4>` untuk membuat heading 4.
- `<h5>` untuk membuat heading 5.
- `<h6>` untuk membuat heading 6.
- `<style>` untuk menaruh internal css.
- `<form>` untuk mendeklarasi awal mula form, disertakan juga method requestnya.
- `<div>` tag yang digunakan untuk separasi antar elemen. Sangat berguna untuk styling.

##  Jelaskan tipe-tipe CSS selector yang kamu ketahui.
- Element selector
    Mereference suatu elemen HTML untuk styling elemen tersebut.
    contoh:
    ```css
    h1: {
        font-weight: normal;
    }
    ```
- Class selector
    Mereference nama class untuk distyling. Gunakan format `.NAMA_CLASS` untuk mereference.
    contoh:
    ```css
    .NAMA_CLASS {
        css-property: value;
    }
    ```
- Id selector
    Mereference nama id untuk distyling. Gunakan format `#NAMA_ID`.
    contoh:
    ```css
    #NAMA_ID {
        css-property: value;   
    }
    ```

Selain selector diatas, dapat diintegrasikan combinators agar dapat lebih meng-specify reference elemen yang ingin distyling. Format dari combinator sendiri adalah `x {combinator} y`. Adapun contoh combinators adalah:
- Descendant selector (space)
    Specify semua elemen y yang didalam x (termasuk grandchild, grand-grandchild, and so on). Contoh: 
    ```css
    div p {
        
    }
    ```
- Child selector (>)
    Specify hanya y yang tepat menjadi child dari x. Contoh:
    ```css
    div > p {
        
    }
    ```
- Adjacent sibling selector (+)
    Specify sebuah y yang berupa sibling dari x dan berada tepat setelah (dibawah) x. Contoh:
    ```css
    div + p {
        
    }
    
    akan meselect p dengan layout:
    <div></div>
    <p></p>
    
    dan tidak akan meselect p dengan layout:
    <div></div>
    <h1></h1>
    <p></p>
    ```
- General sibling selector (~)
    Specify semua y yang berupa sibling setelah x. Contoh:
    ```css
    div ~ p {
    }
    ```

## Implementasi
- Menggunakan framework Tailwind CSS, dan daisyUI dengan menambahkan 
```css
<link href="https://cdn.jsdelivr.net/npm/daisyui@2.31.0/dist/full.css" rel="stylesheet" type="text/css" />
<script src="https://cdn.tailwindcss.com"></script>
``` 
pada elemen `<head>` di `base.html`
- Membaca dokumentasi komponen daisyUI dan menerapkannya ke HTML saya. Adapun dokumentasinya dapat diakses pada laman berikut : https://daisyui.com/components/
- Membaca cheatsheet Tailwind CSS dan menerapkannya pada HTML saya. Adapun cheatsheetnya dapat diakses pada laman berikut: https://nerdcave.com/tailwind-cheat-sheet
- Dengan tekat yang kuat akhirnya seluruh tugas 4 (dan bahkan tugas 2 dan 3 juga) dapat distyling.