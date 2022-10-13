# Tugas 6
## Perbedaan asynchronous programming dengan synchronous?
- Asynchronous programming memanfaatkan konsep multi-thread sehingga memungkinan request secara paralel, dalam artian apabila aplikasi kita melakukan request X, dan setelah itu melakukan request Y. Nah, dengan asynchronous programming kita dapat melakukan kedua request tersebut secara bersamaan, dengan asumsi request Y tidak membutuhkan response dari request X. Nah, dengan keuntungan tersebut otomatis aplikasi kita dapat berjalan lebih cepat (karena request dilakukan bersamaan).
- Synchronous programming tidak memungkinkan hal diatas, karena masih menggunakan single-thread. Sehingga request / task harus dijalankan secara berurutan dan sinkronus.

## Event-Driven Programming
Event adalah action dari user. Sehingga event-driven programming adalah paradigma yang memungkinkan aplikasi kita menjadi lebih terarah dan interaktif. 
    
Contoh kasus: Ada button `Add task` yang jika diklik akan me-popup modal berupa form untuk user memasukkan task.

Implementasi:
```javascript
$("#add-task-button").click(function (e) {
    // popup modal
});
```
## Penerapan asynchornous programming di AJAX
Dengan AJAX, kita dapat melakukan request secara asinkronus. Nanti response dari request tersebut akan kita olah pada file HTML kita. Hal tersebut akan dilakukan secara asinkronus asal mengikuti aturan untuk tidak me-redirect atau me-reload aplikasi kita. 

## Implementasi
- Tambahkan script CDN JQuery
```html
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
```
- Buat views baru yang mereturn semua data task dalam bentuk JSON. Dan tambahkan script AJAX yang melakukan GET request ke views tersebut untuk mendapatkan semua task secara asinkronus.
```javascript
$(document).ready(function () {
    getTaskData();
    postTaskData();
});
    
function getTaskData() {
    $.get("./json/", displayTask);
}
  
function displayTask(data) {
    const container = $("#task-container");
    container.empty();
    if (data.length > 0 && data[0].fields) {
        data.forEach(task => {
            appendTask(task);
        });
    } else {
        container.append(`
        <div id="no-task">
            <br>
            <p class="text-lg">
                Kamu belum membuat todo list, silakan buat dengan mengklik tombol "Buat Todolist" di atas!
            </p>
            <br>
        </div>
        `);
    }
}
```
- Buat handler ajax ketika user telah add task, dan views baru yang menyimpan task baru tersebut di database
```javascript
function postTaskData() {
    $("form#add-task-form").submit(function (e) {
        e.preventDefault();
        var actionURL = e.currentTarget.action;
        var formData = $(this).serialize();
        $.ajax({
            url: actionURL,
            type: "POST",
            data: formData,
            dataType: "json",
            success: (data) => {
                $("#close-task-modal").click();

                // console.log(data);
                appendTask(data[0]);
            },
            error: (error) => {
                console.log(error);
                alert("Error!");
            }
        });
    });
}
```
- Buat handler ajax saat user delete task
```javascript
function deleteTask(id) {
    $.ajax({
        url: `./delete/${id}`,
        type: "DELETE",
        success: (data) => {
            $(`#task-${data.task_id}`).remove();
            getTaskData();
        },
        error: (error) => {
            console.log(error);
            alert("Error!");
        }
    });
}
```
    