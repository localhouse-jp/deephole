FROM openresty/openresty:alpine

COPY nginx.conf /usr/local/openresty/nginx/conf/nginx.conf
COPY proxy.lua /usr/local/openresty/nginx/lua/proxy.lua
RUN mkdir -p /var/log/nginx /usr/local/openresty/nginx/lua

EXPOSE 80
CMD ["/usr/local/openresty/bin/openresty", "-g", "daemon off;"]
