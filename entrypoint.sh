set -e
echo "Start Flask!!!"

# flask resetdb

echo "Reset db!!!"


echo "------------------------------------"

gunicorn --bind 0.0.0.0:${APP_PORT} src:app