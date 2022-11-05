cd /applications || exit

export PYTHONUNBUFFERED=TRUE

python3 -m gunicorn -k uvicorn.workers.UvicornWorker \
  --workers 1 \
  --bind "0.0.0.0:${APP_PORT:-8080}" \
  --timeout 600 \
  --log-level debug \
  --access-logfile - \
  --log-file - \
   signs.main:app \
  "$@"
