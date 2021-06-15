
import os
from time import time
from datetime import datetime
from slack_bolt import App, Ack
from slack import WebClient
from travel import travel_bot
#export SLACK_EVENTS_TOKEN='cfc7d7ebfd3d2843066e84e9ab8ff50f'
#export SLACK_TOKEN='xoxb-2135193288769-2120092576725-284jGR0LqQbQ6lVItvNrBbE1'


app = App(
    signing_secret = os.environ.get("SLACK_EVENTS_TOKEN"),

# Initialize a Web API client
    token=os.environ.get("SLACK_TOKEN")
)

@app.shortcut("ice")
def travel_modal(shortcut, say, client, ack):
    ack()
    client.views_open(
        trigger_id=shortcut["trigger_id"],
        view=travel_bot.TRAVEL_BLOCK)

@app.view("view_travel")
def handle_submission(ack, body, client, view, logger, message, user):
    # Assume there's an input block with `block_c` as the block_id and `dreamy_input`
    line1 = view["state"]["values"]["block_a"]["departure"]["selected_date"]
    line2 = view["state"]["values"]["block_from"]["from_select"]["selected_option"]["text"]["text"]
    line3 = view["state"]["values"]["block_b"]["return"]["selected_date"]
    line4 = view["state"]["values"]["block_return"]["to_select"]["selected_option"]["text"]["text"]
    line5 = view["state"]["values"]["block_vehicle"]["vehicle_select"]["selected_option"]["text"]["text"]
    line6 = view["state"]["values"]["block_class"]["class_select"]["selected_option"]["text"]["text"]
    line7 = view["state"]["values"]["block_d"]["reason_input"]["value"]
    line8 = view["state"]["values"]["block_perdiem"]["perdiem_select"]["selected_option"]["text"]["text"]
    line9 = view["state"]["values"]["block_id"]["input_id"]["value"]
    line10 = view["state"]["values"]["block_bank"]["bank_input"]["value"]
    line11 = view["state"]["values"]["block_user_input"]["user_select"]["selected_users"][0]
    response = client.users_info(user=f"{body['user']['id']}")
    assert(response)
    #profile = response['user']['profile']
    display_name = response['user']['profile']['display_name']
    phone = response['user']['profile']['phone']
    title = response['user']['profile']['title']
    avatar = response['user']['profile']['image_72']
    email = response['user']['profile']['email']
    # Validate the inputs
    # Acknowledge the view_submission event and close the modal
    errors = {}
    date1 = datetime.strptime(line1, "%Y-%m-%d")
    date2 = datetime.strptime(line3, "%Y-%m-%d")
    date3 = datetime.strptime(datetime.today().strftime('%Y-%m-%d'), "%Y-%m-%d")
    timestamp1 = datetime.timestamp(date1)
    timestamp2 = datetime.timestamp(date2)
    timestamp3 = datetime.timestamp(date3)
    if timestamp1 is not None and timestamp1 > timestamp2:
        errors["block_a"] = "Departure date cannot be later than return date"
    if timestamp1 - timestamp3 < 259200:
        errors["block_a"] = "You have to make the request 3 days in advance"
    if len(errors) > 0:
        ack(response_action="errors", errors=errors)
        return
    ack()
    # Do whatever you want with the input data - here we're saving it to a DB
    # then sending the user a verification of their submission

    # Message to send user
    msg = ""
    try:
        # Save to DB
        msg = f":airplane_departure: *Departure:* \n{line1}\n:airplane_arriving: *Arrival:* \n{line3}\n*From:* \n{line2}\n*To:*\n{line4}\n*Vehicle: * {line5}\n*Class: * {line6}\n *ID/Passport number: *\n{line9}\n*Reasons for travel:*\n{line7}\n*Per diem request: * {line8}\n*Bank information: *\n{line10}"
    except Exception as e:
        # Handle error
        msg = "There was an error with your submission"

    # Message the user
    try:
        client.chat_postMessage(channel='C0252EMRTS7', blocks=[
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": f"You have a new request from *<@{body['user']['username']}>* with email *{email}*:\n*Display name: * {display_name}\n*Title: * {title}\n*Phone: * {phone}"
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": msg
			},
			"accessory": {
				"type": "image",
				"image_url": f"{avatar}",
				"alt_text": "computer thumbnail"
			}
		}
	])
        client.chat_postMessage(channel=f'{line11}', blocks=[
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": f"You have a new request from *<@{body['user']['username']}>* with email *{email}*:\n*Display name: * {display_name}\n*Title: * {title}\n*Phone: * {phone}"
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": msg
			},
			"accessory": {
				"type": "image",
				"image_url": f"{avatar}",
				"alt_text": "computer thumbnail"
			}
		},
		{
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"emoji": True,
						"text": "Approve"
					},
					"style": "primary",
					"action_id": "button1"
				},
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"emoji": True,
						"text": "Deny"
					},
					"style": "danger",
					"action_id": "button2"
				}
			]
		}
	])
    except e:
        logger.exception(f"Failed to post a message {e}")

@app.view("view_travel_update")
def view_update(ack, body, client, view, logger, message, user, say):
    ack()
    say("nice")

@app.action("button1")
def action_button_click1(body, ack, say, client, view):
    # Acknowledge the action
    user = body["user"]["id"]
    ts=body['message']['ts']
    result = client.conversations_history(channel = 'C0252EMRTS7', inclusive=True,latest=ts,limit=1)
    conversation_history = f"{result['messages'][0]['blocks'][0]['text']['text']}\n{result['messages'][0]['blocks'][1]['text']['text']}"
    msg = conversation_history
    ack()
    client.chat_postMessage(channel = body['message']['user'], text = f"<@{body['user']['id']}> approved")
    client.chat_postMessage(channel = user, text = f"<@{body['user']['id']}> approved")
    client.chat_postMessage(channel = 'C024Z67LNDB', blocks=[
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": f"You have a new request from *<@{body['user']['username']}>*"
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": msg
			}
		},
		{
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"emoji": True,
						"text": "Done"
					},
					"style": "primary",
					"action_id": "button_done"
				}
			]
		}
	])

@app.action("button_done")
def info_click(body, say, client, ack, action):
    ts=body['message']['ts']
    result = client.conversations_history(channel = "C0252EMRTS7", inclusive=True,latest=ts,limit=1)
    conversation_history = f"{result['messages'][0]['blocks'][0]['text']['text']}\n{result['messages'][0]['blocks'][1]['text']['text']}"
    msg = conversation_history
    ack()
    client.chat_update(ts=ts, channel = 'C024Z67LNDB', blocks=[
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": f"You have a new request from *<@{body['user']['username']}>*"
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": msg
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": f":white_check_mark: Use the command */travelinfo* to fill out the travelling form"
			}
		}
	])

@app.command("/travelinfo")
def info_modal(body, say, client, ack, command):
    ack()
    client.views_open(
        trigger_id=command["trigger_id"],
        view=travel_bot.SEND_INFO)

@app.view("view_info")
def handle_info_travel(ack, body, client, view, logger, message, user,say):
    # Assume there's an input block with `block_c` as the block_id and `dreamy_input`
    line1 = view["state"]["values"]["block_a_input"]["user_select"]["selected_users"][0]
    line2 = view["state"]["values"]["block_b_input"]["vehicle_select"]["selected_option"]["text"]["text"]
    line3 = view["state"]["values"]["block_c_input"]["vehicle_num"]["value"]
    line4 = view["state"]["values"]["block_d_input"]["driver_name"]["value"]
    line5 = view["state"]["values"]["block_e_input"]["driver_num"]["value"]
    line6 = view["state"]["values"]["block_f_input"]["hotel_name"]["value"]
    line7 = view["state"]["values"]["block_g_input"]["hotel_location"]["value"]
    line8 = view["state"]["values"]["block_h_input"]["hotel_num"]["value"]
    line9 = view["state"]["values"]["block_j_input"]["boarding_pass"]["value"]
    line10 = view["state"]["values"]["block_k_input"]["note_id"]["value"]
    response = client.users_info(user=line1)
    assert(response)
    profile = response['user']['profile']['display_name']
    # Validate the inputs
    # Acknowledge the view_submission event and close the modal
    ack()
    # Do whatever you want with the input data - here we're saving it to a DB
    # then sending the user a verification of their submission
    # Message to send user
    msg = ""
    try:
        # Save to DB
        msg = f"Hello *{profile}*, this is your travel information:\n*Vehicle:* {line2}\n*Vehicle's number/License plate:* {line3}\n*Driver's name:* {line4}\n*Diver's phone number: * {line5}\n*Hotel: * {line6}\n *Hotel's location: * {line7}\n*Hotel's booking number:*\n{line8}\n*Boarding pass (if travel by plane): * {line9}\n*Note:*\n{line10}"
    except Exception as e:
        # Handle error
        msg = "There was an error with your submission"

    # Message the user
    try:
        client.chat_postMessage(channel=f'{line1}', blocks=[
        {
			"type": "divider"
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": f"You have received new travel information from *<@{body['user']['username']}>*"
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": msg
			}
		}
	])
    except e:
        logger.exception(f"Failed to post a message {e}")

@app.action("button2")
def action_button_click2(body, ack, say, client):
    # Acknowledge the action
    user = body["user"]["id"]
    ack()
    client.chat_postMessage(channel = user, text = f"<@{body['user']['id']}> denied")

# Start your app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
