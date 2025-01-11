## 🔑 How to Get Telegram API Credentials

### 🇺🇸 English Instructions:

1. Visit [my.telegram.org](https://my.telegram.org) and log in
2. Click on "API development tools"
3. Fill in your application details:
   - App title: Your app name (e.g., "Message Forwarder")
   - Short name: Short version of name (e.g., "msgfwd")
   - Platform: Choose "Desktop"
   - Description: Brief description of your app
4. Click "Create application"
5. You will receive:
   - `api_id`: A number like "1234567"
   - `api_hash`: A 32-character string
6. Copy these values to your script:
```python
api_id = 'YOUR_API_ID'
api_hash = 'YOUR_API_HASH'
```

⚠️ **IMPORTANT**: 
- Never share your `api_id` and `api_hash` with anyone
- Don't commit these values to GitHub
- Consider using environment variables or a config fileد
