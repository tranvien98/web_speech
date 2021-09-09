## Dự đoán văn bản

### Cài đặt

yêu cầu python >= 3.6


`
pip install -r requirements.txt
`

Dòng 47 file run_server sử dụng api để dự đoán lời

Lời của file được dự đoán được trả về theo dạng danh sách

ví dụ:

[
"[00:00.06]Bài hát: Gặp Gỡ, Yêu Đương Và Được Bên Em",
"[00:02.46]Ca sĩ: Phan Mạnh Quỳnh",
]

các phần tử trong danh sách có dạng `[thòi gian] + Lời` thời gian được format theo dạng giờ:phút:giây

### Chạy mô hình 

`python3 run_servepy`

sau khi chạy xong truy cập vào địa chỉ `http://0.0.0.0:5050/`

