FROM nginx:1.23.3-alpine

ENV http_proxy=$http_proxy
ENV https_proxy=$https_proxy

RUN apk add --no-cache openssl inotify-tools

WORKDIR /etc/nginx/

ADD nginx.conf.envsubst nginx.https.available.conf.envsubst ./
ADD geonode.conf.envsubst ./sites-enabled/

ADD docker-autoreload.sh docker-entrypoint.sh /
ENTRYPOINT ["/docker-entrypoint.sh"]
RUN chmod +x /docker-autoreload.sh
RUN chmod +x /docker-entrypoint.sh

CMD ["nginx", "-g", "daemon off;"]
