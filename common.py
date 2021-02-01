import yaml


"""On this Python file, we load parameters from config, 
    this is a good practice to improve escalability"""
__config = None

def config():
    global __config
    if not __config:
        with open('C:/Users/bisma/OneDrive/Escritorio/Bismarck/web_scraper/config.yaml', mode='r') as f:
            __config = yaml.load(f, Loader=yaml.FullLoader)
    return __config