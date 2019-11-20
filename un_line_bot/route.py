import re
from flask import Flask, request, abort
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, ButtonsTemplate, MessageAction, CarouselTemplate, CarouselColumn
)
from un_line_bot import line_bot_api, handler, app, models


user = {}
un_search = {}

@app.route('/')
def index():
    return "hello"

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return ('',204)

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.sender_id
    user_message = event.message.text
    if user_message == "UN Career Today":
        job_list = models.UNDataQuery().search_by_day(today=True)
        for i in job_list:
            line_bot_api.push_message(user_id,TextSendMessage(text=f"{i.title}\n{i.department}\n{i.link}"))
    elif user_message == "My UN Career Search":
        # Setup the customize searching key
        user[user_id] = {}
        buttons_template = personal_search_template()
        line_bot_api.reply_message(event.reply_token, buttons_template)
    elif user_id in user.keys() and re.match("^PS-",user_message) != None:
        user[user_id][user_message] = "Admin-Step1"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="""Please type down keyword you want to setup.
            If there are muti-keywords, pls follow the template 'key1/key2/e=key3'""")
        )
    elif user_message == "admin-user":
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f"{user}"))
    elif "Admin-Step1" in user.get(user_id,{}).values():
        for k, v in user[user_id].items():
            if v == "Admin-Step1":
                category = k
        user[user_id][category]=[i.strip() for i in user_message.split("/")]
        buttons_template = personal_search_template(True)
        line_bot_api.reply_message(event.reply_token, buttons_template)


def personal_search_template(sencond= False):
    _columns=[
        CarouselColumn(
            title='Categories-Job Level',
            text="Please select category that you want to set requirement",
            actions=[
                MessageAction(
                    label="Job Title",
                    text="PS-title",
                ),
                MessageAction(
                    label="Job Level",
                    text="PS-level"
                ),
                MessageAction(
                    label="Location",
                    text="PS-location"
                )
            ]
        ),
        CarouselColumn(
            title="Categories-Department Level",
            text = "Please select category that you want to set requirement",
            actions=[
                MessageAction(
                    label="Job Network",
                    text="PS-job_network"
                ),
                MessageAction(
                    label="Job Family",
                    text="PS-job_family"
                ),
                MessageAction(
                    label="Department",
                    text="PS-department"
                )
            ]
        )
        ]
    if sencond == True:
        _columns.insert(0,
            CarouselColumn(
                title="Settings",
                text = "If you complete the personal seeting, press 'Complete'.",
                actions=[
                    MessageAction(
                        label="Complete",
                        text="CZ-complete"
                    ),
                    MessageAction(
                        label="Show My Setting",
                        text="CZ-showczsetting"
                    ),
                    MessageAction(
                        label="Reset My Setting",
                        text="CZ-reset"
                    )
                ]
            )
        )
    template = TemplateSendMessage(
        alt_text='Personal Search Template',
        template=CarouselTemplate(
        columns = _columns
        )
    )
    return template
