# Katalog Saya
[Klik disini untuk mengakses :)](https://tugas-2-pbp-neozap.herokuapp.com/katalog/)

## Bagan
![](https://i.imgur.com/nQzzjRO.png)
###### Referensi: https://pbp-fasilkom-ui.github.io/ganjil-2023/assignments/tutorial/tutorial-1/

1. User / Client memasukkan url.
2. URL yang diberikan Client kita proses pada `urls.py`, dan nanti kita masukkan ke views sesuai dengan yang diminta user.
3. Pada app katalog, views (`views.py`) menquery data katalog pada `fixtures/initial_catalog_data.json` sesuai dengan model yang sudah didefinisikan di `models.py`, dengan menambah data tambahan berupa NPM dan Nama. 
4. Selanjutnya, views akan merender template (`katalog.html`) sesuai request user dengan data katalog tersebut (sebagai context) agar bisa ditampilkan pada `katalog.html`

## Jelaskan kenapa menggunakan virtual environment? 
Dengan virtual environment, kita dapat memaintain aplikasi kita dengan lebih mudah. Dikarenakan virtual environment benar-benar membuat environment baru sehingga module module kita terdahulu tidak akan masuk pada aplikasi kita. Hal tersebut sangatlah membantu karena module module kita terdahulu bisa saja memiliki ukuran besar dan belum tentu berguna bagi aplikasi kita. Selain itu aplikasi kita dapat ditest atau diakses oleh user dengan lebih mudah, dikarenakan adanya file `requirements.txt` yang berisi module module beserta versinya yang diperlukan untuk aplikasi kita.

## Apakah kita tetap dapat membuat aplikasi web berbasis Django tanpa menggunakan virtual environment?
Bisa, tetapi akan sangat rentan terhadap error. Misal jika kita memiliki suatu module yang tidak dapat diinstall oleh pihak deployer, maka deploy kita tidak berhasil. Selain itu, ukuran aplikasi web kita akan sangat besar, atau pastinya akan semakin besar lama kelamaan. Hal tersebut dikarenakan kebutuhan kita untuk menginstall module baru, dan jika kita tidak menggunakan virtual environment pasti aplikasi web kita akan ikut menginstall module tersebut yang mengakibatkan pada penumpukan ukuran / size aplikasi pada hal yang tidak mesti diperlukan.

## Jelaskan bagaimana cara kamu mengimplementasikan poin 1 sampai dengan 4 di atas.
1. Pada `katalog/views.py` terdapat fungsi `show_katalog` yang mengambil data dengan `CatalogItem.objects.all()` lalu dirender pada file `katalog/templates/katalog.html` sebagai context sehingga dapat diakses pada file html tersebut.
2. Pada `katalog/urls.py` tambahkan sebuah path pada `urlpatterns` path yang memanggil fungsi `show_katalog`
3. Context yang dirender pada tahap 1 dapat kita akses menggunakan syntax django `{}`. Contohnya, untuk mengakses variabel name kita gunakan syntax `{{name}}` lalu untuk melakukan for pada list `item_catalog` gunakan syntax `{% for item in item_catalog %}`. Syntax lainnya dapat dilihat pada dokumentasi Django.
4. Lakukan deploy pada heroku dengan membuat app dulu pada heroku serta mengimport API_KEY dan APP_NAME pada repository secrets, lalu pada setiap push file `deploy.yml` akan secara otomatis mendeploy aplikasi kita.