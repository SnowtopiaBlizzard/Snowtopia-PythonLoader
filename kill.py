import psutil

def kill_process_by_name(name):
    """Terminate processes by name.

    Args:
        name (str): The name of the process to terminate.
    """
    # Flag to check if process was found
    process_found = False

    # Iterate over all running processes
    for proc in psutil.process_iter(['pid', 'name']):
        # Check if the process name matches
        if proc.info['name'] == name:
            process_found = True
            try:
                # Terminate the process
                proc.terminate()
                print(f"Process {name} with PID {proc.info['pid']} has been terminated.")
            except psutil.NoSuchProcess:
                print(f"Process {name} with PID {proc.info['pid']} does not exist.")
            except psutil.AccessDenied:
                print(f"Access denied to terminate process {name} with PID {proc.info['pid']}.")
            except psutil.TimeoutExpired:
                print(f"Terminating process {name} with PID {proc.info['pid']} timed out.")
            except Exception as e:
                print(f"An error occurred: {e}")
            break
    
    # Inform user if no process was found
    if not process_found:
        print(f"No process found with name {name}")

