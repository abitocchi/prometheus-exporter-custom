## Certificates

To generate certificates run the following commands
```bash
openssl genrsa -out prometheus-exportert-CA.key 2048 

openssl req -x509 -new -nodes -key prometheus-exportert-CA.key -sha256 -days 1825 -out prometheus-exportert-CA.pem -subj "/C=IT/ST=RM/O=Sourcesense/CN=prom-exp-promehteus-exporter-devops.apps-crc.testing"

openssl genrsa -out promehteus-exporter.key 2048

openssl req -new -sha256 -key promehteus-exporter.key -subj "/C=IT/ST=RM/O=Sourcesense/CN=prom-exp-promehteus-exporter-devops.apps-crc.testing" -out promehteus-exporter.csr

openssl x509 -req -in promehteus-exporter.csr  -CA prometheus-exportert-CA.pem -CAkey prometheus-exportert-CA.key -CAcreateserial -out prometheus-exporter.crt -days 500 -sha256
```

Once the files are generated put the content of the following files into the values.yaml for the tls section:
* prometheus-exporter.crt -> certificate
* promehteus-exporter.key -> key
* prometheus-exportert-CA.pem -> caCertificate