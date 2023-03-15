from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
import paramiko
import re
from datetime import datetime
import os


app = FastAPI()

VAR_HOSTNAME = os.getenv('FAST_HOSTNAME')
VAR_USERNAME = os.getenv('FAST_USERNAME')
VAR_PASSWORD = os.getenv('FAST_PASSWORD')
VAR_PLAYERS = os.getenv('FAST_PLAYERS').split(", ")
JSON_INPUT = {"Users": {}, "Server": "", "ServerDate": "", "ServerVersion": ""}
JSON_OUTPUT = json.loads(json.dumps(JSON_INPUT))


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_minecraft_data():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=VAR_HOSTNAME, username=VAR_USERNAME, password=VAR_PASSWORD)
    stdin, stdout, stderr = ssh.exec_command('cat minecraft_serwer_63/output.txt')
    output = stdout.read().decode('utf-8')
    ssh.close()
    return output


def get_state(minecraft_user, output):
    results_conn = []
    results_disconn = []
    for line in output.split('\n'):
        match = re.search(f"Player connected: {minecraft_user}", line)
        match2 = re.search(f"Player disconnected: {minecraft_user}", line)
        if match:
            results_conn.append(line.strip())
        elif match2:
            results_disconn.append(line.strip())
    if len(results_conn) > len(results_disconn):
        state = "Online"
    else:
        state = "Offline"
    return state

def get_disconn_date(minecraft_user,output):
    results_conn = []
    results_disconn = []
    last_in = ''
    for line in output.split('\n'):
        match = re.search(f"Player connected: {minecraft_user}", line)
        match2 = re.search(f"Player disconnected: {minecraft_user}", line)
        if match:
            results_conn.append(line.strip())
        elif match2:
            results_disconn.append(line.strip())
    if len(results_conn) > len(results_disconn):
        last_in = "Teraz"
    else:
        for result in reversed(results_disconn):
            if result:
                last_result = result
                timestamp_match = re.search(r"^\[(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2})", last_result)
                if timestamp_match:
                    year, month, day, hour, minute, second = map(int, timestamp_match.groups())
                    timestamp = datetime(year, month, day, hour, minute, second)
                    last_in = str(timestamp).replace('T', ' ')
                    break
                break
    return last_in



@app.get("/avaible")
async def get_availability():
    output = get_minecraft_data()
    for minecraft_user in VAR_PLAYERS:
        state = get_state(minecraft_user, output)
        last_in = get_disconn_date(minecraft_user, output)
        JSON_OUTPUT["Users"].setdefault(minecraft_user, {})
        JSON_OUTPUT["Users"][minecraft_user]["state"] = state
        JSON_OUTPUT["Users"][minecraft_user]["last_in"] = last_in
    for line in output.split('\n'):
        match = re.search("Crash", line)
        if match:
            JSON_OUTPUT["Server"] = "Offline"
            break
    else:
        JSON_OUTPUT["Server"] = "Online"

    for line in output.split('\n'):
        match = re.search("Version", line)
        if match:
            version_line = line.strip()
            version_match = re.search(r"Version (\d+\.\d+\.\d+\.\d+)", version_line)
            if version_match:
                version = version_match.group(1)
                timestamp_match = re.search(r"^\[(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2})", version_line)
                if timestamp_match:
                    year, month, day, hour, minute, second = map(int, timestamp_match.groups())
                    timestamp = datetime(year, month, day, hour, minute, second)
                    JSON_OUTPUT["ServerDate"] = timestamp
                    JSON_OUTPUT["ServerVersion"] = version
                    break
    return JSON_OUTPUT

@app.post("/day")
async def post_minecraft_day():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=VAR_HOSTNAME, username=VAR_USERNAME, password=VAR_PASSWORD)
    stdin, stdout, stderr = ssh.exec_command('screen -r minecraft', get_pty=True)
    stdin.write('time set day\n')
    stdin.write('\x01')  # Ctrl+A
    stdin.write('d')     # d
    output = stdout.read().decode()
    ssh.close()
    return {"message": output}

@app.post("/clear")
async def post_minecraft_day():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=VAR_HOSTNAME, username=VAR_USERNAME, password=VAR_PASSWORD)
    stdin, stdout, stderr = ssh.exec_command('screen -r minecraft', get_pty=True)
    stdin.write('weather clear\n')
    stdin.write('\x01')  # Ctrl+A
    stdin.write('d')     # d
    output = stdout.read().decode()
    ssh.close()
    return {"message": output}