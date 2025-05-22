FROM grafana/grafana:latest

RUN grafana-cli --pluginUrl https://github.com/tinybirdco/grafana-tinybird-datasource/releases/download/2.0.3/tinybird-tinybird-datasource-2.0.3.zip \
    plugins install tinybird-tinybird-datasource
