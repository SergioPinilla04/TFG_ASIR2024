import paramiko

def execute_ssh_command(hostname, port, username, key_filepath, command):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, port, username, key_filename=key_filepath)
    
    stdin, stdout, stderr = ssh.exec_command(command)
    result = stdout.read().decode('utf-8')
    error = stderr.read().decode('utf-8')
    
    ssh.close()
    
    if error:
        raise Exception(f"Error ejecutando comando: {error}")
    
    return result
