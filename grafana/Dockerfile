FROM grafana/grafana:latest
USER root

RUN apk add --no-cache curl unzip gettext

COPY provisioning /etc/grafana/provisioning

# Download and manually install the Tinybird plugin correctly
RUN mkdir -p /usr/share/grafana/plugins/tinybird-tinybird-datasource && \
    curl -L https://github.com/tinybirdco/grafana-tinybird-datasource/releases/download/2.0.3/tinybird-tinybird-datasource-2.0.3.zip -o /tmp/plugin.zip && \
    unzip /tmp/plugin.zip -d /tmp/plugin && \
    mv /tmp/plugin/tinybird-tinybird-datasource/* /usr/share/grafana/plugins/tinybird-tinybird-datasource && \
    rm -rf /tmp/plugin /tmp/plugin.zip

RUN chmod -R 755 /var/lib/grafana/plugins

