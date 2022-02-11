import tableauserverclient as TSC

class tableau_api():
    def __init__(self):
        self.tableau_user='igalemona'
        self.tableau_token='E3vAQj1ETzOCpRAuYd4xwA==:1xrl66pO62MlP7lS6KrjQoidnHmWWIIY'
        self.tableau_server='https://bi.kenshoo.com'
        self.tableau_auth = TSC.PersonalAccessTokenAuth(self.tableau_user, self.tableau_token)
        self.server = TSC.Server(self.tableau_server, use_server_version=True)
        self.pagesize=1000
        self.request_options = TSC.RequestOptions(pagesize=self.pagesize)
        self.server.auth.sign_in(self.tableau_auth)
        

    def datasource_list(self,like=None):
        tableau_auth=self.tableau_auth
        server=self.server
        #all_datasources, pagination_item = server.datasources.get()
        all_datasources = list(TSC.Pager(server.datasources.get, self.request_options))
        #
        if like is None:
            for datasource in all_datasources:
                print(datasource.name)
        else:
            for datasource in all_datasources:
                if like.lower() in datasource.name.lower():
                    print(datasource.name, '(id:', datasource.id +')')
        #                 
        #server.auth.sign_out()

    def datasource_download_no_extract(self,filepath):
            tableau_auth=self.tableau_auth
            server=self.server
            #datasource_id='0ac5ac8e-517f-4668-a3e4-2fb16aa56614'
            datasource_id=input('Enter datasource id: ')
            server.datasources.download(datasource_id, filepath=filepath, include_extract=False, no_extract=None)

    def users_list(self,like=None):
        tableau_auth=self.tableau_auth
        server=self.server
        all_users = list(TSC.Pager(server.users.get, self.request_options))
        #
        if len(like) == 0:
            for user in all_users:
                print(user.name)
        else:
            for user in all_users:
                if like.lower() in user.name.lower():
                    print(user.name, '  Site role:', user.site_role)
        print('\n')