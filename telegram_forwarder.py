from telethon import TelegramClient, events, types
from telethon.errors import FloodWaitError
import asyncio
import logging
import json
import os
from datetime import datetime
from telethon import types
import jdatetime

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Replace these with your values
api_id = 'YOUR_API_ID'
api_hash = 'YOUR_API_HASH'
source_user = '@SOURCE_CHANNEL'
target_group = 'TARGET_GROUP_LINK'

# State file to store progress
STATE_FILE = 'forward_state.json'

client = TelegramClient('session_name', api_id, api_hash)

async def show_menu():
    """Show menu to user and get starting point for forwarding"""
    print("\n=== Message Forwarding Menu ===")
    print("1. Start from the beginning")
    print("2. Continue from the last point")
    print("3. Start from a specific message_id")
    
    while True:
        try:
            choice = input("\nPlease select an option (1-3): ")
            
            if choice == "1":
                if os.path.exists(STATE_FILE):
                    os.remove(STATE_FILE)
                return 0, 0, None
                
            elif choice == "2":
                state = load_state()
                if state:
                    return state["last_message_id"], state["messages_forwarded"], state["last_date"]
                else:
                    print("No saved state found. Starting from the beginning.")
                    return 0, 0, None
                    
            elif choice == "3":
                while True:
                    try:
                        msg_id = int(input("Please enter the message_id: "))
                        if msg_id <= 0:
                            print("message_id must be a positive number.")
                            continue
                            
                        return msg_id, None
                        
                    except ValueError:
                        print("Please enter valid numbers.")
            
            else:
                print("Invalid option. Please enter a number between 1 and 3.")
                
        except Exception as e:
            print(f"Error: {e}")
            print("Please try again.")

def save_state(last_message_id, messages_forwarded, last_date):
    """Save current state to file"""
    state = {
        "last_message_id": last_message_id,
        "messages_forwarded": messages_forwarded,
        "last_date": last_date.isoformat() if last_date else None
    }
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f)
    logger.info(f"State saved: {state}")

def load_state():
    """Load state from file"""
    try:
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, 'r') as f:
                state = json.load(f)
                if state.get("last_date"):
                    state["last_date"] = datetime.fromisoformat(state["last_date"])
                return state
    except Exception as e:
        logger.error(f"Error loading state: {e}")
    return None

def get_persian_date(date):
    """Convert Gregorian date to Persian date string"""
    try:
        persian_date = jdatetime.datetime.fromgregorian(datetime=date)
        weekday = persian_date.strftime("%A")
        day = persian_date.day
        month = persian_date.strftime("%B")
        year = persian_date.year
        return f"{weekday} {day} {month} {year}"
    except Exception as e:
        logger.error(f"Error converting date: {e}")
        return str(date)

async def find_safe_batch_end(messages, batch_start, check_next=5):
    """Find the largest safe batch size that ensures no reply chain breaks"""
    if not messages:
        return 0
    
    max_size = min(100, len(messages) - batch_start)
    if max_size <= 0:
        return 0
        
    for size in range(max_size, 0, -1):
        end_idx = batch_start + size
        current_batch_ids = [msg.id for msg in messages[batch_start:end_idx]]
        
        # Check next messages for replies to current batch
        is_safe = True
        for i in range(min(check_next, len(messages) - end_idx)):
            next_msg = messages[end_idx + i]
            
            # Check if message has a reply
            if hasattr(next_msg, 'reply_to'):
                # Handle normal replies
                if hasattr(next_msg.reply_to, 'reply_to_msg_id'):
                    if next_msg.reply_to.reply_to_msg_id in current_batch_ids:
                        is_safe = False
                        break
                # Handle story replies - we can safely ignore them for batching
                elif isinstance(next_msg.reply_to, types.MessageReplyStoryHeader):
                    continue
                    
        if is_safe:
            return size
            
    return 1  # Fallback to single message if no safe size found

async def forward_messages(start_message_id=0, start_messages_forwarded=0, start_date=None):
    try:
        source = await client.get_entity(source_user)
        target = await client.get_entity(target_group)
        
        last_message_id = start_message_id
        messages_forwarded = start_messages_forwarded
        last_processed_date = start_date
        current_date = None
        
        while True:
            try:
                # Get messages with extra buffer for reply checking
                messages = await client.get_messages(source, limit=105,
                                                  offset_id=last_message_id if last_message_id else 0,
                                                  reverse=True)
                
                if not messages:
                    logger.info("No more messages to forward")
                    break

                # Filter out service messages and create valid messages list
                valid_messages = []
                for msg in messages:
                    # Skip service messages, None messages, and messages without content
                    if (msg is None or 
                        isinstance(msg, types.MessageService) or 
                        (not msg.message and not msg.media)):
                        continue
                        
                    # Skip messages that are replies to stories
                    if (hasattr(msg, 'reply_to') and 
                        isinstance(msg.reply_to, types.MessageReplyStoryHeader)):
                        logger.info(f"Skipping story reply message {msg.id}")
                        continue
                        
                    valid_messages.append(msg)

                batch_start = 0
                while batch_start < len(valid_messages):
                    message = valid_messages[batch_start]
                    message_date = message.date.replace(hour=0, minute=0, second=0, microsecond=0)
                    
                    # Handle date header
                    if current_date is None or message_date != current_date:
                        if not last_processed_date or message_date != last_processed_date:
                            try:
                                date_header = f"---------- Messages from {get_persian_date(message_date)} ----------"
                                await client.send_message(target, date_header)
                                await asyncio.sleep(2)
                            except Exception as e:
                                logger.error(f"Error sending date header: {e}")
                                await asyncio.sleep(30)
                                continue
                        
                        current_date = message_date
                        last_processed_date = message_date

                    # Find safe batch size
                    batch_size = await find_safe_batch_end(valid_messages, batch_start)
                    if batch_size > 0:
                        try:
                            batch = valid_messages[batch_start:batch_start + batch_size]
                            await client.forward_messages(target, messages=batch)
                            messages_forwarded += len(batch)
                            last_message_id = batch[-1].id
                            save_state(last_message_id, messages_forwarded, current_date)
                            
                            logger.info(f"Successfully forwarded batch of {len(batch)} messages")
                            
                            # Take longer break every 500 messages
                            if messages_forwarded % 500 == 0:
                                logger.info(f"Forwarded {messages_forwarded} messages, taking a break...")
                                await asyncio.sleep(180)
                            else:
                                await asyncio.sleep(3)
                            
                            batch_start += batch_size
                        except Exception as e:
                            logger.error(f"Error forwarding batch: {e}")
                            await asyncio.sleep(30)
                            continue
                    else:
                        batch_start += 1

            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                save_state(last_message_id, messages_forwarded, current_date)
                await asyncio.sleep(60)
                continue

    except Exception as e:
        logger.error(f"Fatal error: {e}")
        save_state(last_message_id, messages_forwarded, current_date)

async def main():
    await client.start()
    start_message_id, start_messages_forwarded, start_date = await show_menu()
    await forward_messages(start_message_id, start_messages_forwarded, start_date)
    await client.disconnect()

if __name__ == '__main__':
    client.loop.run_until_complete(main())