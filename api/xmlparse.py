import os

PROJECT_ROOT = os.path.dirname(os.path.abspath('.'))

class xmlParser():
    def __init__(self, wb_type, username='', filename='', cloudlink='///////', sql_query=''):
        self.wb_type = wb_type
        self.file_path = PROJECT_ROOT + '/template/' + self.wb_type + '.twb'
        self.file_trg_path = PROJECT_ROOT + '/template/' + self.wb_type + '_temp.twb'
        
        self.class_parse = {'google_ss' : "class='cloudfile:googledrive-excel-direct'",
                            'sql_query' : "snowflake"}

        self.cloudlink = cloudlink
        self.cloudFieldId = self.cloudlink.split('/')[5]
        self.sql_query = sql_query.replace(';', '')
        self.tags = {
            'google_ss' : {'cloudFileId' : "'{cloudFieldId}'".format(cloudFieldId=self.cloudFieldId),
                            'cloudFileRequestURL' : "'https://www.googleapis.com/drive/v3/files/{cloudFieldId}/export?mimeType=application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'".format(cloudFieldId=self.cloudFieldId),
                            'username' : "'{username}'".format(username=username),
                            'cloudFileName' : "'{filename}'".format(filename=filename),
                            'filename' : "'{filename}'".format(filename=filename)},
            'sql_query' : {'type' : "'text'>" + self.sql_query,
                            'warehouse' : "'WH_XLARGE_POOL'",
                            'username' : "'TABLEAU_BOT_PROD'"}
        }


    def parse(self):
        print('\nStart parsing WB type:', self.wb_type, '\n')
        readfile = open(self.file_path, 'r')
        writefile = open(self.file_trg_path, 'w')
        xmltemp = readfile.readlines()

        for line in xmltemp:
            if self.class_parse[self.wb_type] in line:
                workbook = line.split(' ')
                if self.wb_type == 'sql_query':
                    startQueryIndex = [i for i,w in enumerate(workbook) if "type='text'" in w]
                    endQueryIndex = '<' + [w for w in workbook if '<' in w][-1].split('<')[-1]
                    if len(startQueryIndex) > 0:
                        del workbook[startQueryIndex[0]:]
                        workbook.append('type=')
                        workbook.append(endQueryIndex)
                wb_temp = []
                for tag in workbook:
                    kv = tag.split('=')
                    wb_tags = self.tags[self.wb_type]
                    if kv[0] in wb_tags:
                        kv_temp='='.join([kv[0], wb_tags[kv[0]]])
                        wb_temp.append(kv_temp)
                    else:
                        kv_temp = '='.join(kv)
                        wb_temp.append(kv_temp)
                line_temp = ' '.join(wb_temp)
            else:
                line_temp = line
            writefile.write(line_temp)

        writefile.close()
        readfile.close()

# if __name__ == '__main__':
#     xmlparser = xmlParser(wb_type='sql_query',
#                             sql_query='Select * from BI_DWH_PROD.DW_DIM_CHANNEL;')
                        
#     xmlparser.parse()