# Kubernetes Manifests per MS10-LOGGER

Questa directory contiene i manifest Kubernetes per il deployment completo dello stack ELK (Elasticsearch, Logstash, Kibana) e componenti correlati per MS10-LOGGER.

## 1. Namespace

**File**: `namespace.yaml`
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: zenia-logging
  labels:
    name: zenia-logging
    app: ms10-logger
```

## 2. Elasticsearch Cluster

### StatefulSet per Elasticsearch

**File**: `elasticsearch-statefulset.yaml`
```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: elasticsearch
  namespace: zenia-logging
  labels:
    app: elasticsearch
    component: ms10-logger
spec:
  serviceName: elasticsearch
  replicas: 3
  selector:
    matchLabels:
      app: elasticsearch
  template:
    metadata:
      labels:
        app: elasticsearch
        component: ms10-logger
    spec:
      securityContext:
        fsGroup: 1000
        runAsUser: 1000
      containers:
      - name: elasticsearch
        image: docker.elastic.co/elasticsearch/elasticsearch:8.11.0
        env:
        - name: ES_JAVA_OPTS
          value: "-Xms2g -Xmx2g"
        - name: discovery.type
          value: single-node
        - name: cluster.name
          value: zenia-logging
        - name: node.name
          valueFrom:
            fieldRef:
              fieldPath: metadata.name
        - name: path.data
          value: /usr/share/elasticsearch/data
        - name: path.logs
          value: /usr/share/elasticsearch/logs
        - name: xpack.security.enabled
          value: "true"
        - name: xpack.security.transport.ssl.enabled
          value: "true"
        - name: xpack.security.http.ssl.enabled
          value: "true"
        - name: xpack.security.transport.ssl.verification_mode
          value: certificate
        - name: xpack.security.http.ssl.verification_mode
          value: certificate
        - name: xpack.monitoring.collection.enabled
          value: "true"
        ports:
        - containerPort: 9200
          name: http
        - containerPort: 9300
          name: transport
        volumeMounts:
        - name: elasticsearch-data
          mountPath: /usr/share/elasticsearch/data
        - name: elasticsearch-config
          mountPath: /usr/share/elasticsearch/config/elasticsearch.yml
          subPath: elasticsearch.yml
        - name: elasticsearch-certs
          mountPath: /usr/share/elasticsearch/config/certs
        resources:
          requests:
            memory: 4Gi
            cpu: 1000m
          limits:
            memory: 4Gi
            cpu: 2000m
        readinessProbe:
          httpGet:
            path: /_cluster/health
            port: 9200
            scheme: HTTPS
          initialDelaySeconds: 30
          periodSeconds: 10
        livenessProbe:
          httpGet:
            path: /_cluster/health
            port: 9200
            scheme: HTTPS
          initialDelaySeconds: 60
          periodSeconds: 30
      volumes:
      - name: elasticsearch-config
        configMap:
          name: elasticsearch-config
      - name: elasticsearch-certs
        secret:
          secretName: elasticsearch-certs
  volumeClaimTemplates:
  - metadata:
    name: elasticsearch-data
    namespace: zenia-logging
  spec:
    accessModes: ["ReadWriteOnce"]
    resources:
      requests:
        storage: 100Gi
    storageClassName: fast-ssd
```

### Service per Elasticsearch

**File**: `elasticsearch-service.yaml`
```yaml
apiVersion: v1
kind: Service
metadata:
  name: elasticsearch
  namespace: zenia-logging
  labels:
    app: elasticsearch
    component: ms10-logger
spec:
  selector:
    app: elasticsearch
  ports:
  - name: http
    port: 9200
    targetPort: 9200
  - name: transport
    port: 9300
    targetPort: 9300
  clusterIP: None
```

### ConfigMap per Elasticsearch

**File**: `elasticsearch-configmap.yaml`
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: elasticsearch-config
  namespace: zenia-logging
data:
  elasticsearch.yml: |
    cluster.name: zenia-logging
    node.name: ${POD_NAME}
    path.data: /usr/share/elasticsearch/data
    path.logs: /usr/share/elasticsearch/logs

    network.host: 0.0.0.0
    http.port: 9200

    discovery.seed_hosts: ["elasticsearch-0.elasticsearch.zenia-logging.svc.cluster.local:9300", "elasticsearch-1.elasticsearch.zenia-logging.svc.cluster.local:9300", "elasticsearch-2.elasticsearch.zenia-logging.svc.cluster.local:9300"]
    cluster.initial_master_nodes: ["elasticsearch-0", "elasticsearch-1", "elasticsearch-2"]

    xpack.security.enabled: true
    xpack.security.transport.ssl.enabled: true
    xpack.security.http.ssl.enabled: true
    xpack.security.transport.ssl.verification_mode: certificate
    xpack.security.http.ssl.verification_mode: certificate

    xpack.security.transport.ssl.keystore.path: certs/elastic-certificates.p12
    xpack.security.transport.ssl.truststore.path: certs/elastic-certificates.p12
    xpack.security.http.ssl.keystore.path: certs/elastic-certificates.p12
    xpack.security.http.ssl.truststore.path: certs/elastic-certificates.p12

    xpack.monitoring.collection.enabled: true
    xpack.monitoring.collection.interval: 10s

    indices.query.bool.max_clause_count: 1024
    search.max_buckets: 10000
    indices.memory.index_buffer_size: 10%

    cluster.routing.allocation.disk.threshold_enabled: true
    cluster.routing.allocation.disk.watermark.low: 85%
    cluster.routing.allocation.disk.watermark.high: 90%
    cluster.routing.allocation.disk.watermark.flood_stage: 95%
```

## 3. Logstash Deployment

### Deployment per Logstash

**File**: `logstash-deployment.yaml`
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: logstash
  namespace: zenia-logging
  labels:
    app: logstash
    component: ms10-logger
spec:
  replicas: 3
  selector:
    matchLabels:
      app: logstash
  template:
    metadata:
      labels:
        app: logstash
        component: ms10-logger
    spec:
      containers:
      - name: logstash
        image: docker.elastic.co/logstash/logstash:8.11.0
        env:
        - name: LS_JAVA_OPTS
          value: "-Xms1g -Xmx1g"
        - name: XPACK_MONITORING_ENABLED
          value: "true"
        - name: XPACK_MONITORING_ELASTICSEARCH_HOSTS
          value: "https://elasticsearch:9200"
        ports:
        - containerPort: 5044
          name: beats
        - containerPort: 8080
          name: http
        volumeMounts:
        - name: logstash-config
          mountPath: /usr/share/logstash/pipeline
        - name: logstash-templates
          mountPath: /usr/share/logstash/templates
        - name: geoip-db
          mountPath: /usr/share/logstash/geoip
        resources:
          requests:
            memory: 2Gi
            cpu: 500m
          limits:
            memory: 2Gi
            cpu: 1000m
        readinessProbe:
          httpGet:
            path: /
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        livenessProbe:
          httpGet:
            path: /
            port: 8080
          initialDelaySeconds: 60
          periodSeconds: 30
      volumes:
      - name: logstash-config
        configMap:
          name: logstash-config
      - name: logstash-templates
        configMap:
          name: logstash-templates
      - name: geoip-db
        configMap:
          name: geoip-db
```

### Service per Logstash

**File**: `logstash-service.yaml`
```yaml
apiVersion: v1
kind: Service
metadata:
  name: logstash
  namespace: zenia-logging
  labels:
    app: logstash
    component: ms10-logger
spec:
  selector:
    app: logstash
  ports:
  - name: beats
    port: 5044
    targetPort: 5044
  - name: http
    port: 8080
    targetPort: 8080
  type: ClusterIP
```

## 4. Kibana Deployment

### Deployment per Kibana

**File**: `kibana-deployment.yaml`
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: kibana
  namespace: zenia-logging
  labels:
    app: kibana
    component: ms10-logger
spec:
  replicas: 1
  selector:
    matchLabels:
      app: kibana
  template:
    metadata:
      labels:
        app: kibana
        component: ms10-logger
    spec:
      containers:
      - name: kibana
        image: docker.elastic.co/kibana/kibana:8.11.0
        env:
        - name: ELASTICSEARCH_HOSTS
          value: "https://elasticsearch:9200"
        - name: ELASTICSEARCH_SSL_CERTIFICATEAUTHORITIES
          value: /usr/share/kibana/config/certs/ca.crt
        - name: SERVER_SSL_ENABLED
          value: "true"
        - name: SERVER_SSL_CERTIFICATE
          value: /usr/share/kibana/config/certs/kibana.crt
        - name: SERVER_SSL_KEY
          value: /usr/share/kibana/config/certs/kibana.key
        - name: XPACK_SECURITY_ENABLED
          value: "true"
        - name: XPACK_ENCRYPTEDSAVEDOBJECTS_ENCRYPTIONKEY
          valueFrom:
            secretKeyRef:
              name: kibana-secrets
              key: encryption-key
        ports:
        - containerPort: 5601
          name: http
        volumeMounts:
        - name: kibana-config
          mountPath: /usr/share/kibana/config/kibana.yml
          subPath: kibana.yml
        - name: kibana-certs
          mountPath: /usr/share/kibana/config/certs
        resources:
          requests:
            memory: 1Gi
            cpu: 500m
          limits:
            memory: 1Gi
            cpu: 1000m
        readinessProbe:
          httpGet:
            path: /login
            port: 5601
            scheme: HTTPS
          initialDelaySeconds: 30
          periodSeconds: 10
        livenessProbe:
          httpGet:
            path: /login
            port: 5601
            scheme: HTTPS
          initialDelaySeconds: 60
          periodSeconds: 30
      volumes:
      - name: kibana-config
        configMap:
          name: kibana-config
      - name: kibana-certs
        secret:
          secretName: kibana-certs
```

### Service per Kibana

**File**: `kibana-service.yaml`
```yaml
apiVersion: v1
kind: Service
metadata:
  name: kibana
  namespace: zenia-logging
  labels:
    app: kibana
    component: ms10-logger
spec:
  selector:
    app: kibana
  ports:
  - name: http
    port: 5601
    targetPort: 5601
  type: ClusterIP
```

## 5. Ingress per Accesso Esterno

**File**: `ingress.yaml`
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: zenia-logging-ingress
  namespace: zenia-logging
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/force-ssl-redirect: "true"
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
spec:
  tls:
  - hosts:
    - logger.zenia.local
    secretName: zenia-logging-tls
  rules:
  - host: logger.zenia.local
    http:
      paths:
      - path: /kibana
        pathType: Prefix
        backend:
          service:
            name: kibana
            port:
              number: 5601
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: logstash
            port:
              number: 8080
```

## 6. Configurazione HPA (Horizontal Pod Autoscaler)

**File**: `hpa.yaml`
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: logstash-hpa
  namespace: zenia-logging
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: logstash
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: External
    external:
      metric:
        name: kafka_consumer_lag
        selector:
          matchLabels:
            topic: zenia-logs
      target:
        type: AverageValue
        averageValue: "1000"
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: elasticsearch-hpa
  namespace: zenia-logging
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: StatefulSet
    name: elasticsearch
  minReplicas: 3
  maxReplicas: 6
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 75
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

## 7. Network Policies

**File**: `network-policies.yaml`
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: elasticsearch-network-policy
  namespace: zenia-logging
spec:
  podSelector:
    matchLabels:
      app: elasticsearch
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          component: ms10-logger
    - namespaceSelector:
        matchLabels:
          name: zenia-system
    ports:
    - protocol: TCP
      port: 9200
    - protocol: TCP
      port: 9300
  egress:
  - to: []
    ports:
    - protocol: TCP
      port: 443
---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: logstash-network-policy
  namespace: zenia-logging
spec:
  podSelector:
    matchLabels:
      app: logstash
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          component: ms10-logger
    - namespaceSelector:
        matchLabels:
          name: zenia-apps
    ports:
    - protocol: TCP
      port: 5044
    - protocol: TCP
      port: 8080
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: elasticsearch
    - podSelector:
        matchLabels:
          app: kafka
    ports:
    - protocol: TCP
      port: 9200
    - protocol: TCP
      port: 9300
    - protocol: TCP
      port: 9092
```

Questi manifest Kubernetes forniscono un deployment completo e sicuro dello stack ELK per MS10-LOGGER, con alta disponibilità, scalabilità automatica e sicurezza enterprise.
