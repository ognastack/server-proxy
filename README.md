# server-proxy

See test cases to add a route and a service

chmod 755 ./certs
chmod -R 755 ./certs/live ./certs/archive

python3 manage.py --action up --domain user.ognastack.com --email ognastack@gmail.com --conf
python3 manage.py --action up-prod
