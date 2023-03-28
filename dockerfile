FROM ubuntu:latest

RUN mkdir -p /app/minecraft
WORKDIR /app/minecraft

RUN apt-get update && apt-get install -y wget unzip libcurl4

ARG DOWNLOAD_LINK
RUN wget ${DOWNLOAD_LINK} -O minecraft.zip && unzip minecraft.zip && rm minecraft.zip

RUN sed -i 's/difficulty=.*/difficulty=normal/' server.properties && \
    sed -i 's/allow-cheats=.*/allow-cheats=true/' server.properties && \
    sed -i '$ a emit-server-telemetry=true' server.properties

EXPOSE 19132
CMD ./bedrock_server > output.txt 2>&1