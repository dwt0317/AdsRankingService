from hdfs.client import Client
import pandas as pd

def list2dict(mylist):
    myDict = {}
    i = 0
    for v in mylist:
        myDict[v] = i
        i += 1
    return myDict


# read log from hdfs
def read(dir_path, header):
    client = Client("http://127.0.0.1:50070")
    log_data = []
    for date_dir in client.list(dir_path):
        for log_file in client.list(dir_path+'/'+date_dir):
            with client.read(dir_path+'/'+date_dir+'/'+log_file) as fs:
                for line in fs:
                    row = line.strip().split('&')
                    if row != ['']:
                        tmp = []
                        for field in row:
                            tmp.append(field.split('=')[1])
                        log_data.append(tmp)
    return pd.DataFrame(log_data, columns=header)


# hash trick to represent id feature
def hash_id(id, hash_size):
    return hash(id) % hash_size
