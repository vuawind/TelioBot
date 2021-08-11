
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
    #line10 = view["state"]["values"]["block_bank"]["bank_input"]["value"]
    line11 = view["state"]["values"]["block_user_input"]["user_select"]["selected_users"][0]
    line12 = view["state"]["values"]["block_urgent"]['urgent']['selected_options']
    response = client.users_info(user=f"{body['user']['id']}")
    assert(response)
    #profile = response['user']['profile']
    display_name = response['user']['profile']['display_name']
    phone = response['user']['profile']['phone']
    title = response['user']['profile']['title']
    avatar = response['user']['profile']['image_72']
    email = response['user']['profile']['email']
    day=259200
    # Validate the inputs
    # Acknowledge the view_submission event and close the modal
    errors = {}
    date1 = datetime.datetime.strptime(line1, "%Y-%m-%d")
    date2 = datetime.datetime.strptime(line3, "%Y-%m-%d")
    date3 = datetime.datetime.strptime(datetime.datetime.today().strftime('%Y-%m-%d'), "%Y-%m-%d")
    timestamp1 = datetime.datetime.timestamp(date1)
    timestamp2 = datetime.datetime.timestamp(date2)
    timestamp3 = datetime.datetime.timestamp(date3)
    if len(line12) == 0:
        day = 259200
    elif len(line12) == 1:
        day = 0
    if timestamp1 is not None and timestamp1 > timestamp2:
        errors["block_b"] = "Departure date cannot be later than return date"
    if timestamp1 - timestamp3 < day:
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
        if view["state"]["values"]["block_perdiem"]["perdiem_select"]["selected_option"]['value'] == "value-1":
            if len(line12) == 1:
                msg = f":airplane_departure: *Departure:* \n{line1}\n:airplane_arriving: *Arrival:* \n{line3}\n*From:* \n{line2}\n*To:*\n{line4}\n*Vehicle: * {line5}\n*Class: * {line6}\n *ID/Passport number: *\n{line9}\n*Reasons for travel:*\n{line7}\n*Per diem request: * {line8}\n*:warning: Very URGENT Travel Request*"
            else:
                msg = f":airplane_departure: *Departure:* \n{line1}\n:airplane_arriving: *Arrival:* \n{line3}\n*From:* \n{line2}\n*To:*\n{line4}\n*Vehicle: * {line5}\n*Class: * {line6}\n *ID/Passport number: *\n{line9}\n*Reasons for travel:*\n{line7}\n*Per diem request: * {line8}"
        # Save to DB
        if view["state"]["values"]["block_perdiem"]["perdiem_select"]["selected_option"]['value'] == "value-0":
            line10 = view["state"]["values"]["block_bank"]["bank_input"]["value"]
            if len(line12) == 1:
                msg = f":airplane_departure: *Departure:* \n{line1}\n:airplane_arriving: *Arrival:* \n{line3}\n*From:* \n{line2}\n*To:*\n{line4}\n*Vehicle: * {line5}\n*Class: * {line6}\n *ID/Passport number: *\n{line9}\n*Reasons for travel:*\n{line7}\n*Per diem request: * {line8}\n*Bank information: *\n{line10}\n*:warning: Very URGENT Travel Request*"
            else:
                msg = f":airplane_departure: *Departure:* \n{line1}\n:airplane_arriving: *Arrival:* \n{line3}\n*From:* \n{line2}\n*To:*\n{line4}\n*Vehicle: * {line5}\n*Class: * {line6}\n *ID/Passport number: *\n{line9}\n*Reasons for travel:*\n{line7}\n*Per diem request: * {line8}\n*Bank information: *\n{line10}"
    except Exception as e:
        # Handle error
        msg = "There was an error with your submission"

    # Message the user
    try:
        client.chat_postMessage(channel=body['user']['id'], text=f"Bạn đã nộp đơn thành công! :tada:\nĐơn xin đi công tác của bạn đang đợi được duyệt bởi <@{line11}>, xin cảm ơn")
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


@app.action("perdiem_select")
def perdiemyes(body, ack, say, client, view):
    selected_option = body['view']['state']['values']['block_perdiem']['perdiem_select']['selected_option']['value']
    ack()
    # Call views_update with the built-in client
    if selected_option == "value-0":
        client.views_update(
            # Pass the view_id
            view_id=body["view"]["id"],
            # String that represents view state to protect against race conditions
            hash=body["view"]["hash"],
            # View payload with updated blocks
            view=travel_bot.TRAVEL_BLOCK
        )
    if selected_option == "value-1":
        client.views_update(
            # Pass the view_id
            view_id=body["view"]["id"],
            # String that represents view state to protect against race conditions
            hash=body["view"]["hash"],
            # View payload with updated blocks
            view=travel_bot.TRAVEL_BLOCK1
        )

@app.action("extend")
def extend_travel(body, ack, say, client, view):
    client.views_update(
        # Pass the view_id
        view_id=body["view"]["id"],
        # String that represents view state to protect against race conditions
        hash=body["view"]["hash"],
        # View payload with updated blocks
        view=travel_bot.TRAVEL_BLOCK_EXTEND)

@app.action("extend_perdiem_select")
def perdiem_extend(body, ack, say, client, view):
    selected_option = body['view']['state']['values']['block_perdiem_extend']['extend_perdiem_select']['selected_option']['value']
    ack()
    # Call views_update with the built-in client
    if selected_option == "value-0":
        client.views_update(
            # Pass the view_id
            view_id=body["view"]["id"],
            # String that represents view state to protect against race conditions
            hash=body["view"]["hash"],
            # View payload with updated blocks
            view=travel_bot.TRAVEL_BLOCK_EXTEND
        )
    if selected_option == "value-1":
        client.views_update(
            # Pass the view_id
            view_id=body["view"]["id"],
            # String that represents view state to protect against race conditions
            hash=body["view"]["hash"],
            # View payload with updated blocks
            view=travel_bot.TRAVEL_BLOCK_EXTEND1
        )

@app.view("view_extend")
def handle_extend(ack, body, client, view, logger, message, user):
    # Assume there's an input block with `block_c` as the block_id and `dreamy_input`
    line1 = view["state"]["values"]["block_a"]["departure"]["selected_date"]
    line2 = view["state"]["values"]["block_from"]["from_select"]["selected_option"]["text"]["text"]
    line3 = view["state"]["values"]["block_b"]["return"]["selected_date"]
    line4 = view["state"]["values"]["block_return"]["to_select"]["selected_option"]["text"]["text"]
    line5 = view["state"]["values"]["block_vehicle"]["vehicle_select"]["selected_option"]["text"]["text"]
    line6 = view["state"]["values"]["block_class"]["class_select"]["selected_option"]["text"]["text"]
    line7 = view["state"]["values"]["block_d"]["reason_input"]["value"]
    line8 = view["state"]["values"]["block_perdiem_extend"]["extend_perdiem_select"]["selected_option"]["text"]["text"]
    line9 = view["state"]["values"]["block_id"]["input_id"]["value"]
    #line10 = view["state"]["values"]["block_bank"]["bank_input"]["value"]
    line11 = view["state"]["values"]["block_user_input"]["user_select"]["selected_users"][0]
    line12 = view["state"]["values"]["block_invoice"]["input_invoice"]["value"]
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
    timestamp1 = datetime.datetime.timestamp(date1)
    timestamp2 = datetime.datetime.timestamp(date2)
    if timestamp1 is not None and timestamp1 > timestamp2:
        errors["block_a"] = "Departure date cannot be later than return date"
    if len(errors) > 0:
        ack(response_action="errors", errors=errors)
        return
    ack()
    # Do whatever you want with the input data - here we're saving it to a DB
    # then sending the user a verification of their submission

    # Message to send user
    msg = ""
    try:
        if view["state"]["values"]["block_perdiem_extend"]["extend_perdiem_select"]["selected_option"]['value'] == "value-1":
            msg = f":airplane_departure: *Departure:* \n{line1}\n:airplane_arriving: *Arrival:* \n{line3}\n*From:* \n{line2}\n*To:*\n{line4}\n*Vehicle: * {line5}\n*Class: * {line6}\n *ID/Passport number: *\n{line9}\n*Reasons for travel:*\n{line7}\n*Per diem request: * {line8}"
        # Save to DB
        if view["state"]["values"]["block_perdiem_extend"]["extend_perdiem_select"]["selected_option"]['value'] == "value-0":
            line10 = view["state"]["values"]["block_bank"]["bank_input"]["value"]
            msg = f":airplane_departure: *Departure:* \n{line1}\n:airplane_arriving: *Arrival:* \n{line3}\n*From:* \n{line2}\n*To:*\n{line4}\n*Vehicle: * {line5}\n*Class: * {line6}\n *ID/Passport number: *\n{line9}\n*Reasons for travel:*\n{line7}\n*Per diem request: * {line8}\n*Bank information: *\n{line10}"
    except Exception as e:
        # Handle error
        msg = "There was an error with your submission"

    # Message the user
    try:
        client.chat_postMessage(thread_ts=line12,channel=log_channel, blocks=[
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
				"type": "plain_text",
				"text": f"{line12}"
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
					"action_id": "button1x"
				},
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"emoji": True,
						"text": "Deny"
					},
					"style": "danger",
					"action_id": "button2x"
				}
			]
		}
	])
    except e:
        logger.exception(f"Failed to post a message {e}")


@app.action("button1")
def action_button_click1(body, ack, say, client, view, action):
    # Acknowledge the action
    ts=body['message']['ts']
    result = client.conversations_history(channel = log_channel, inclusive=True,latest=ts,limit=1)
    result1 = client.conversations_history(channel = body['container']['channel_id'], inclusive=True,latest=ts,limit=1)
    conversation_history = f"{result1['messages'][0]['blocks'][1]['text']['text']}\n{result1['messages'][0]['blocks'][2]['text']['text']}"
    msg = conversation_history
    ack()
    client.chat_postMessage(channel = body['message']['blocks'][0]['text']['text'], text = f"<@{body['user']['id']}> đã chấp thuận đơn xin công tác của bạn\nĐây là số ts của bạn, hãy lưu lại trong trường hợp bạn muốn kéo dài thời gian công tác:\n *{result['messages'][0]['ts']}*")
    client.chat_update(ts=ts,channel = body['container']['channel_id'], blocks=[
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

@app.action("button1x")
def action_button_click1x(body, ack, say, client, view, action):
    # Acknowledge the action
    ts=body['message']['ts']
    result = client.conversations_replies(channel = log_channel, inclusive=True,latest=ts,ts=body['message']['blocks'][1]['text']['text'],limit=1)
    conversation_history = f"{result['messages'][1]['blocks'][0]['text']['text']}\n{result['messages'][1]['blocks'][1]['text']['text']}"
    msg = conversation_history
    ack()
    client.chat_postMessage(channel = body['message']['blocks'][0]['text']['text'], text = f"<@{body['user']['id']}> đã chấp thuận đơn xin công tác của bạn\nĐây là số ts của bạn, hãy lưu lại trong trường hợp bạn muốn kéo dài thời gian công tác:\n *{result['messages'][0]['ts']}*")
    client.chat_update(ts=ts,channel = body['container']['channel_id'], blocks=[
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

@app.command("/getts")
def getts(body, say, client, ack, command):
    mess=client.chat_getPermalink(channel=log_channel,message_ts=command['text'])
    ack()
    client.chat_postMessage(channel=command['user_id'],text=f"{mess['permalink']}")


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
    result = client.conversations_history(channel = body['container']['channel_id'], inclusive=True,latest=ts,limit=1)
    conversation_history = f"{result['messages'][0]['blocks'][1]['text']['text']}\n{result['messages'][0]['blocks'][2]['text']['text']}"
    msg = conversation_history
    ack()
    client.chat_postMessage(as_user=True,channel = body['message']['blocks'][0]['text']['text'], text = f"<@{body['user']['id']}> đã từ chối đơn xin công tác của bạn")
    client.chat_update(ts=ts, channel = body['container']['channel_id'], blocks=[
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

@app.action("button2x")
def action_button_click2x(body, ack, say, client):
    # Acknowledge the action
    ts=body['message']['ts']
    result = client.conversations_replies(channel = log_channel, inclusive=True,latest=ts,ts=body['message']['blocks'][1]['text']['text'],limit=1)
    conversation_history = f"{result['messages'][1]['blocks'][0]['text']['text']}\n{result['messages'][1]['blocks'][1]['text']['text']}"
    msg = conversation_history
    ack()
    client.chat_postMessage(as_user=True,channel = body['message']['blocks'][0]['text']['text'], text = f"<@{body['user']['id']}> đã từ chối đơn xin công tác của bạn")
    client.chat_update(ts=ts, channel = body['container']['channel_id'], blocks=[
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


@app.message("svxhyy")
def new_comer(body, ack, say, client):
    ack()
    client.chat_postMessage(channel=log_channel, text="svxhyy")

@app.command("/travelreport")
def travelA(body, say, client, ack, command):
    client.chat_postMessage(channel=command['user_id'], text=f"Sau khi điền xong xin hãy nộp cho admin: <@U02030491HU> hoặc <@U020ZHTRWJC>")
    ack()
    if command['text'] == "A":
        client.files_upload(channels=command['user_id'],file="reportA.xlsx",filename='Báo cáo công tác.xlsx',title='Báo cáo công tác')
    if command['text'] == "B":
        client.files_upload(channels=command['user_id'],file="reportB.xlsx",filename='Báo cáo công tác.xlsx',title='Báo cáo công tác')
    if command['text'] == "C":
        client.files_upload(channels=command['user_id'],file="reportC.xlsx",filename='Báo cáo công tác.xlsx',title='Báo cáo công tác')

# Start your app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
