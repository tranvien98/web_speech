## Dự đoán văn bản

### Cài đặt

yêu cầu python >= 3.6


`
pip install -r requirements.txt
`

Cài đặt sqlite3

`
sudo apt-get install sqlite3
`

Dòng 36 hàm get_audio sử dụng api để dự đoán lời

Dòng 47 file run_server sử dụng api để dự đoán lời

Lời của file được dự đoán được trả về theo dạng danh sách

ví dụ:

thời gian dạng giây. mili giây

[
"[0.36, 0.63]Bài hát: Gặp Gỡ, Yêu Đương Và Được Bên Em",
"[1.23, 6.34]Ca sĩ: Phan Mạnh Quỳnh",
]




các phần tử trong danh sách có dạng `[thòi gian] + Lời` thời gian được format theo dạng giờ:phút:giây

### Chạy mô hình 

`python3 run_servepy`

sau khi chạy xong truy cập vào địa chỉ `http://0.0.0.0:5050/`

