import psutil

def kill_process_by_name(name):
    # Iterate over all running processes
    for proc in psutil.process_iter(['pid', 'name']):
        # Check if the process name matches
        if proc.info['name'] == name:
            try:
                # Terminate the process
                proc.kill()
                print(f"Process {name} with PID {proc.info['pid']} has been terminated.")
            except psutil.NoSuchProcess:
                print(f"Process {name} with PID {proc.info['pid']} does not exist.")
            except psutil.AccessDenied:
                print(f"Access denied to terminate process {name} with PID {proc.info['pid']}.")
            except Exception as e:
                print(f"An error occurred: {e}")
            break
    else:
        print(f"No process found with name {name}")