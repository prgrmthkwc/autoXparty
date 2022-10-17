

# text in "00:31:03" format
def time2secs(text):
    
    t = text.strip()
    ts = list(map(int, t.split(':')))

    return ts[0]*3600 + ts[1]*60 + ts[2]