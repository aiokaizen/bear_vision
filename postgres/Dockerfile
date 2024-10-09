FROM postgres:15.3-alpine3.18

EXPOSE 5437

COPY init_db.sh /docker-entrypoint-initdb.d/
RUN chmod +x /docker-entrypoint-initdb.d/init_db.sh
