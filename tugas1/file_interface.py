import os
import json
import base64
from glob import glob


class FileInterface:
    def __init__(self):
        os.chdir('files/')

    def list(self,param=[]):
        try:
            filelist = glob('*.*')
            return dict(status='OK',data=filelist)
        except Exception as e:
            # print(e)
            return dict(status='ERROR',data=str(e))

    def get(self,filename=''):
        if(filename==''):
            return None
        try:
            fp = open(f"{filename}",'rb')
            isifile = base64.b64encode(fp.read()).decode()
            return dict(status='OK',data_namafile=filename,data_file=isifile)
        except Exception as e:
            return dict(status='ERROR',data=str(e))

        
    def upload(self, param):
        try:
            filename = param[0] 
            data = param[1]
            file = open(filename, 'xb')
            file.write(base64.b64decode(data))
            file.close()
        except IndexError:
            return dict(status='ERROR',data ='Parameter tidak valid')
        except FileExistsError:
            return dict(status='ERROR', data = 'File sudah ada')
        return dict(status="OK", data='UPLOAD SUKSES');

    def delete(self,param):
        try:
            filename = param[0]
            os.remove(filename)
        except IndexError:
            return dict(status='ERROR',data='Parameter tidak valid')
        except FileNotFoundError:
            return dict(status='ERROR',data='File tidak ditemukan')
        return dict(status='OK',data="HAPUS SUKSES")

if __name__=='__main__':
    f = FileInterface()
    print(f.list())
    print(f.get('pokijan.jpg'))
