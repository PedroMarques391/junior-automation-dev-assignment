import logging
from datetime import datetime

import pandas as pd

from src.pipeline import Pipeline

logger = logging.getLogger(__name__)

def main():
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_filename = f'logs/execution_{current_time}.log'

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.FileHandler(log_filename),
        ]
    )

    Pipeline.Pipeline()
    
 
if __name__ == '__main__':
    main()