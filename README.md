# Telegram Message Forwarder 📱

[English](#english) | [فارسی](#فارسی)

## English

### 📝 Description
A Python script that allows you to forward messages from a Telegram channel/user to another channel/group with advanced features like batch processing, state management, and error handling.

### ⭐ Features
- 🔄 Forward messages in batches for better performance
- 💾 Save progress and resume from last point
- 📅 Add date headers in standard format (e.g., "Sunday 14 January 2024")
- 🎯 Start forwarding from:
  - Beginning
  - Last saved point
  - Specific message ID
- ⚡ Smart batch processing that preserves reply chains
- 🛡️ Error handling and retry mechanisms
- ⏲️ Automatic delays to prevent flooding
- 📊 Progress tracking and logging

### 🚀 Setup & Configuration
1. Install python packages:
```bash
pip install telethon
```

2. Configure the following variables in the script:
```python
api_id = 'YOUR_API_ID'
api_hash = 'YOUR_API_HASH'
source_user = '@SOURCE_CHANNEL'
target_group = 'TARGET_GROUP_LINK'
```
[🔑How To Get Telegram API key](https://github.com/TheMarwin/Telegram-Message-Forwarder/blob/main/Telegram_API_guide_en.md)


### 💻 Usage
1. Run the script:
```bash
python telegram_forwarder.py
```

2. Choose from the menu options:
   - Start from beginning
   - Continue from last point
   - Start from specific message ID

### ⚠️ Important Notes
- Requires Telegram API credentials
- Respects message reply chains
- Handles Story replies appropriately
- Includes automatic pauses to prevent rate limiting
- Takes longer breaks every 500 messages

---

## فارسی

### 📝 توضیحات
اسکریپت پایتون برای انتقال پیام‌ها از یک کانال/کاربر تلگرام به کانال/گروه دیگر با ویژگی‌های پیشرفته مانند پردازش دسته‌ای، مدیریت وضعیت و مدیریت خطا.

### ⭐ ویژگی‌ها
- 🔄 انتقال پیام‌ها به صورت دسته‌ای برای عملکرد بهتر
- 💾 ذخیره پیشرفت و ادامه از آخرین نقطه
- 📅 اضافه کردن هدر تاریخ به فرمت استاندارد (مثال: "Sunday 14 January 2024")
- 🎯 شروع انتقال از:
  - ابتدا
  - آخرین نقطه ذخیره شده
  - message_id خاص
- ⚡ پردازش هوشمند دسته‌ای با حفظ زنجیره پاسخ‌ها
- 🛡️ مدیریت خطا و مکانیزم‌های تلاش مجدد
- ⏲️ تاخیرهای خودکار برای جلوگیری از فلود
- 📊 پیگیری پیشرفت و لاگ‌گیری

### 🚀 نصب و پیکربندی
1. نصب پکیج‌های مورد نیاز:
```bash
pip install telethon
```

2. تنظیم متغیرهای زیر در اسکریپت:
```python
api_id = 'YOUR_API_ID'
api_hash = 'YOUR_API_HASH'
source_user = '@SOURCE_CHANNEL'
target_group = 'TARGET_GROUP_LINK'
```
[🔑نحوه دریافت API تلگرام](https://github.com/TheMarwin/Telegram-Message-Forwarder/blob/main/Telegram_API_guide_fa.md)

### 💻 نحوه استفاده
1. اجرای اسکریپت:
```bash
python telegram_forwarder.py
```

2. انتخاب از گزینه‌های منو:
   - شروع از ابتدا
   - ادامه از آخرین نقطه
   - شروع از message_id خاص

### ⚠️ نکات مهم
- نیاز به اعتبارنامه API تلگرام دارد
- زنجیره پاسخ‌های پیام‌ها را حفظ می‌کند
- پاسخ‌های Story را به درستی مدیریت می‌کند
- شامل توقف‌های خودکار برای جلوگیری از محدودیت نرخ ارسال
- هر 500 پیام یک وقفه طولانی‌تر ایجاد می‌کند
