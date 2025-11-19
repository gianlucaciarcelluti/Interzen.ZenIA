FROM apache/nifi-registry:1.28.1

USER root

# Scarica il driver PostgreSQL JDBC
RUN curl -L https://jdbc.postgresql.org/download/postgresql-42.7.3.jar \
    -o /opt/nifi-registry/nifi-registry-current/lib/postgresql-jdbc.jar

# Installa netcat per wait-for-it
RUN apt-get update && \
    apt-get install -y netcat-openbsd && \
    rm -rf /var/lib/apt/lists/*

# Script wait-for-it
RUN echo '#!/bin/bash\n\
set -e\n\
host="$1"\n\
port="$2"\n\
shift 2\n\
until nc -z "$host" "$port"; do\n\
  echo "Waiting for $host:$port..."\n\
  sleep 2\n\
done\n\
echo "PostgreSQL is ready!"\n\
exec "$@"' > /usr/local/bin/wait-for-postgres.sh && \
    chmod +x /usr/local/bin/wait-for-postgres.sh

# Copia il file providers.xml configurato per PostgreSQL
COPY providers.xml /opt/nifi-registry/nifi-registry-current/conf/providers.xml

# Cambia ownership del file providers.xml
RUN chown nifi:nifi /opt/nifi-registry/nifi-registry-current/conf/providers.xml

# Ripristina l'utente nifi
USER nifi

EXPOSE 18080

# Avvia con wait-for-it
ENTRYPOINT ["/usr/local/bin/wait-for-postgres.sh", "postgres", "5432", "/opt/nifi-registry/nifi-registry-current/bin/nifi-registry.sh"]
CMD ["run"]