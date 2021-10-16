# The standard nginx container just runs nginx. The configuration file added
# below will be used by nginx.
FROM nginx

# Copy the nginx configuration file. This sets up the behavior of nginx. Most
# important, it ensures that nginx listens on port 8080. Google App Engine expects
# the runtime to respond to HTTP requests at port 8080.
COPY nginx.conf /etc/nginx/nginx.conf

# create log dir configured in nginx.conf
RUN mkdir -p /var/log/app_engine

# Finally, all static assets.
ADD dist /usr/share/nginx/html

CMD ["/bin/sh",  "-c",  "envsubst < /usr/share/nginx/html/assets/envconfig.template.js > /usr/share/nginx/html/assets/envconfig.js && exec nginx -g 'daemon off;'"]
