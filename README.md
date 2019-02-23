# bachelor-components
Žiarovka(bulb) - pri zapnutí začne odoberať(subscribe) tému "settings/bulb_IP_address".
    Pomocou tejto témy môžme:
        -odoberať ďalšie témy. Uvediem príklad ako môže vyzerať správa. 
        "SUBSCRIBE home/room home/room/bulb1"
        Keď žiarovka dostane túto správu na tému "settings/bulb_IP_address", tak začne odoberať témy home/room a home/room/bulb1.

        -prestať odoberať témy, ktoré odoberáme.
        "UNSUBSCRIBE home/room home/room/bulb1"
        Keď žiarovka dostane túto správu na tému "settings/bulb_IP_address", tak prestane odoberať témy home/room a home/room/bulb1.

        -ukázať témy, ktoré práve odoberáme.
        "TOPICS"
        Keď žiarovka dostane túto správu na tému "settings/bulb_IP_address", tak zverejní(publish) všetky svoje odoberané témy na tému "ovladac/bulb_IP_address".
    
    Keď žiarovka odoberá ďalšie témy, tak na tieto témy prijíma správy:
        - "0" vypne svetlo
        - "1" zapne svetlo s poslednou použitou farbou
        - "[R,G,B]" zapne svetlo vo farbe danej správy. R,G,B možu mať hodnoty 0 až 255.

Žiarovka kominukuje pomocou MQTT protokolu. MQTT je založený na odosielaní správ pomocou publish a subscribe metód. Pracuje na vrchole protokolu TCP / IP. Aby sme zabezpečili bezpečnú komunikáciu používame TLS(Transport Layer Security) protokol. Systém MQTT pozostáva z klientov komunikujúcich so serverom, často nazývaným broker.

Inštalácia na raspberry pi.
    MQTT broker :
        sudo apt-get install mosquitto mosquitto-clients
    Python MQTT client :
        sudo apt-get install python-pip	
        sudo pip install paho-mqtt


Konfiguracia MQTT broker aby používal TLS.
Najskôr si musíme vytvoriť našu vlastnú Certifikačnú autoritu(CA), vygenerovať kľúče a certifikáty pomocou openssl. Robíme to v adresáry openssl.
1. Vytvoríme CA key pair
    openssl genrsa -des3 -out ca.key 2048
2. Na vytvorenie CA certificate a podpísanie použijeme kľúč z prvého kroku.
    openssl req -new -x509 -days 1826 -key ca.key -out ca.crt
3. Vytvoríme broker key pair nechránený heslom.
    openssl genrsa -out server.key 2048
4. Na vytvorenie broker certificate použijeme klúč z 3. kroku.
    openssl req -new -out server.csr -key server.key
5. Podpíšeme broker certificate pomocou CA certificate z 2. kroku.
    openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt -days 360
6. Vytvoríme priečinok certs v adresáry /etc/mosquitto/ a presunieme tam položky broker certificate, čiže server.crt a broker key, čiže server.key. Vytvoríme priečinok ca_certificates v adresáry /etc/mosquitto/ a presunieme tam položku CA certificate, čiže ca.crt.
7. Vytvorimé súbor rpimosquitto.conf ktorý bude obsahovať:
#Plain MQTT protocol configuration
listener 8883 192.168.1.2
log_dest stderr
log_dest topic
log_type error
log_type warning
log_type notice
log_type information
log_type all
log_type debug
log_timestamp true
connection_messages true
persistence true
persistence_file mosquitto.db
retained_persistence true
#user_authentication
allow_anonymous false
password_file /etc/mosquitto/passwordfile
#certificates
cafile /etc/mosquitto/ca_certificates/ca.crt
keyfile /etc/mosquitto/certs/server.key
certfile /etc/mosquitto/certs/server.crt
tls_version tlsv1
#end plain config
8. MQTT client v našom prípade žiarovka obsahuje cestu k položke ca.crt, ktorú používa na komunikáciu.



