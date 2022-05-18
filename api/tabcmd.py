from tkinter import W
import tableauserverclient as TSC

class tableau_api():
    def __init__(self, server, user, token, pagesize = 1000):
        self.tableau_user = user
        self.tableau_token = token
        self.tableau_server = server
        self.tableau_auth = TSC.PersonalAccessTokenAuth(self.tableau_user, self.tableau_token)
        self.server = TSC.Server(self.tableau_server, use_server_version=True)
        self.pagesize = pagesize
        self.request_options = TSC.RequestOptions(pagesize=self.pagesize)
        self.server.auth.sign_in(self.tableau_auth)
        self.ds_temp_file_path = '/Users/igale/vsCode/tableau-api/template/google_ss.tds'
        self.wb_temp_file_path = '/Users/igale/vsCode/tableau-api/template/google_ss_temp.twb'
        

    def datasource_list(self, search=None):
        ds_list=[]
        server=self.server
        all_datasources = list(TSC.Pager(server.datasources.get, self.request_options))

        for datasource in all_datasources:
            if search is None or search.lower() in datasource.name.lower():
                print(datasource.name)
                ds_list.append([datasource.name, datasource.id])
        return ds_list

    def datasource_download_no_extract(self, filepath):
            server=self.server
            datasource_id=input('\nEnter datasource id: ')
            server.datasources.download(datasource_id, filepath=filepath, include_extract=False, no_extract=None)

    def datasource_download_id_no_extract(self, ds_id, filepath):
                server=self.server
                datasource_id=ds_id
                return server.datasources.download(datasource_id, filepath=filepath, include_extract=False, no_extract=None)

    def users_list(self, search=None):
        users_list =[]
        server=self.server
        all_users = list(TSC.Pager(server.users.get, self.request_options))
        for user in all_users:
            if search is None or search.lower() in user.name.lower():
                users_list.append([user.id, user.name])
        return users_list

    def projects_list(self, search=None):
        projects_list = []
        server = self.server
        all_projects = list(TSC.Pager(server.projects.get, self.request_options))
        for project in all_projects:
            if search is None or search.lower() in project.name.lower():
                #print(project.name)
                projects_list.append([project.name, project.id])
        return projects_list

    def ds_publish(self, project_id):
        print('\nPublishing Datasource...\n') 
        server = self.server
        publish_mode = TSC.Server.PublishMode.Overwrite
        project_id =project_id
        new_datasource = TSC.DatasourceItem(project_id) #, name='sheet_test')
        new_conn_creds = None
        ds_temp_file_path = self.ds_temp_file_path
        return server.datasources.publish(datasource_item=new_datasource, 
                                            file=ds_temp_file_path, 
                                            mode=publish_mode,
                                            connection_credentials=new_conn_creds)#, as_job=True)

    def ds_refresh(self, datasource_id):
        server = self.server
        datasource = datasource_id
        server.datasources.refresh(datasource)

    def wb_publish(self, owner_id, project_id=None, name='igal_test'):
        print('\nPublishing Workbook...\n') 
        if project_id is None:
            self.projects_list(search='defualt')[0][1]
        server = self.server
        publish_mode = TSC.Server.PublishMode.Overwrite
        wb_item = TSC.WorkbookItem(project_id=project_id, name=name)
        wb_temp_file_path = self.wb_temp_file_path
        return server.workbooks.publish(wb_item, wb_temp_file_path, mode=publish_mode,skip_connection_check=True)
        
    def wb_update_owner(self, workbook_id, owner_id):
        print('Updating owner')
        server = self.server
        wb_id = workbook_id
        owner_id = owner_id
        workbook = server.workbooks.get_by_id(wb_id)
        workbook.owner_id = owner_id
        server.workbooks.update(workbook)


