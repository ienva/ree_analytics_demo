docker build -t grafana-with-tinybird .
docker run -d -p 3000:3000 --name=grafana -e "GF_PLUGINS_ALLOW_LOADING_UNSIGNED_PLUGINS=tinybird-tinybird-datasource" grafana-with-tinybird