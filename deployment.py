
import os
import paramiko
import boto3

# EC2 instance details
EC2_INSTANCE = "i-02774624903721133"
EC2_KEY = "D:\Fullstack Course\Slides\Agile And DevOps\Assignment\backend.pem"
local_file_path="C:\ProgramData\Jenkins\.jenkins\workspace\Backend"
remote_file_path="/app/backend/"

# SSH connection options
SSH_OPTIONS = "-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null"

ec2_client = boto3.client('ec2')

# Get the public IP address of the EC2 instance
response = ec2_client.describe_instances(InstanceIds=[EC2_INSTANCE])
public_ip = response['Reservations'][0]['Instances'][0]['PublicIpAddress']

def copy_to_ec2():
    transport = paramiko.Transport((public_ip, 22))
    private_key = paramiko.RSAKey.from_private_key_file(EC2_KEY)
    transport.connect(username='ec2-user', pkey=private_key)
    sftp = transport.open_sftp()

    # Copy the file to the EC2 instance
    sftp.put(local_file_path, remote_file_path)

    # Close the SFTP session and the transport
    sftp.close()
    transport.close()

# Connect to the EC2 instance and execute commands
def deploy_to_ec2():
    # Create SSH client
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Connect to the EC2 instance
    ssh_client.connect(EC2_INSTANCE, key_filename=EC2_KEY, timeout=10)

    # Change to the app's directory
    command = f"cd {remote_file_path}"
    ssh_client.exec_command(command)

    command = "sh requirement.sh"
    ssh_client.exec_command(command)

    # Close the SSH connection
    ssh_client.close()

# Execute the deployment function
copy_to_ec2()

# Execute the deployment function
deploy_to_ec2()
