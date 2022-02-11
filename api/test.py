from tabcmd import tableau_api

filepath='tmp/'

search=input('\nSearch for: ')
print('\n')

tabcmd=tableau_api()
#tabcmd.datasource_list(search)
#tabcmd.users_list(search)

tabcmd.datasource_download_no_extract(filepath=filepath)