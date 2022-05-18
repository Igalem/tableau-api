class xmlParser():
    def __init__(self, username, filename, cloudlink='///////'):
        self.file_path = '/Users/igale/vsCode/tableau-api/template/google_ss.twb'
        self.file_trg_path = '/Users/igale/vsCode/tableau-api/template/google_ss_temp.twb'
        self.parse_text = "class='cloudfile:googledrive-excel-direct'"
        self.cloudlink = cloudlink
        self.cloudFieldId = self.cloudlink.split('/')[5]
        self.tags = {'cloudFileId' : "'{cloudFieldId}'".format(cloudFieldId=self.cloudFieldId),
            'cloudFileRequestURL' : "'https://www.googleapis.com/drive/v3/files/{cloudFieldId}/export?mimeType=application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'".format(cloudFieldId=self.cloudFieldId),
            'username' : "'{username}'".format(username=username),
            'cloudFileName' : "'{filename}'".format(filename=filename),
            'filename' : "'{filename}'".format(filename=filename)
        }

    def parse(self):
        readfile = open(self.file_path, 'r')
        writefile = open(self.file_trg_path, 'w')
        xmltemp = readfile.readlines()

        for line in xmltemp:
            if self.parse_text in line:
                datasource = line.split(' ')
                ds_temp = []
                for ds in datasource:
                    kv = ds.split('=')
                    if kv[0] in self.tags:
                        kv_temp='='.join([kv[0], self.tags[kv[0]]])
                        ds_temp.append('='.join([kv[0], self.tags[kv[0]]]))
                    else:
                        kv_temp = '='.join(kv)
                        ds_temp.append(kv_temp)
                line_temp = ' '.join(ds_temp)
            else:
                line_temp = line
            writefile.write(line_temp)

        writefile.close()
        readfile.close()

# if __name__ == '__main__':
#     xmlparser = xmlParser(username='igal.emona@skai.io',
#                             filename='f1f1f1.xls',
#                             cloudFieldId='1234567890')
#     xmlparser.parse()