FROM node:16-alpine

# Installera Reveal.js och nödvändiga verktyg
WORKDIR /app
RUN apk add --no-cache git && \
    git clone https://github.com/hakimel/reveal.js.git && \
    cd reveal.js && \
    npm install && \
    npm install -D markdown

# Kopiera startskript
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

# Exponera port
EXPOSE 8000

CMD ["/app/start.sh"]