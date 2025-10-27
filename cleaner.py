import asyncio
import argparse
import sys
from telethon.sync import TelegramClient
from telethon.errors.rpcerrorlist import FloodWaitError

async def get_channel_entity(client, channel_input):
    """Handles different types of channel inputs."""
    if channel_input.startswith('@'):
        return channel_input
    try:
        return int(channel_input)
    except ValueError:
        print(f"Error: '{channel_input}' is not a valid channel username or ID.", file=sys.stderr)
        sys.exit(1)

async def main(api_id, api_hash, channel_input, keep):
    session_name = "my_session"
    try:
        async with TelegramClient(session_name, api_id, api_hash) as client:
            if not await client.is_user_authorized():
                print("Client not authorized. Please log in.")
                phone = input('Enter phone number (e.g., +1234567890): ')
                await client.send_code_request(phone)
                await client.sign_in(phone, input('Enter code: '))
            
            print(f"Successfully logged in. Session saved to {session_name}.session")
            
            entity = await get_channel_entity(client, channel_input)
            print(f"Fetching messages from {channel_input}...")

            all_message_ids = [msg.id async for msg in client.iter_messages(entity)]
            total_messages = len(all_message_ids)
            print(f"Found a total of {total_messages} messages.")

            if total_messages <= keep * 2:
                print(f"Not enough messages to delete (Total: {total_messages}, Keep: {keep * 2}). Exiting.")
                return

            all_message_ids.sort()
            ids_to_delete = all_message_ids[keep:-keep]
            num_to_delete = len(ids_to_delete)

            if num_to_delete == 0:
                print("No messages to delete after applying the keep filter. Exiting.")
                return

            print(f"Total to delete: {num_to_delete} (Keeping first {keep} and last {keep})")
            confirm = input(f"Are you sure you want to delete {num_to_delete} messages? This CANNOT be undone. (yes/no): ")
            
            if confirm.lower() != 'yes':
                print("Deletion cancelled.")
                return

            print("Starting deletion...")
            total_chunks = (num_to_delete + 99) // 100
            for i in range(0, num_to_delete, 100):
                chunk = ids_to_delete[i:i + 100]
                chunk_num = (i // 100) + 1
                try:
                    await client.delete_messages(entity, chunk)
                    print(f"Deleted chunk {chunk_num}/{total_chunks}")
                    await asyncio.sleep(2)
                except FloodWaitError as e:
                    print(f"Rate limit exceeded. Waiting for {e.seconds} seconds...")
                    await asyncio.sleep(e.seconds)
                    await client.delete_messages(entity, chunk) # Retry
                    print(f"Resumed and deleted chunk {chunk_num}/{total_chunks}")
                except Exception as e:
                    print(f"Error deleting chunk {chunk_num}: {e}", file=sys.stderr)

            print("\n✅ Done! All specified messages have been deleted.")

    except Exception as e:
        print(f"\nAn error occurred: {e}", file=sys.stderr)
        print("Please check your API_ID, API_HASH, and channel ID/username.", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Deletes messages from a Telegram channel, keeping the first and last N.",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("api_id", help="Your Telegram API ID")
    parser.add_argument("api_hash", help="Your Telegram API HASH")
    parser.add_argument("channel", help="The channel username (e.g., @mychannel) or ID (e.g., -100123456)")
    parser.add_argument(
        "-k", "--keep", type=int, default=2,
        help="Number of messages to keep at the start AND end (default: 10)"
    )
    
    args = parser.parse_args()
    
    try:
        int(args.api_id)
    except ValueError:
        print("Error: API ID must be a number.", file=sys.stderr)
        sys.exit(1)

    asyncio.run(main(args.api_id, args.api_hash, args.channel, args.keep))

