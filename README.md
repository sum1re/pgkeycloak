# Custom Keycloak Image

A customized [**Keycloak**](https://www.keycloak.org/) image.

Docker Hub: [**sum1re/pgkeycloak**](https://hub.docker.com/r/sum1re/pgkeycloak)

## ✨ Features

This image is based on the official Keycloak distribution and includes:

- Passkeys support (KC_FEATURES=passkeys)
- Health checks enabled (KC_HEALTH_ENABLED=true)
- Prometheus metrics enabled (KC_METRICS_ENABLED=true)
- Optimized proxy and HTTP bindings for reverse-proxy scenarios
- Ready for **PostgreSQL** as the primary database

## 🚀 Usage (podman)

Example `.container` or `.service` unit for rootless Podman or system-wide systemd:

```Ini
[Unit]
Description=Keycloak Identity Server
After=network-online.target postgres.service

[Container]
Image=docker.io/sum1re/pgkeycloak:<version>

PublishPort=8080:8080
PublishPort=8082:8082

Exec=start --optimized

Environment=KC_DB_USERNAME=username
Environment=KC_DB_PASSWORD=password
Environment=KC_DB_URL=jdbc:postgresql://pgHost:pgPort/db

Environment=KC_HOSTNAME=https://example.com
Environment=KC_HOSTNAME_ADMIN=https://admin.example.com

[Install]
WantedBy=multi-user.target default.target
```

### Notes

- PublishPort=8080:8080 exposes HTTP (Keycloak user-facing port)
- PublishPort=8082:8082 exposes management API (metrics, health)

## 📘 Keycloak Documentation

- [Reverse Proxy Configuration](https://www.keycloak.org/server/reverseproxy)
- [Full Configuration Reference](https://www.keycloak.org/server/all-config)
- [Guide Index](https://www.keycloak.org/guides)

## 🛠️ Image Details

### 🔧 Build-time Environment

| env                | value    |
|--------------------|----------|
| KC_DB              | postgres |
| KC_FEATURES        | passkeys |
| KC_HEALTH_ENABLED  | true     |
| KC_METRICS_ENABLED | true     |

### 🚀 Runtime Defaults

| env                     | value      |
|-------------------------|------------|
| KC_DB                   | postgres   |
| KC_HTTP_ENABLED         | true       |
| KC_PROXY_HEADERS        | xforwarded |
| KC_HTTP_HOST            | 127.0.0.1  |
| KC_HTTP_PORT            | 8080       |
| KC_HTTPS_PORT           | 8081       |
| KC_HTTP_MANAGEMENT_PORT | 8082       |
