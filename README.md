# Telegram Message Forwarder 📱
[English](#english) | [فارسی](#فارسی)
## English
### 📝 Description
A Python script that allows you to forward messages from a Telegram channel/user to another channel/group with advanced features like batch processing, state management, and error handling.
### ⭐ Features
- 🔍 **Interactive Group Selection** - Browse and select source/target groups directly from your Telegram
- 🔎 **Group Search** - Find groups by name using the search function
- 📋 **Paginated Group List** - Navigate through your groups with easy pagination
- 🔄 Forward messages in batches for better performance
- 💾 Save progress and resume from last point
- 📅 Add date headers in standard format
- 🗓️ **Persian Calendar Support** - Date headers in Persian format
- 🎯 Start forwarding from:
  - Beginning
  - Last saved point
  - Specific message ID
- ⚡ Smart batch processing that preserves reply chains
- 🛡️ Enhanced error handling and retry mechanisms
- ⚠️ **FloodWait Protection** - Smart handling of Telegram rate limits
- ⏲️ Automatic delays to prevent flooding
- 📊 Improved progress tracking and logging
- 👥 **Group Info Display** - See member counts and other group details
### 🚀 Setup & Configuration
1. Install python packages:
```bash
pip install telethon jdatetime
```
2. Configure the following variables in the script:
```python
api_id = 'YOUR_API_ID'
api_hash = 'YOUR_API_HASH'
```
[🔑How To Get Telegram API key](https://github.com/TheMarwin/Telegram-Forward-Messages/blob/main/Telegram_API_guide_en.md)
### 💻 Usage
1. Run the script:
```bash
python telegram_forwarder.py
```
2. Follow the interactive prompts:
   - 🔍 Select source group from the list or search by name
   - 🔍 Select target group from the list or search by name
   - 🚀 Choose from the menu options:
     - Start from beginning
     - Continue from last point
     - Start from specific message ID
### 🧭 Navigation Commands
- 'n' → Next page of groups
- 'p' → Previous page of groups
- 's' → Search for groups by name
- 'q' → Quit selection
### ⚠️ Important Notes
- Requires Telegram API credentials
- Respects message reply chains
- Handles Story replies appropriately
- Includes automatic pauses to prevent rate limiting
- Takes longer breaks every 500 messages
- ✅ Now with confirmation dialogs for critical actions
---
## فارسی
### 📝 توضیحات
اسکریپت پایتون برای انتقال پیام‌ها از یک کانال/کاربر تلگرام به کانال/گروه دیگر با ویژگی‌های پیشرفته مانند پردازش دسته‌ای، مدیریت وضعیت و مدیریت خطا.
### ⭐ ویژگی‌ها
- 🔍 **انتخاب تعاملی گروه** - مرور و انتخاب گروه‌های منبع/مقصد مستقیماً از تلگرام شما
- 🔎 **جستجوی گروه** - یافتن گروه‌ها با نام با استفاده از عملکرد جستجو
- 📋 **لیست صفحه‌بندی شده گروه‌ها** - پیمایش آسان بین گروه‌های خود
- 🔄 انتقال پیام‌ها به صورت دسته‌ای برای عملکرد بهتر
- 💾 ذخیره پیشرفت و ادامه از آخرین نقطه
- 📅 اضافه کردن هدر تاریخ به فرمت استاندارد
- 🗓️ **پشتیبانی از تقویم شمسی** - نمایش هدرهای تاریخ به فرمت شمسی
- 🎯 شروع انتقال از:
  - ابتدا
  - آخرین نقطه ذخیره شده
  - message_id خاص
- ⚡ پردازش هوشمند دسته‌ای با حفظ زنجیره پاسخ‌ها
- 🛡️ مدیریت خطای پیشرفته و مکانیزم‌های تلاش مجدد
- ⚠️ **محافظت از FloodWait** - مدیریت هوشمند محدودیت‌های نرخ تلگرام
- ⏲️ تاخیرهای خودکار برای جلوگیری از فلود
- 📊 پیگیری پیشرفت و لاگ‌گیری بهبود یافته
- 👥 **نمایش اطلاعات گروه** - مشاهده تعداد اعضا و سایر جزئیات گروه
### 🚀 نصب و پیکربندی
1. نصب پکیج‌های مورد نیاز:
```bash
pip install telethon jdatetime
```
2. تنظیم متغیرهای زیر در اسکریپت:
```python
api_id = 'YOUR_API_ID'
api_hash = 'YOUR_API_HASH'
```
[🔑نحوه دریافت API تلگرام](https://github.com/TheMarwin/Telegram-Forward-Messages/blob/main/Telegram_API_guide_fa.md)
### 💻 نحوه استفاده
1. اجرای اسکریپت:
```bash
python telegram_forwarder.py
```
2. دنبال کردن راهنماهای تعاملی:
   - 🔍 انتخاب گروه منبع از لیست یا جستجو با نام
   - 🔍 انتخاب گروه مقصد از لیست یا جستجو با نام
   - 🚀 انتخاب از گزینه‌های منو:
     - شروع از ابتدا
     - ادامه از آخرین نقطه
     - شروع از message_id خاص
### 🧭 دستورات ناوبری
- 'n' → صفحه بعدی گروه‌ها
- 'p' → صفحه قبلی گروه‌ها
- 's' → جستجوی گروه‌ها با نام
- 'q' → خروج از انتخاب
### ⚠️ نکات مهم
- نیاز به اعتبارنامه API تلگرام دارد
- زنجیره پاسخ‌های پیام‌ها را حفظ می‌کند
- پاسخ‌های Story را به درستی مدیریت می‌کند
- شامل توقف‌های خودکار برای جلوگیری از محدودیت نرخ ارسال
- هر 500 پیام یک وقفه طولانی‌تر ایجاد می‌کند
- ✅ اکنون با دیالوگ‌های تأیید برای اقدامات حساس
