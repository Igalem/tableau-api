from xmlparse import xmlParser
from tabcmd import tableau_api

username='Dana.Tavori@skai.io'
#username='igal.emona@skai.io'
filename='Zendesk Groups.xlsx'
cloudlink='https://docs.google.com/spreadsheets/d/1-T-aV3abtYHPr377CDNPNvxPXlJvp53q5B_pl06ZnDI/edit#gid=0'

xmlparse=xmlParser(username=username, filename=filename, cloudlink=cloudlink).parse()

tabcmd=tableau_api(server='https://bi.skai.io', 
                    user='igalemona_token', 
                    token = '1O7hDFMIRZ2NL6llUaKNIw==:FFG9ZZCgwuoosDZMWN2SrRlg2KK0jRBN')

project_name, project_id = tabcmd.projects_list(search='external data')[0]

owner_id, owner_name = tabcmd.users_list(search=username.lower())[0]
print(owner_id, owner_name)

workbook_id = tabcmd.wb_publish(owner_id=owner_id, project_id=project_id, name='xxxx_test').id

tabcmd.wb_update_owner(workbook_id=workbook_id, owner_id=owner_id)