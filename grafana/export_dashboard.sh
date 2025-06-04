#!/bin/sh

DASHBOARD_UIDS="energy-prices other-dashboard"
DEST_DIR="/dashboards"

mkdir -p "$DEST_DIR"

for UID in $DASHBOARD_UIDS; do
  echo "Exporting $UID..."
  curl -s -H "Authorization: Bearer $API_KEY" \
       "$GRAFANA_URL/api/dashboards/uid/$UID" \
       -o "$DEST_DIR/$UID.json"
done