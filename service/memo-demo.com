upstream fastapi_backend {
    server 127.0.0.1:8000;
    keepalive 32;
}

server {
    listen 80;
    server_name localhost sgcc-memo-demo.com www.sgcc-memo-demo.com;
    access_log /var/log/nginx/sgcc-memo-demo.access.log;
    error_log /var/log/nginx/sgcc-memo-demo.error.log;
    
    location ^~ /.well-known/acme-challenge/ {
        allow all;
        root /var/lib/letsencrypt/;
        default_type "text/plain";
        try_files $uri =404;
    }

    location /api/ {
        proxy_pass http://fastapi_backend/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
        proxy_read_timeout 90;
    }

    location /memos/ {
        proxy_pass http://fastapi_backend/memos/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
        proxy_read_timeout 90;
    }
    
    location / {
        root /home/rvnnt/sgcc-web-study/build;
        try_files $uri $uri/ /app.html;
        index app.html;
    }
    
    gzip on;
    gzip_vary on;
    gzip_min_length 1000;
    gzip_types text/plain text/css text/xml text/javascript application/javascript application/xml+rss application/json;
}

# HTTPS server (commented out until SSL certificates are available)
# server {
#     listen 443 ssl;
#     listen [::]:443 ssl;
#     http2 on;
#     server_name sgcc-memo-demo.com www.sgcc-memo-demo.com;
#     
#     ssl_certificate /etc/letsencrypt/live/sgcc-memo-demo.com/fullchain.pem;
#     ssl_certificate_key /etc/letsencrypt/live/sgcc-memo-demo.com/privkey.pem;
#     
#     add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;
#     add_header X-Frame-Options DENY always;
#     add_header X-Content-Type-Options nosniff always;
#     add_header X-XSS-Protection "0" always;
#     add_header Referrer-Policy "strict-origin-when-cross-origin" always;
#     
#     location /api/ {
#         proxy_pass http://fastapi_backend/;
#         proxy_http_version 1.1;
#         proxy_set_header Upgrade $http_upgrade;
#         proxy_set_header Connection 'upgrade';
#         proxy_set_header Host $host;
#         proxy_set_header X-Real-IP $remote_addr;
#         proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
#         proxy_set_header X-Forwarded-Proto $scheme;
#         proxy_cache_bypass $http_upgrade;
#         proxy_read_timeout 90;
#     }
#     
#     location / {
#         root /home/rvnnt/sgcc-web-study/build;
#         try_files $uri $uri/ /app.html;
#         index app.html;
#     }
#     
#     gzip on;
#     gzip_vary on;
#     gzip_min_length 1000;
#     gzip_types text/plain text/css text/xml text/javascript application/javascript application/xml+rss application/json;
# }
