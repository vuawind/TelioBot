
import os
from time import time
import datetime
from slack_bolt import App, Ack
from slack import WebClient
from travel import travel_bot
from hrwelcome import welcome
from hranswer import *

app = App(
    signing_secret = os.environ.get("SLACK_EVENTS_TOKEN"),

# Initialize a Web API client
    token=os.environ.get("SLACK_TOKEN")
)

log_channel='C0252EMRTS7'
admin_channel='C024Z67LNDB'
bot_channel='D024MFB2B1D'
hr_channel='C025751TS0P'

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
    date1 = datetime.datetime.strptime(line1, "%Y-%m-%d")
    date2 = datetime.datetime.strptime(line3, "%Y-%m-%d")
    date3 = datetime.datetime.strptime(datetime.datetime.today().strftime('%Y-%m-%d'), "%Y-%m-%d")
    timestamp1 = datetime.datetime.timestamp(date1)
    timestamp2 = datetime.datetime.timestamp(date2)
    timestamp3 = datetime.datetime.timestamp(date3)
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
        client.chat_postMessage(channel=log_channel, blocks=[
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
        client.chat_postMessage(channel=line11, blocks=[
		{
			"type": "section",
			"text": {
				"type": "plain_text",
				"text": f"{body['user']['id']}"
			}
		},
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

@app.action("button1")
def action_button_click1(body, ack, say, client, view):
    # Acknowledge the action
    ts=body['message']['ts']
    result = client.conversations_history(channel = log_channel, inclusive=True,latest=ts,limit=1)
    conversation_history = f"{result['messages'][0]['blocks'][0]['text']['text']}\n{result['messages'][0]['blocks'][1]['text']['text']}"
    msg = conversation_history
    ack()
    client.chat_postMessage(channel = body['message']['blocks'][0]['text']['text'], text = f"<@{body['user']['id']}> approved")
    client.chat_update(ts=ts,channel = bot_channel, blocks=[
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
				"text": f":white_check_mark: You have approved this request"
			}
		}
	])
    client.chat_postMessage(channel = admin_channel, blocks=[
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": f"Line manager *<@{body['user']['username']}>* approved this travel plan"
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
    result = client.conversations_history(channel = admin_channel, inclusive=True,latest=ts,limit=1)
    conversation_history = f"{result['messages'][0]['blocks'][0]['text']['text']}\n{result['messages'][0]['blocks'][1]['text']['text']}"
    msg = conversation_history
    ack()
    client.chat_update(ts=ts, channel = admin_channel, blocks=[
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": f"You have finished booking for this travel plan"
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
    line11 = view["state"]["values"]["block_l_input"]["flight_ticket"]["value"]
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
        msg = f"Hello *{profile}*, this is your travel information:\n*Vehicle/Phương tiện:* {line2}\n*Vehicle's number/License plate(Số xe):*\n{line3}\n*Driver's name/Tên người lái:* {line4}\n*Diver's phone number/sđt người lái: * {line5}\n*Hotel/Khách sạn: * {line6}\n *Hotel's location/Địa điểm: * {line7}\n*Hotel's booking number/số booking khách sạn:*\n{line8}\n*Flight ticket/Vé máy bay:*\n {line11}\n*Boarding pass (if travel by plane)/Thẻ máy bay: * \n{line9}\n*Note/Ghi chú:*\n{line10}"
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
    ts=body['message']['ts']
    result = client.conversations_history(channel = log_channel, inclusive=True,latest=ts,limit=1)
    conversation_history = f"{result['messages'][0]['blocks'][0]['text']['text']}\n{result['messages'][0]['blocks'][1]['text']['text']}"
    msg = conversation_history
    ack()
    client.chat_postMessage(as_user=True,channel = body['message']['blocks'][0]['text']['text'], text = f"<@{body['user']['id']}> denied your travel plan")
    client.chat_update(ts=ts, channel = bot_channel, blocks=[
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
				"text": f":negative_squared_cross_mark: You have denied this request"
			}
		}
	])

@app.message("print")
def new_comer(body, ack, say, client):
    ack()
    client.chat_postMessage(channel=log_channel, blocks=welcome.WELCOME_BLOCK)
    #response = client.team_accessLogs(team_id=)

@app.event("team_join")
def ask_for_introduction(event, say, client, body):
    tomorrow = datetime.datetime.today() + datetime.timedelta(days=7)
    scheduled_time = datetime.time(hour=9, minute=30, second=10)
    schedule_timestamp = datetime.datetime.combine(tomorrow, scheduled_time).strftime('%s')
    user_id = event["user"]['id']
    text2 = f"🎉 Xin chào <@{user_id}>, Bạn có câu hỏi về chế độ, chính sách, thủ tục nhân sự? Hãy hỏi với Sophie bằng cách bấm vào mục liên quan bên dưới nhé!"
    say(text=text2, channel=user_id)
    client.chat_postMessage(channel=user_id, blocks=welcome.WELCOME_BLOCK)
    client.chat_scheduleMessage(channel=user_id,text=f"Hello <@{body['user']['id']}>", blocks=welcome.WELCOME_BLOCK, post_at=schedule_timestamp)

@app.shortcut("sophie")
def sophie(event, say, ack, client,shortcut, body):
    ack()
    client.chat_postMessage(channel=shortcut['user']['id'], text=f":hello-there: Xin chào <@{body['user']['id']}>, Tôi là Sophie - HR Chatbot. Bạn có câu hỏi nào cho Sophie - Hãy bấm vào mục liên quan bên dưới nhé!")
    client.chat_postMessage(channel=shortcut['user']['id'], blocks=welcome.WELCOME_BLOCK)

@app.action("onboard_id")
def onboard(event, say, ack, client,body):
    ack()
    client.chat_postMessage(channel=body['user']['id'], blocks=welcome.BLOCK_ONBOARD)

@app.action("quitjob_id")
def quit(event, say, ack, client,body):
    ack()
    client.chat_postMessage(channel=body['user']['id'], blocks=welcome.BLOCK_QUIT)
    
@app.action("move_id")
def move(event, say, ack, client,body):
    ack()
    client.chat_postMessage(channel=body['user']['id'], blocks=welcome.BLOCK_MOVE)

@app.action("insurance_id")
def insurance(event, say, ack, client,body):
    ack()
    client.chat_postMessage(channel=body['user']['id'], blocks=welcome.BLOCK_INSURANCE)

@app.action("tax_id")
def tax(event, say, ack, client,body):
    ack()
    client.chat_postMessage(channel=body['user']['id'], blocks=welcome.BLOCK_TAX)

@app.action("salary_id")
def salary(event, say, ack, client,body):
    ack()
    client.chat_postMessage(channel=body['user']['id'], blocks=welcome.BLOCK_SALARY)

@app.action("work_id")
def work(event, say, ack, client,body):
    ack()
    client.chat_postMessage(channel=body['user']['id'], blocks=welcome.BLOCK_WORK)

@app.action("other_id")
def other(event, say, ack, client,body):
    ack()
    client.chat_postMessage(channel=body['user']['id'], blocks=welcome.BLOCK_OTHER)

@app.action("onboard_select")
def onboard_choice(event, say, ack, client,body,action):
    selected_option = body['state']['values']['block_a']['onboard_select']['selected_option']['value']
    ack()
    if selected_option == 'value-0':
        client.chat_postMessage(channel=body['user']['id'], text=onboard_answer.ans1)
    if selected_option == 'value-1':
        client.chat_postMessage(channel=body['user']['id'], text=onboard_answer.ans2)
    if selected_option == 'value-2':
        client.chat_postMessage(channel=body['user']['id'], text=onboard_answer.ans3)
    if selected_option == 'value-3':
        client.chat_postMessage(channel=body['user']['id'], text=onboard_answer.ans4)
    if selected_option == 'value-4':
        client.chat_postMessage(channel=body['user']['id'], text=onboard_answer.ans5)
    if selected_option == 'value-5':
        client.chat_postMessage(channel=body['user']['id'], text=onboard_answer.ans6)
    if selected_option == 'value-6':
        client.chat_postMessage(channel=body['user']['id'], text=onboard_answer.ans7)
    if selected_option == 'value-7':
        client.chat_postMessage(channel=body['user']['id'], text=onboard_answer.ans8)

@app.action("quit_select")
def quit_choice(event, say, ack, client,body,action):
    selected_option = body['state']['values']['block_b']['quit_select']['selected_option']['value']
    ack()
    if selected_option == 'value-0':
        client.chat_postMessage(channel=body['user']['id'], text=quit_answer.ans1)
    if selected_option == 'value-1':
        client.chat_postMessage(channel=body['user']['id'], text=quit_answer.ans2)
    if selected_option == 'value-2':
        client.chat_postMessage(channel=body['user']['id'], text=quit_answer.ans3)
    if selected_option == 'value-3':
        client.chat_postMessage(channel=body['user']['id'], text=quit_answer.ans4)
    if selected_option == 'value-4':
        client.chat_postMessage(channel=body['user']['id'], text=quit_answer.ans5)

@app.action("move_select")
def move_choice(event, say, ack, client,body,action):
    selected_option = body['state']['values']['block_c']['move_select']['selected_option']['value']
    ack()
    if selected_option == 'value-0':
        client.chat_postMessage(channel=body['user']['id'], text=move_answer.ans1)
    if selected_option == 'value-1':
        client.chat_postMessage(channel=body['user']['id'], text=move_answer.ans2)
    if selected_option == 'value-2':
        client.chat_postMessage(channel=body['user']['id'], text=move_answer.ans3)

@app.action("insurance_select")
def insurance_choice(event, say, ack, client,body,action):
    selected_option = body['state']['values']['block_d']['insurance_select']['selected_option']['value']
    ack()
    if selected_option == 'value-0':
        client.chat_postMessage(channel=body['user']['id'], text=insurance_answer.ans1)
    if selected_option == 'value-1':
        client.chat_postMessage(channel=body['user']['id'], text=insurance_answer.ans2)
    if selected_option == 'value-2':
        client.chat_postMessage(channel=body['user']['id'], text=insurance_answer.ans3)
    if selected_option == 'value-3':
        client.chat_postMessage(channel=body['user']['id'], text=insurance_answer.ans4)
    if selected_option == 'value-4':
        client.chat_postMessage(channel=body['user']['id'], text=insurance_answer.ans5)
    if selected_option == 'value-5':
        client.chat_postMessage(channel=body['user']['id'], text=insurance_answer.ans6)
    if selected_option == 'value-6':
        client.chat_postMessage(channel=body['user']['id'], text=insurance_answer.ans7)
    if selected_option == 'value-7':
        client.chat_postMessage(channel=body['user']['id'], text=insurance_answer.ans8)
    if selected_option == 'value-8':
        client.chat_postMessage(channel=body['user']['id'], text=insurance_answer.ans9)

@app.action("tax_select")
def tax_choice(event, say, ack, client,body,action):
    selected_option = body['state']['values']['block_e']['tax_select']['selected_option']['value']
    ack()
    if selected_option == 'value-0':
        client.chat_postMessage(channel=body['user']['id'], text=tax_answer.ans1)
    if selected_option == 'value-1':
        client.chat_postMessage(channel=body['user']['id'], text=tax_answer.ans2)
    if selected_option == 'value-2':
        client.chat_postMessage(channel=body['user']['id'], text=tax_answer.ans3)
    if selected_option == 'value-3':
        client.chat_postMessage(channel=body['user']['id'], text=tax_answer.ans4)
    if selected_option == 'value-4':
        client.chat_postMessage(channel=body['user']['id'], text=tax_answer.ans5)
    if selected_option == 'value-5':
        client.chat_postMessage(channel=body['user']['id'], text=tax_answer.ans6)

@app.action("salary_select")
def salary_choice(event, say, ack, client,body,action):
    selected_option = body['state']['values']['block_f']['salary_select']['selected_option']['value']
    ack()
    if selected_option == 'value-0':
        client.chat_postMessage(channel=body['user']['id'], text=salary_answer.ans1)
    if selected_option == 'value-1':
        client.chat_postMessage(channel=body['user']['id'], text=salary_answer.ans2)
    if selected_option == 'value-2':
        client.chat_postMessage(channel=body['user']['id'], text=salary_answer.ans3)
    if selected_option == 'value-3':
        client.chat_postMessage(channel=body['user']['id'], text=salary_answer.ans4)
    if selected_option == 'value-4':
        client.chat_postMessage(channel=body['user']['id'], text=salary_answer.ans5)
    if selected_option == 'value-5':
        client.chat_postMessage(channel=body['user']['id'], text=salary_answer.ans6)
    if selected_option == 'value-6':
        client.chat_postMessage(channel=body['user']['id'], text=salary_answer.ans7)
    if selected_option == 'value-7':
        client.chat_postMessage(channel=body['user']['id'], text=salary_answer.ans8)
    if selected_option == 'value-8':
        client.chat_postMessage(channel=body['user']['id'], text=salary_answer.ans9)
    if selected_option == 'value-9':
        client.chat_postMessage(channel=body['user']['id'], text=salary_answer.ans10)
    if selected_option == 'value-10':
        client.chat_postMessage(channel=body['user']['id'], text=salary_answer.ans11)
    if selected_option == 'value-11':
        client.chat_postMessage(channel=body['user']['id'], text=salary_answer.ans12)

@app.action("work_select")
def work_choice(event, say, ack, client,body,action):
    selected_option = body['state']['values']['block_g']['work_select']['selected_option']['value']
    ack()
    if selected_option == 'value-0':
        client.chat_postMessage(channel=body['user']['id'], text=work_answer.ans1)
    if selected_option == 'value-1':
        client.chat_postMessage(channel=body['user']['id'], text=work_answer.ans2)
    if selected_option == 'value-2':
        client.chat_postMessage(channel=body['user']['id'], text=work_answer.ans3)

@app.action("submit")
def other_text(event, say, ack, client,body,action,button):
    text = body['state']['values']['block_h']['other_input']['value']
    ack()
    client.chat_postMessage(channel = hr_channel, text = f"you have a new question from <@{body['user']['id']}>:\n{text}")

@app.action("back")
def back(event, say, ack, client,body,action):
    ack()
    client.chat_postMessage(channel = body['user']['id'], blocks=welcome.WELCOME_BLOCK)

# Start your app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
