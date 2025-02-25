from telethon import TelegramClient, events, types
from telethon.errors import FloodWaitError
from telethon.tl.types import Chat, Channel, User
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

# State file to store progress
STATE_FILE = 'forward_state.json'

client = TelegramClient('session_name', api_id, api_hash)

async def display_groups(groups, page, per_page=10):
    """Display groups with pagination"""
    start_idx = page * per_page
    end_idx = start_idx + per_page
    current_groups = groups[start_idx:end_idx]
    
    print("\nGroup List:")
    print("------------------------")
    for i, dialog in enumerate(current_groups, start_idx + 1):
        entity = dialog.entity
        name = dialog.name or "Unnamed"
        print(f"\n{i}. Group Name: {name}")
        print(f"   Group ID: {entity.id}")
        if hasattr(entity, 'participants_count'):
            print(f"   Members: {entity.participants_count}")
        print("   ---------------")
    
    total_pages = (len(groups) + per_page - 1) // per_page
    print(f"\nPage {page + 1} of {total_pages}")
    return total_pages

async def select_group(is_source=True):
    """
    Show list of available groups and let user select one
    
    Args:
        is_source (bool): True if selecting source group, False if selecting target group
    
    Returns:
        The selected group entity
    """
    print(f"\n=== Select {'Source' if is_source else 'Target'} Group ===")
    print("Fetching group list...")
    
    # Get all groups (excluding channels)
    dialogs = []
    async for dialog in client.iter_dialogs():
        # Check if it's a group (not a channel)
        if isinstance(dialog.entity, Chat) or (
            isinstance(dialog.entity, Channel) and dialog.entity.megagroup
        ):
            dialogs.append(dialog)
    
    if not dialogs:
        print("No groups found!")
        return None
        
    page = 0
    per_page = 10
    
    while True:
        total_pages = await display_groups(dialogs, page, per_page)
        
        print("\nGuide:")
        print("- Enter group number to select")
        print("- Enter 'n' for next page")
        print("- Enter 'p' for previous page")
        print("- Enter 's' to search groups")
        print("- Enter 'q' to quit")
        
        choice = input("\nEnter your choice: ").lower()
        
        if choice == 'q':
            return None
            
        elif choice == 'n':
            if page < total_pages - 1:
                page += 1
            else:
                print("You are on the last page.")
                
        elif choice == 'p':
            if page > 0:
                page -= 1
            else:
                print("You are on the first page.")
                
        elif choice == 's':
            search_term = input("Enter group name to search: ").lower()
            filtered_dialogs = [
                d for d in dialogs 
                if search_term in d.name.lower()
            ]
            if filtered_dialogs:
                print("\nSearch Results:")
                for i, dialog in enumerate(filtered_dialogs, 1):
                    print(f"{i}. {dialog.name}")
                try:
                    idx = int(input("\nEnter group number (0 to return): "))
                    if 0 < idx <= len(filtered_dialogs):
                        selected = filtered_dialogs[idx-1]
                        confirm = input(f"\nSelected group: {selected.name}\nIs this correct? (y/n) ").lower()
                        if confirm in ['y', 'yes']:
                            return selected.entity
                except ValueError:
                    print("Please enter a valid number.")
            else:
                print("No groups found with that name.")
                
        else:
            try:
                idx = int(choice)
                if 0 < idx <= len(dialogs):
                    selected = dialogs[idx-1]
                    confirm = input(f"\nSelected group: {selected.name}\nIs this correct? (y/n) ").lower()
                    if confirm in ['y', 'yes']:
                        return selected.entity
                else:
                    print("Invalid number.")
            except ValueError:
                print("Please enter a valid option.")

async def show_menu():
    """Show menu to user and get starting point for forwarding"""
    print("\n=== Message Forward Menu ===")
    print("1. Start from beginning")
    print("2. Continue from last point")
    print("3. Start from specific message_id")
    
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
                    print("No saved state found. Starting from beginning.")
                    return 0, 0, None
                    
            elif choice == "3":
                while True:
                    try:
                        msg_id = int(input("Enter message_id to start from: "))
                        if msg_id <= 0:
                            print("message_id must be positive.")
                            continue
                            
                        msgs_forwarded = int(input("Enter number of messages forwarded up to this message_id: "))
                        if msgs_forwarded < 0:
                            print("Number of messages cannot be negative.")
                            continue
                            
                        return msg_id, msgs_forwarded, None
                        
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
    """Convert gregorian date to persian date string"""
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

async def forward_messages(source_entity, target_entity, start_message_id=0, start_messages_forwarded=0, start_date=None):
    try:
        last_message_id = start_message_id
        messages_forwarded = start_messages_forwarded
        last_processed_date = start_date
        current_date = None
        
        while True:
            try:
                # Get messages with extra buffer for reply checking
                print(f"Fetching messages after ID: {last_message_id}")
                messages = await client.get_messages(source_entity, limit=105,
                                                  offset_id=last_message_id if last_message_id else 0,
                                                  reverse=True)
                
                if not messages:
                    print("No more messages to forward")
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
                                await client.send_message(target_entity, date_header)
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
                            await client.forward_messages(target_entity, messages=batch, from_peer=source_entity)
                            messages_forwarded += len(batch)
                            last_message_id = batch[-1].id
                            save_state(last_message_id, messages_forwarded, current_date)
                            
                            print(f"Successfully forwarded batch of {len(batch)} messages. Total: {messages_forwarded}")
                            logger.info(f"Successfully forwarded batch of {len(batch)} messages")
                            
                            # Take longer break every 500 messages
                            if messages_forwarded % 500 == 0:
                                print(f"Forwarded {messages_forwarded} messages, taking a longer break...")
                                logger.info(f"Forwarded {messages_forwarded} messages, taking a break...")
                                await asyncio.sleep(180)
                            else:
                                await asyncio.sleep(3)
                            
                            batch_start += batch_size
                        except FloodWaitError as e:
                            print(f"Hit rate limit. Waiting {e.seconds} seconds...")
                            logger.warning(f"FloodWaitError: {e}")
                            await asyncio.sleep(e.seconds)
                            continue
                        except Exception as e:
                            print(f"Error forwarding batch: {e}")
                            logger.error(f"Error forwarding batch: {e}")
                            await asyncio.sleep(30)
                            continue
                    else:
                        batch_start += 1

            except Exception as e:
                print(f"Error in forwarding loop: {e}")
                logger.error(f"Error in main loop: {e}")
                save_state(last_message_id, messages_forwarded, current_date)
                await asyncio.sleep(60)
                continue

    except Exception as e:
        print(f"Fatal error: {e}")
        logger.error(f"Fatal error: {e}")
        save_state(last_message_id, messages_forwarded, current_date)

async def main():
    print("Starting Telegram Forward Bot...")
    await client.start()
    
    # Select source and target groups
    print("\nPlease select the source group:")
    source_entity = await select_group(is_source=True)
    if not source_entity:
        print("Source group selection cancelled.")
        await client.disconnect()
        return
    
    print("\nPlease select the target group:")
    target_entity = await select_group(is_source=False)
    if not target_entity:
        print("Target group selection cancelled.")
        await client.disconnect()
        return
    
    # Get starting point
    start_message_id, start_messages_forwarded, start_date = await show_menu()
    
    # Start forwarding
    print("\nStarting message forwarding...")
    await forward_messages(source_entity, target_entity, start_message_id, start_messages_forwarded, start_date)
    
    print("Forwarding completed.")
    await client.disconnect()

if __name__ == '__main__':
    print("Initializing...")
    client.loop.run_until_complete(main())
