# Tugas PBP
### [Klik disini untuk mengakses :)](https://tugas-2-pbp-neozap.herokuapp.com/)
### NB: Untuk link langsung menuju masing-masing tugas, dapat dilihat di folder aplikasi tugas terkait ya :)
<br><br>
# Tugas 2
## Bagan
![Bagan](https://i.imgur.com/aPFLz41.png)
###### Referensi: https://pbp-fasilkom-ui.github.io/ganjil-2023/assignments/tutorial/tutorial-1/

1. User / Client memasukkan url.
2. URL yang diberikan Client kita proses pada `urls.py`, dan nanti kita masukkan ke views sesuai dengan yang diminta user.
3. Pada app katalog, views (`views.py`) menquery data katalog pada `../db.sqlite3` yang sudah sesuai dengan model yang telah kita definisikan pada `models.py`. Isi dari `../db.sqlite3` tersebut adalah data yang kita berikan pada `fixtures/initial_catalog_data.json`.
4. Selanjutnya, views selayaknya API, akan merender template (`templates/katalog.html`) sesuai request user dengan data yang sudah kita query tadi dengan tambahan Nama dan NPM sebagai context agar bisa ditampilkan pada `templates/katalog.html`.

## Jelaskan kenapa menggunakan virtual environment? 
Dengan virtual environment, kita dapat memaintain aplikasi kita dengan lebih mudah. Dikarenakan virtual environment benar-benar membuat environment baru sehingga module module kita terdahulu tidak akan masuk pada aplikasi kita. Hal tersebut sangatlah membantu karena module module kita terdahulu bisa saja memiliki ukuran besar dan belum tentu berguna bagi aplikasi kita. Selain itu aplikasi kita dapat ditest oleh user atau diakses dari device lain dengan lebih mudah, dikarenakan adanya file `requirements.txt` yang berisi module module beserta versinya yang diperlukan untuk aplikasi kita.

## Apakah kita tetap dapat membuat aplikasi web berbasis Django tanpa menggunakan virtual environment?
Bisa, tetapi akan sangat rentan terhadap error. Misal jika kita memiliki suatu module yang tidak dapat diinstall oleh pihak deployer, maka deploy kita tidak berhasil. Selain itu, ukuran aplikasi web kita akan sangat besar, atau pastinya akan semakin besar lama kelamaan. Hal tersebut dikarenakan kebutuhan kita untuk menginstall module baru, dan jika kita tidak menggunakan virtual environment pasti aplikasi web kita akan ikut menginstall module tersebut yang mengakibatkan pada penumpukan ukuran / size aplikasi pada hal yang tidak mesti diperlukan.

## Jelaskan bagaimana cara kamu mengimplementasikan poin 1 sampai dengan 4 di atas.
Sebelum mengimplementasikan poin 1 hingga 4, mari kita buat virtual environment baru dengan perintah `python -m venv env`. Selanjutnya akan kita aktifkan venv tersebut dengan menggunakan perintah `env/Scripts/activate`. Jangan lupa juga install dependency yang diperlukan dengan `pip install -r requirements.txt`.
1. Jalankan `python manage.py makemigrations` pada command prompt untuk membuat folder `katalog/migrations` yang berisi class `Migration` yang berfungsi untuk memigrasi skema model data kepada database yang dapat dijalankan dengan perintah `python manage.py migrate`. Selanjutnya lakukan `python manage.py loaddata initial_catalog_data.json` untuk memasukkan data json pada `initial_catalog_data.json` ke database kita. Pada `katalog/views.py` terdapat fungsi `show_katalog` yang mengambil data dari database yang sudah kita setup tadi dengan `CatalogItem.objects.all()` lalu dirender pada file `katalog/templates/katalog.html` sebagai context sehingga dapat diakses pada file html tersebut.
2. Pada `katalog/urls.py` tambahkan sebuah path pada `urlpatterns` path yang memanggil fungsi `show_katalog`
3. Context yang dirender pada tahap 1 dapat kita akses menggunakan syntax django `{}`. Contohnya, untuk mengakses variabel name kita gunakan syntax `{{name}}` lalu untuk melakukan for pada list `item_catalog` gunakan syntax `{% for item in item_catalog %}`. Syntax lainnya dapat dilihat pada dokumentasi Django.
4. Lakukan deploy pada heroku dengan membuat app dulu pada heroku serta mengimport API_KEY dan APP_NAME pada repository secrets, lalu pada setiap push file `deploy.yml` akan secara otomatis mendeploy aplikasi kita.

# Tugas 3
##  Jelaskan perbedaan antara JSON, XML, dan HTML!
**1. HTML**
HTML merupakan singkatan dari HyperText Markup Language. HTML tidak dapat digunakan untuk Data Delivery, melainkan HTML mendefinisikan struktur dari suatu website.<br>
**2. XML**
XML merupakan singkatan dari Extensible Markup Language. Syntax nya sangat mirip dengan HTML, tetapi kegunaannya sangat berbeda karena XML ini digunakan sebagai Data Delivery. XML biasanya digunakan untuk mendeskripsikan data secara lebih detail dibandingkan dengan JSON, tetapi memang lebih susah dibaca karena syntaxnya seperti HTML.<br>
**3. JSON**
JSON merupakan singkatan dari JavaScript Object Notation. JSON sangat umum digunakan sebagai Data Delivery. Syntaxnya yang simpel (key dan value) membuatnya menjadi bahasa yang umum untuk pengiriman data (sepengetahuan saya). Selain itu data pada JSON lebih mudah diolah dibanding XML.<br>

##  Jelaskan mengapa kita memerlukan data delivery dalam pengimplementasian sebuah platform?
Aplikasi pada umumnya terdiri dari 2 bagian, frontend dan backend. Jika aplikasi kita membutuhkan banyak data, maka data tersebut tidak mungkin kita simpan pada frontend (client-side), selain semakin susah diatur, user juga harus mengunduh data tersebut setiap kali membuka aplikasi kita, yang tentunya akan berdampak sangat buruk bagi user. Maka dari itu, backend (server-side) diperlukan agar frontend merequest data secukupnya kepada backend, dan backend merespon dengan melakukan data delivery kepada frontend untuk diolah dan digunakan.

##  Jelaskan bagaimana cara kamu mengimplementasikan checklist di atas.
1. Buat aplikasi `mywatchlist` baru dengan `python manage.py startapp mywatchlist`.
2. Tambahkan path menuju aplikasi tersebut dengan menambahkan `path('mywatchlist/', include('mywatchlist.urls'))` pada `project_django/urls.py` agar bisa diakses di `http://localhost:8000/mywatchlist`.
3. Buat model baru di `mywatchlist/models.py` sebagai berikut:
```python
class MyWatchList(models.Model):
    watched = models.BooleanField()
    title = models.CharField(max_length=255)
    rating = models.FloatField()
    release_date = models.TextField()
    review = models.TextField()
```
4. Menambahkan 10 data movies pada aplikasi sesuai yang ada di `mywatchlist/fixtures/initial_watchlist_data.json`
5. Data movies tersebut akan kita keluarkan dalam 3 format, yakni HTML, XML, dan JSON sesuai request dari user. Maka buat 3 fungsi di `mywatchlist/views.py` yang setiap fungsi akan menampilkan data sesuai format yang direquest user. Pada format HTML, user juga akan diberi detail apabila sudah menonton banyak film atau belum pada watchlistnya. <br></br>Berikut ketiga fungsinya:
```python
def show_mywatchlist(request):
    mywatchlist = MyWatchList.objects.all()
    watched = 0
    for movie in mywatchlist:
        watched += movie.watched
    not_watched = len(mywatchlist) - watched
    if watched >= not_watched:
        msg = "Selamat, kamu sudah banyak menonton!"
    else:
        msg = "Wah, kamu masih sedikit menonton!"

    context = {
        "mywatchlist": mywatchlist,
        "msg": msg,
    }
    
    return render(request, "mywatchlist.html", context)

def show_mywatchlist_json(request):
    mywatchlist = MyWatchList.objects.all()
    return HttpResponse(serializers.serialize("json", mywatchlist), content_type="application/json")

def show_mywatchlist_xml(request):
    mywatchlist = MyWatchList.objects.all()
    return HttpResponse(serializers.serialize("xml", mywatchlist), content_type="application/xml")
```
6. Pada `mywatchlist/urls.py`, kita buat routing agar user dapat mengakses ketiga format tersebut sesuai potongan kode dibawah ini. Contoh penggunaannya adalah sebagai berikut: 
- `http://localhost:8000/mywatchlist/html` untuk mengakses format HTML
- `http://localhost:8000/mywatchlist/xml` untuk mengakses format XML
- `http://localhost:8000/mywatchlist/json` untuk mengakses format JSON
<br>Berikut routingnya:
```python
urlpatterns = [
    path('html/', show_mywatchlist, name='show_mywatchlist'),
    path('json/', show_mywatchlist_json, name='show_mywatchlist_json'),
    path('xml/', show_mywatchlist_xml, name='show_mywatchlist_xml'),
]
```
7. Deploy ke heroku, jangan lupa load data watchlist kita juga ke aplikasi heroku dengan menambahkan `python manage.py loaddata initial_watchlist_data.json` pada `./Procfile` kita. Lalu tambahkan secret data berupa `APP_NAME` dan `API_KEY` agar dapat dideploy secara otomatis setiap kita melakukan push oleh file `.github/workflows/dpl.yml`.
8. Buat unit test pada `mywatchlist/tests.py` untuk melakukan testing pada semua endpoint yang ada pada aplikasi mywatchlist kita. Sebelum melakukan testing, jalankan perintah `python manage.py collectstatic` agar tidak mengalami error `ValueError: Missing staticfiles manifest entry for 'css/style.css'`. Setelah itu lakukan testing dengan perintah `python manage.py test`. Testing berhasil apabila semua endpoint berhasil me-return status code 200.<br></br>Berikut unit test yang saya gunakan:
```python
class MyWatchListTests(TestCase):
    def test_html_endpoint(self):
        resp = self.client.get("/mywatchlist/html/")
        self.assertEqual(resp.status_code, 200)

    def test_json_endpoint(self):
        resp = self.client.get("/mywatchlist/json/")
        self.assertEqual(resp.status_code, 200)

    def test_xml_endpoint(self):
        resp = self.client.get("/mywatchlist/xml/")
        self.assertEqual(resp.status_code, 200)
```
9. Mengecek apakah hasil deploy dapat diakses dengan lancar (me-return status 200 OK) dengan Postman.

- Endpoint HTML:
![](https://i.imgur.com/MbROutm.png)
- Endpoint XML:
![](https://i.imgur.com/zRXR1ok.png)
- Endpoint JSON:
![](https://i.imgur.com/SmkEz9E.png)

# Tugas 4
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
