ARG VERSION
FROM quay.io/keycloak/keycloak:${VERSION} AS builder
LABEL authors="sum1re"

WORKDIR /opt/keycloak

ENV KC_HEALTH_ENABLED=true
ENV KC_METRICS_ENABLED=true
ENV KC_DB=postgres
ENV KC_FEATURES=passkeys

RUN /opt/keycloak/bin/kc.sh build

FROM quay.io/keycloak/keycloak:${VERSION}
COPY --from=builder /opt/keycloak/ /opt/keycloak/

ENV KC_DB=postgres
ENV KC_HTTP_ENABLED=true
ENV KC_PROXY_HEADERS=xforwarded
ENV KC_HTTP_HOST=127.0.0.1
ENV KC_HTTP_PORT=8080
ENV KC_HTTPS_PORT=8081
ENV KC_HTTP_MANAGEMENT_PORT=8082

EXPOSE 8080
EXPOSE 8081
EXPOSE 8082

ENTRYPOINT ["/opt/keycloak/bin/kc.sh"]
