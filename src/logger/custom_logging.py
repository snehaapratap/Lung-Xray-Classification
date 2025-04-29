from datetime import datetime
import os
import logging

logging_str='[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s'

LOG_FILE = f'{datetime.now().strftime("%m %d %Y %H %M")}.log'

log_path=os.path.join(os.getcwd(),'logs',LOG_FILE)
os.makedirs(log_path,exist_ok=True)


log_filepath=os.path.join(log_path,LOG_FILE)

logging.basicConfig(
    filename=log_filepath,
    level=logging.INFO,
    format=logging_str
)


logger=logging.getLogger(__name__)