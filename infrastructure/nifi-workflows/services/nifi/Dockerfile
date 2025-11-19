FROM apache/nifi:1.28.1

USER root

# Installa jq e curl per manipolare JSON e scaricare driver
RUN apt-get update && \
    apt-get install -y jq curl && \
    rm -rf /var/lib/apt/lists/*

# Scarica il driver JDBC PostgreSQL
RUN curl -o /opt/nifi/nifi-current/lib/postgresql-42.7.3.jar https://jdbc.postgresql.org/download/postgresql-42.7.3.jar && \
    chown nifi:nifi /opt/nifi/nifi-current/lib/postgresql-42.7.3.jar

# Crea lo script per configurare automaticamente NiFi Registry
RUN mkdir -p /opt/nifi/scripts

COPY configure-registry.sh /opt/nifi/scripts/configure-registry.sh
RUN chmod +x /opt/nifi/scripts/configure-registry.sh && \
    chown nifi:nifi /opt/nifi/scripts/configure-registry.sh

USER nifi

# Lo script verrà eseguito dopo l'avvio di NiFi tramite docker-compose command
