
---

## 1. Chạy server

1. Mở Terminal (hoặc Git Bash/PowerShell).  
2. Chuyển đến thư mục chứa project.
   ```bash
   cd "C:/Users/Admin/Documents/project Blockchain"
   ```
3. Chạy server bằng lệnh:
   ```bash
   python app.py
   ```
4. Xác nhận trong Terminal xuất hiện thông báo như:
   ```
   * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
   ```
   – Điều này có nghĩa là server đã chạy trên cổng 5000.

---

## 2. Test API từng bước

### 2.1. Xem danh sách giao dịch chờ

- Mở trình duyệt (hoặc dùng PowerShell với `Invoke-RestMethod`) và truy cập:
  ```
  http://127.0.0.1:5000/pending
  ```
- Nếu chưa có giao dịch nào, kết quả trả về sẽ là:
  ```json
  []
  ```

### 2.2. Thêm giao dịch mới

- Sử dụng PowerShell (với `Invoke-RestMethod`) để gửi yêu cầu POST:

  ```powershell
  Invoke-RestMethod -Uri http://127.0.0.1:5000/transfer -Method Post -Body '{"sender": "Khanh", "receiver": "Duc Anh", "amount": 100000}' -ContentType "application/json"
  ```
- Kết quả trả về dự kiến:
  ```json
  {"message": "Giao dịch đã ký và thêm vào block chờ!"}
  ```
- Sau đó, truy cập lại `http://127.0.0.1:5000/pending` để kiểm tra danh sách giao dịch chờ.  sẽ thấy mảng chứa giao dịch vừa thêm.

### 2.3. Đào block

- Sau khi có giao dịch trong danh sách chờ, gửi yêu cầu GET đến endpoint mine:
  
  ```powershell
  Invoke-RestMethod -Uri http://127.0.0.1:5000/mine -Method Get
  ```
- Nếu có giao dịch chờ, server sẽ đào block và trả về:
  ```json
  {"message": "Block mới đã được đào thành công!"}
  ```
- Trong Terminal,  sẽ thấy log cho biết quá trình "Mining pending transactions" đã diễn ra, block mới được thêm và blockchain được lưu vào file JSON (xem thông báo "Blockchain đã được lưu vào file: blockchain_data.json").

### 2.4. Kiểm tra toàn bộ blockchain

- Gửi yêu cầu GET đến endpoint `/chain`:
  ```powershell
  Invoke-RestMethod -Uri http://127.0.0.1:5000/chain -Method Get
  ```
- Kết quả trả về sẽ là một mảng JSON chứa ít nhất 2 block:  
  - Block Genesis  
  - Block mới chứa giao dịch `{ "sender": "Khanh", "receiver": "Duc Anh", "amount": 100000, ... }`.

### 2.5. Kiểm tra file lưu trữ

- Mở file `blockchain_data.json` trong thư mục dự án ( cótắt

- Bắt đầu: Chạy server.  
- Thêm giao dịch: Sử dụng POST `/transfer` để gửi giao dịch.  
- Đào block: Gọi GET `/mine` để chuyển giao dịch từ pending sang block mới.  
- Xem chain: Gọi GET `/chain` để xem toàn bộ chuỗi blockchain.  
- Lưu trữ: Kiểm tra file `blockchain_data.json` để đảm bảo dữ liệu đã được lưu lại và có thể khôi phục khi server khởi động lại.

Nếu làm đúng các bước trên, dự án blockchain sẽ hoạt động ổn định và lưu trữ dữ liệu một cách bền vững qua file JSON.

Trên đây là mô phỏng cơ bản của 1 Project Blockchain trong lĩnh vực ngân hàng.
