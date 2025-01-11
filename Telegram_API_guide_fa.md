## 🔑نحوه دریافت اعتبارنامه API تلگرام

### **![Lang_farsi](https://user-images.githubusercontent.com/125398461/234186932-52f1fa82-52c6-417f-8b37-08fe9250a55f.png) راهنمای فارسی**:

1. به [my.telegram.org](https://my.telegram.org) برید و وارد حساب خودتان شوید
2. روی "API development tools" کلیک کنید
3. مشخصات برنامه را پر کنید:
   - `App title`: نام برنامه (مثلاً "Message Forwarder")
   - `Short name`: نام کوتاه (مثلاً "msgfwd")
   - `Platform`: گزینه "Desktop" را انتخاب کنید
   - `Description`: توضیح مختصر برنامه
   
5. روی "Create application" کلیک کنید
6. درصورت صحبح وارد کردن اطلاعات، مقادیر زیر به شما داده می‌شود:
   - `api_id`: یک عدد مانند "1234567"
   - `api_hash`: یک رشته 32 کاراکتری
7. این مقادیر را در اسکریپت خود قرار دهید:
```python
api_id = 'YOUR_API_ID'
api_hash = 'YOUR_API_HASH'
```

⚠️ **مهم**:
- هرگز `api_id` و `api_hash` خود را با کسی به اشتراک نگذارید
- این مقادیر را در GitHub کامیت نکنید
- بهتر است از متغیرهای محیطی یا فایل کانفیگ استفاده کنید
