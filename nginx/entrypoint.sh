#!/bin/bash
[ ! -z "$NGINX_SSL" ] && envsubst '${NGINX_DASHBOARD_DOMAIN}' < /etc/nginx/conf.d/with_domain.template > /etc/nginx/conf.d/default.conf && exec nginx -g 'daemon off;'
[ -z "$NGINX_SSL" ] && envsubst '${NGINX_DASHBOARD_DOMAIN}' < /etc/nginx/conf.d/without_domain.template > /etc/nginx/conf.d/default.conf && exec nginx -g 'daemon off;'  
