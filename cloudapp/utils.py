import paramiko
import pysftp

def execute_ssh_commands(hostname, port, username, key_filepath, commands):
    key = paramiko.RSAKey.from_private_key_file(key_filepath)
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname, port, username, pkey=key)
    
    for command in commands:
        print(f"Executing command: {command}")
        stdin, stdout, stderr = client.exec_command(command)
        exit_status = stdout.channel.recv_exit_status()
        if exit_status != 0:
            error_message = stderr.read().decode()
            print(f"Error executing command: {command}\n{error_message}")
            raise Exception(f"Command '{command}' failed with exit status {exit_status}\n{error_message}")

    client.close()

def sftp_upload_file(hostname, port, username, password, local_path, remote_path):
    try:
        with pysftp.Connection(hostname, username=username, password=password) as sftp:
            sftp.makedirs(remote_path.rsplit('/', 1)[0])  # Create directories if they do not exist
            sftp.put(local_path, remote_path)
    except Exception as e:
        print(f"Failed to upload file via SFTP: {e}")
        raise
