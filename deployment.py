import paramiko
import boto3

# EC2 instance details
EC2_INSTANCE = "i-02774624903721133"
private_key_path = 'C:\ProgramData\Jenkins\.jenkins\workspace\\access.pem'
local_file_path ='C:\ProgramData\Jenkins\.jenkins\workspace\Backend'
remote_file_path ='/app/backend/'
region = 'ap-south-1'
access_key = 'AKIARVVH7RKIQ6JRRTDW'
secret_key = '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'

# SSH connection options
#SSH_OPTIONS = "-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null"

session = boto3.Session(
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
    region_name=region
)

#ec2_client = boto3.client('ec2', region_name='ap-south-1')
ec2_client = session.client('ec2')
# Get the public IP address of the EC2 instance
response = ec2_client.describe_instances(InstanceIds=[EC2_INSTANCE])
public_ip = response['Reservations'][0]['Instances'][0]['PublicIpAddress']

def copy_to_ec2(ssh):

    # Create an SFTP client using the SSH connection
    sftp = ssh.open_sftp()

    # Copy the file to the EC2 instance
    sftp.put(local_file_path, remote_file_path)

    # Close the SFTP session, SSH connection, and the transport
    sftp.close()
    

# Connect to the EC2 instance and execute commands
def deploy_to_ec2(ssh_client):
    # Change to the app's directory
    command = f"cd {remote_file_path}"
    ssh_client.exec_command(command)

    command = "sh requirement.sh"
    ssh_client.exec_command(command)

    # Close the SSH connection
    ssh_client.close()


ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# Connect to the EC2 instance
private_key = paramiko.RSAKey.from_private_key_file(private_key_path)
ssh.connect(public_ip, username='ec2-user', pkey=private_key)
# Execute the deployment function
copy_to_ec2(ssh)

# Execute the deployment function
deploy_to_ec2(ssh)
ssh.close()