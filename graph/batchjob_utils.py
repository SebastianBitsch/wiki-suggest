import sys

def log_message(message : str, file_path : str = None, console_log : bool = False):
    #Log message to file, append if file exists, create if it does not
    if file_path:
        with open(file_path, "a+") as file:
            file.write(message + "\n")
    
    if console_log:
        print(message)
    
            

# Get memory usage of a variable in bytes, KB, MB, GB  
def memory_usage_of(variable : any, logging_message_id : str):
    if type(variable) == list:
        mem = sum([sys.getsizeof(item) for item in variable])
    elif type(variable) == dict:
        mem = sum([sys.getsizeof(key) + sys.getsizeof(value) for key, value in variable.items()])
    elif type(variable) == int: # If you pass in an integer, it will just format the log message
        mem = variable
    else:
        mem = sys.getsizeof(variable)
    mem_log = f"{mem:>12.0f} B, {mem/1024:>9.0f} KB, {mem/(1024**2):>10.1f} MB, {mem/(1024**3):>5.2f} GB"
    log_message = f"Memory usage of {logging_message_id}: \n{mem_log}"
    
    return mem, log_message