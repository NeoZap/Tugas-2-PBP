# My WatchList (Tugas 3)
### [Klik disini untuk mengakses :)](https://tugas-2-pbp-neozap.herokuapp.com/mywatchlist/)
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