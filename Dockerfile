FROM openresty/openresty:alpine

RUN mkdir -p /var/log/nginx /usr/local/openresty/nginx/lua

COPY nginx.conf /usr/local/openresty/nginx/conf/nginx.conf
COPY proxy.lua /usr/local/openresty/nginx/lua/proxy.lua

EXPOSE 80
CMD ["/usr/local/openresty/bin/openresty", "-g", "daemon off;"]
