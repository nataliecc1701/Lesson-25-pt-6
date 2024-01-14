"""General Purpose Configuration File Parser v 0.1

By Natalie Chapman on 2024/01/13"""

def configure_app(app):
    """Loads config params from a file of param names and configs separated by whitespace
    sets them into app.config. doesn't work if app.config is not dictionary-like"""
    with open("config.txt") as config:
        for line in config:
            params = line.split()
            # parse string to bools
            if params[1] == "True":
                params[1] = True
            elif params[1] == "False":
                params[1] = False
            
            # apply to app.config
            app.config[params[0]] = params[1]