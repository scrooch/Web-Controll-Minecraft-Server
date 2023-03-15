# WebControlMinecraftServer

## Minecraft Server

1. Install Minecraft Bedrock Edition server on the Linux host.
   - Go to website https://minecraft.net/en-us/download/server/bedrock/ choose ubuntu version and right-click on the "DOWNLOAD" button, then select "Copy Link Address". As of 15.03.2023, the link is https://minecraft.azureedge.net/bin-linux/bedrock-server-1.19.70.02.zip.
   - On your Ubuntu machine, create a folder for your Minecraft server and navigate to that folder.
   - Run the following command:
   
     ```
     wget https://minecraft.azureedge.net/bin-linux/bedrock-server-1.19.70.02.zip
     ```
     <span style="color:red">Remember to paste the Minecraft server link you copied earlier.</span>
     
   - Unzip the downloaded file and run the following commands:
     
     ```
     chmod +x ./bedrock_server
     ./bedrock_server
     ```
     
   - Configure Minecraft by editing the `server.properties` file.

2. Run the server using the following commands:

    ```
    screen -S minecraft
    screen -r minecraft
    ```
3. Go to your minecraft server folder and run:
    ```
    ./bedrock_server > output.txt 2>&1
    Ctrl+a+d (to log out from screen)
    ```

## Backend (FastApi)

### Add Local Env

Add the following variables to your local environment:

|    Variable   | Description                                   |
| ------------- |-----------------------------------------------|
| FAST_HOSTNAME | Host name of SSH server                       |
| FAST_USERNAME | Username to authorize on SSH server            |
| FAST_PASSWORD | User password to authorize on SSH server       |
| FAST_PLAYERS  | List of players on Minecraft                   |
| FAST_PATH     | Path output.txt in zabbix server folder        |

After setting the variables, install the required packages using the following command:
```
pip install -r requirements.txt
```
To run the FastApi backend, use the following command:
```
python -m uvicorn main:app --reload
```

## Frontend (Vue)

To run the Vue frontend, you need to:

1. Install Node.js
2. Create a file named `.env` in the `/frontend` directory and add the following environment variables:
    ```
    VUE_APP_API_URL=http://127.0.0.1:3000
    VUE_APP_MINECRAFT_IP=127.0.0.1:19132
    ```

    Replace the value of `VUE_APP_API_URL` with your API URL and port, and replace the value of `VUE_APP_MINECRAFT_IP` with your Minecraft server IP and port.

3. Open the terminal in the `/frontend` directory and run the following commands:
    ```
    yarn global add @vue/cli
    yarn install
    yarn serve
    ```
