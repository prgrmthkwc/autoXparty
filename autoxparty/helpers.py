import json


# text in "00:31:03" format
def time2secs(text):
    t = text.strip()
    # print("text stripped:", t)
    ts = list(map(int, t.split(':')))

    if len(ts) == 2 :
        return ts[0]*60 + ts[1]
    elif len(ts) == 3:
        return ts[0]*3600 + ts[1]*60 + ts[2]
    
    return -1

def get_configs(cfg_file_name):
    with open(cfg_file_name, 'r') as cfg:
        data = json.load(cfg)
        cfg.close()
        return data