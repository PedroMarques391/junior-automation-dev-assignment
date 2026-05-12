import logging
from datetime import datetime

from src.pipeline import Pipeline
from src.reporter import Reporter

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
    pipeline = Pipeline(logger)
    pipeline.run()
    
 
if __name__ == '__main__':
    main() 