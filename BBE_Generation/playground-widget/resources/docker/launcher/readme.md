docker run -d -p 8080:80 \
-p 5005:5005 \
-e BPG_REDIS_WRITE_HOST=docker.for.mac.host.internal \
-e BPG_REDIS_WRITE_PORT=6379 \
-e BPG_REDIS_READ_HOST=docker.for.mac.host.internal \
-e BPG_REDIS_READ_PORT=6479 \
-e ENABLE_DEBUG=true \
playground-api:latest