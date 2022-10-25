import json
import os

# text in "00:31:03" format
import logging


def time2secs(text):
    t = text.strip()
    # print("text stripped:", t)
    ts = list(map(int, t.split(':')))

    if len(ts) == 2:
        return ts[0] * 60 + ts[1]
    elif len(ts) == 3:
        return ts[0] * 3600 + ts[1] * 60 + ts[2]

    return -1


def get_configs(cfg_file_name):
    if not os.path.isfile(cfg_file_name):
        logging.error("failed to load file:", cfg_file_name)
        return None

    with open(cfg_file_name, 'r') as cfg:
        data = json.load(cfg)
        cfg.close()
        return data


####### with many thanks to the author【Greenstick】
## get progress_bar() code from : 
# https://stackoverflow.com/questions/3173320/text-progress-bar-in-terminal-with-block-characters
####### with many thanks to the author【Greenstick】, great job!!
def progress_bar(iterable, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iterable    - Required  : iterable object (Iterable)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    total = len(iterable)

    # Progress Bar Printing Function
    def printProgressBar(iteration):
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)

    # Initial Call
    printProgressBar(0)
    # Update Progress Bar
    for i, item in enumerate(iterable):
        yield item
        printProgressBar(i + 1)
    # Print New Line on Complete
    print()


####### with many thanks to the author 【aviraldg】
## get progress_bar() code from : 
# https://stackoverflow.com/questions/3173320/text-progress-bar-in-terminal-with-block-characters
####### with many thanks to the author 【aviraldg】, great job!!
def update_progress(workdone):
    print("\r学习进度: [{0:50s}] {1:.1f}% 完成度".format('#' * int(workdone * 50), workdone * 100), end="", flush=True)
