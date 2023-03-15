import slack
import os
import ssl
from flask import Flask
from slackeventsapi import SlackEventAdapter
from api.xmlparse import xmlParser
from api.tabcmd import tableau_api
import calendar
from datetime import datetime, timedelta

app = Flask(__name__)

tableau_dns = 'http://ip-00-0-0-0.ec2.internal'
tableau_domain = 'https://xxxxxxxxx.xxx.xxx'
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

client = slack.WebClient(token=os.environ.get('SLACK_TOKEN'), ssl=ssl_context)
slack_events_adapter = SlackEventAdapter(os.environ.get('SLACK_EVENTS_TOKEN'), "/slack/events", app)
tableau_token_user = os.environ.get('TABLEAU_TOKEN_USER')
tableau_token_pwd = os.environ.get('TABLEAU_TOKEN_PWD')

BOT_ID = client.api_call("auth.test").get('user_id')
MESSAGE_TIME_DELTA = 3


def publish_wb(username, user_id, tableau_username, channel_id, wb_type='', wb_name=''):
    try:
        tabcmd=tableau_api(server=tableau_domain, 
                    user=tableau_token_user, 
                    token = tableau_token_pwd,
                    wb_type=wb_type)
    except:
        client.chat_postMessage(channel=channel_id, text='Hi <@{user_id}>,\n\
Data Bot was unable to connect to Tableau Server.\nPlease contact the BI Team (_biteam@kenshoo.com) (!!!!) :alert:'.format(user_id=user_id))
        print('(!!!!) Unable to connect to Tableau Server (!!!!)')
        return

    project_name, project_id = tabcmd.projects_list(search='external data')[0]
    owner_id, owner_name = tabcmd.users_list(search=tableau_username.lower())[0]
    print('====== Tableau Owner ID >', owner_id, owner_name)

    client.chat_postMessage(channel=channel_id, text=':tableau: Publishing workbook to Tableau Server...')

    if wb_name =='' or wb_name is None:
        workbook_name = 'bot_' + str(username) + '_' + str(datetime.now().strftime("%Y%m%d"))
    elif 'bot_' in wb_name:
        workbook_name = wb_name
    else:
        workbook_name = 'bot_' + wb_name

    workbook_id = tabcmd.wb_publish(owner_id=owner_id, project_id=project_id, name=workbook_name).id

    tabcmd.wb_update_owner(workbook_id=workbook_id, owner_id=owner_id)

    client.chat_postMessage(channel=channel_id, text=':tableau: WB published!')

    wb_id, wb_name, wb_webpage_url = tabcmd.wbs_list(search=workbook_name)[0]
    workbook_url = wb_webpage_url.replace(tableau_dns, tableau_domain)

    client.chat_postMessage(channel=channel_id, text='Hi <@{user_id}>, your workbook is ready :checkmark-so:, please follow the link below:\
            \n{workbook_url}'.format(user_id=user_id, workbook_url=workbook_url))
    user_id = text = ''

@slack_events_adapter.on('message')
def message(payload):
    
    event = payload.get('event', {})
    text=event.get("text")
    channel_id=event.get("channel")
    user_id = event.get("user")
    user = client.users_info(user=user_id).get('user')
    username = user.get('real_name')
    tableau_username = email = user.get('profile').get('email')
    message_utc = payload.get('event_time')
    now = datetime.utcnow()
    rounded = now - timedelta(seconds=now.second %5 + MESSAGE_TIME_DELTA,microseconds=now.microsecond)
    current_utc_time = calendar.timegm(rounded.utctimetuple())

    if text.count('name=') > 0:
        wb_name = text.split('name=')[1]
    else:
            wb_name = None

    # ## Debug:
    #print('\n--------------------->', text, user_id, username)
    # print('[user_id]', user_id, '[BOT_id]' ,BOT_ID)
    # print('[message utc]', message_utc, '[current utc]', current_utc_time, '\n')
    #print(payload, '\n')

    if (BOT_ID != user_id) and (message_utc >= current_utc_time):
        if 'upload ss' in text.lower():
            wb_type = 'google_ss'
            split_str = 'https://docs.google.com/spreadsheets'
            upload_text = text.split(split_str)

            if len(upload_text) < 2:
                client.chat_postMessage(channel=channel_id, text='Hi <@{user_id}> Spreadsheet URL not provided, please use the following syntax:\
                \n"upload ss" [google spreadsheet url]"'.format(user_id=user_id))
                
            elif len(upload_text) > 1:
                cloudlink = split_str + upload_text[1][:-1:]

                xmlParser(wb_type=wb_type, username=tableau_username, cloudlink=cloudlink).parse()

                publish_wb(username=username, 
                            user_id=user_id, 
                            tableau_username=tableau_username, 
                            channel_id=channel_id,
                            wb_type=wb_type,
                            wb_name=wb_name)

        elif 'help' in text.lower():
            client.chat_postMessage(channel=channel_id, text=':robot_face: Hi <@{user_id}>, please use the following syntax:\
                \n"upload ss" [google spreadsheet url]\
                \n"upload ss" [google spreadsheet url] name=[workbook name]\
                \n"upload sql" [sql query];\
                \n"upload sql" [sql query]; name=[workbook name]'.format(user_id=user_id))
        
        elif 'upload sql' in text.lower():
            wb_type = 'sql_query'
            split_str = 'upload sql '
            upload_text = text.split(split_str)[1]

            if 'select' not in upload_text.lower() or ';' not in upload_text.lower():
                client.chat_postMessage(channel=channel_id, text='Hi <@{user_id}> custom SQL is not valid, please use the following syntax:\
                \n"upload sql" [sql query];'.format(user_id=user_id))

            elif 'select' in upload_text.lower() and ';' in upload_text:

                sql_query = upload_text.split(';')[0]
                print('-------------->', sql_query)
                xmlParser(wb_type=wb_type,  username=tableau_username, sql_query=sql_query).parse()

                # print('username=',username, 
                #             '\nuser_id=',user_id, 
                #             '\ntableau_username=',tableau_username, 
                #             '\nchannel_id=',channel_id,
                #             '\nwb_type=',wb_type,
                #             '\nwb_name=',wb_name)
                
                publish_wb(username=username, 
                            user_id=user_id, 
                            tableau_username=tableau_username, 
                            channel_id=channel_id,
                            wb_type=wb_type,
                            wb_name=wb_name)
        elif 'clear' in text.lower():
            client.chat_postMessage(channel=channel_id, text='.\n'*20)
        else:
            client.chat_postMessage(channel=channel_id, text='This is not a valid option, use "help" for more info')
                  

if __name__ == "__main__":
        app.run(debug=True, port=8000)