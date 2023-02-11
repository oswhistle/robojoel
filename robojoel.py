from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Initialize a Slack client using an API token
SLACK_TOKEN = "xoxp-12623173760-12619319411-4772998756407-a13258d98da631dbbff2f35bbcfd3e57"
client = WebClient(token=SLACK_TOKEN)

# The channel and message to watch for
channel_id = "rostering"
trigger_text = "Birthday Party 12:30"

# The message to post in response
response_text = "I can do this one!"

try:
    # Call the conversations.list method to get a list of channels
    response = client.conversations_list()
    channels = response["channels"]
    
    # Find the channel with the specified name
    target_channel = None
    for channel in channels:
        if channel["name"] == channel_id:
            target_channel = channel
            break
    if not target_channel:
        print(f"Error: Could not find channel {channel_id}")
        exit()
    target_channel_id = target_channel["id"]
    # Call the conversations.history method to get the channel history
    response = client.conversations_history(channel=target_channel_id)
    messages = response["messages"]
    for message in messages:
        if "text" in message and trigger_text in message["text"]:
            # Post the response message as a reply to the triggering message
            response = client.chat_postMessage(channel=target_channel_id, text=response_text, thread_ts=message["ts"])
            print(f"Response posted to channel {channel_id}")
            break

except SlackApiError as e:
    print("Error : {}".format(e))
