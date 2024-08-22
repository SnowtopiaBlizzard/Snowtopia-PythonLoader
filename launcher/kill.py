import psutil
import logging

logger = logging.getLogger(__name__)

def kill_process_by_name(name):
    """Terminate processes by name."""
    process_found = False

    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == name:
            process_found = True
            try:
                proc.terminate()
                logger.info(f"Process {name} with PID {proc.info['pid']} has been terminated.")
            except psutil.NoSuchProcess:
                logger.warning(f"Process {name} with PID {proc.info['pid']} does not exist.")
            except psutil.AccessDenied:
                logger.error(f"Access denied to terminate process {name} with PID {proc.info['pid']}.")
            except psutil.TimeoutExpired:
                logger.error(f"Terminating process {name} with PID {proc.info['pid']} timed out.")
            except Exception as e:
                logger.exception(f"An error occurred: {e}")
            break

    if not process_found:
        logger.info(f"No process found with name {name}")
