from tabcmd import tableau_api

tabcmd=tableau_api(server='https://bi.skai.io', 
                   user='igalemona_token', 
                   token = '1O7hDFMIRZ2NL6llUaKNIw==:FFG9ZZCgwuoosDZMWN2SrRlg2KK0jRBN')

#project_name, project_id = tabcmd.projects_list(search='default')[0]
#print(project_name,project_id) #4df3d008-00c5-40fe-8aa2-53226c9693c7

tabcmd.wb_publish()