V tomto projekte je navrhnutých a naimplementovaných 5 komponent pre inteligentnú domácnosť na platforme Raspberry Pi. Komponenty sú prepojené cez Wi-Fi a kominukujú pomocou MQTT protokolu. MQTT je založený na odosielaní správ pomocou publish a subscribe metód. Pracuje na vrchole protokolu TCP / IP. Aby sme zabezpečili bezpečnú komunikáciu používame TLS(Transport Layer Security) protokol. Systém MQTT pozostáva z klientov komunikujúcich so serverom, často nazývaným broker.

Na každé použité Raspberry Pi nainštalujeme operačný systém Raspbian Stretch.

Z jedného Raspberry pi vytvoríme access point (prístupový bod) a MQTT brokera.
Prístupový bod vytvoríme podľa návodu z oficialnej stránky. (Avšak odporúčam pred vytvorenímprístupového bodu nainštalovať z Internetu všetko potrebné.)
https://www.raspberrypi.org/documentation/configuration/wireless/access-point.md 
Pre prístupový nastavíme statickú IP adresu 192.168.1.1. Nastavíme aby sa ostatným pripojeným zariadeniam priraďovali adresy v rozmedzí 192.168.1.2 až 192.168.1.30. Do hostapd configuračného súboru treba vložiť.
```
interface=wlan0
driver=nl80211
ssid=SmartHome
hw_mode=g
channel=7
wmm_enabled=0
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase=SmartHome1
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP
```

Inštalácia MQTT brokera. Najskôr treba stiahnuť potrebný softvér.
```
    sudo apt-get install mosquitto
    sudo apt-get install openssl
```

Konfiguracia MQTT broker aby používal TLS.

Najskôr si musíme vytvoriť našu vlastnú Certifikačnú autoritu(CA), vygenerovať kľúče a certifikáty pomocou openssl. Robíme to v adresáry openssl.
1. Vytvoríme CA key pair
```
    openssl genrsa -des3 -out ca.key 2048
```
2. Na vytvorenie CA certificate a podpísanie použijeme kľúč z prvého kroku.
```
    openssl req -new -x509 -days 1826 -key ca.key -out ca.crt
```
3. Vytvoríme broker key pair nechránený heslom.
```
    openssl genrsa -out server.key 2048
```
4. Na vytvorenie broker certificate použijeme klúč z 3. kroku.
```
    openssl req -new -out server.csr -key server.key
```
5. Podpíšeme broker certificate pomocou CA certificate z 2. kroku. Do *subjectAltName=IP:* priradime adresu brokera. 
```
    openssl x509 -req -in server.csr -extfile <(printf "subjectAltName=IP:192.168.1.1") -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt -days 365
```
6. Vytvoríme priečinok certs v adresáry /etc/mosquitto/ a presunieme tam položky broker certificate, čiže server.crt a broker key, čiže server.key. Vytvoríme priečinok ca_certificates v adresáry /etc/mosquitto/ a presunieme tam položku CA certificate, čiže ca.crt.
7. Vytvorimé súbor mosquitto.conf v adresáry /etc/mosquitto/conf.d ktorý bude obsahovať:
```
log_dest stderr
log_dest topic
log_type error
log_type warning
log_type notice
log_type information
log_type all
log_type debug
log_timestamp true

port 8883

allow_zero_length_clientid false

#certificates
cafile /etc/mosquitto/ca_certificates/ca.crt
keyfile /etc/mosquitto/certs/server.key
certfile /etc/mosquitto/certs/server.crt
tls_version tlsv1
```

Na každé Raspberry Pi z ktorého chceme vytvoriť komponentu stiahneme tento repozitár.
Súbor ca_certificates/ca.crt prepíšeme nami vytvoreným súborom ca.crt.
Nainštalujeme python knižnicu pre MQTT klienta
```
    sudo apt-get install python-pip	
    sudo pip install paho-mqtt
```
poprípade ďalšie knižnice, ktoré vyžadujú komponenty. Keď je všetko nainštalované, je treba zapnúť Raspberry Pi, ktoré slúži ako prístupový bod. Následne sa treba pripojiť s ostatnými Raspberry Pi do wifi siete s názvom SmartHome a heslom SmartHome1.

**Žiarovka (bulb)**

Je potrebne nainštalovať softvér na ovládanie Raspberry Pi SenseHat a následne Raspberry Pi reštartovať.
```
    sudo apt-get install sense-hat
    sudo reboot
```
Pri zapnutí žiarovky ``` python3 bulb/bulb_controller.py ``` začne odoberať nastavovaciu tému *settings/bulb/<IP_adresa_žiarovky>*.
Následne na túto tému môžme odosielať správy v tvare:

- *SUBSCRIBE <téma1> <téma2>*
    
    V správe môže byť téme jedna alebo viac.
    Keď žiarovka dostane správu *SUBSCRIBE home/room home/room/bulb1*, tak začne odoberať témy home/room a home/room/bulb1, na ktoré môže potom odosielať ovládacie správy.

- *UNSUBSCRIBE <téma1> <téma2>*
    
    V správe môže byť téme jedna alebo viac.
    Keď žiarovka dostane správu *UNSUBSCRIBE home/room home/room/bulb1*, tak prestane odoberať témy home/room a home/room/bulb1.

- *TOPICS*
    
    Keď žiarovka dostane túto správu, tak zverejní(publish) všetky svoje odoberané témy na tému *ovladac/bulb/<bulb_IP_address>*.
    
Na ovládaciu téme môžme zasielať správy:
- *off* - žiarovka sa zhasne 
- *on* - žiarovka sa rozsvieti s poslednou nastavenou farbou
- *switch* - žiarovka zmení svoj stav, buď sa zhasne alebo rozsvieti s~poslednou nastavenou farbou
– *oncolor <farba>* - žiarovka sa rozsvieti
- *switchcolor <farba>* - žiarovka zmení svoj stav, buď sa zhasne alebo rozsvieti s farbou
– *lightupcolor <farba>* - žiarovka sa postupne rozžiari s farbou
- *lowlight* - žiarovka nastaví znížený jas 
- *normallight* - žiarovka nastaví normálny jas
- *switchintensity* - žiarovka zmení svoju intenzitu jasu, buď nastaví znížený alebo normálny jas
- *security* - žiarovka svieti na bielo po dobu 20 sekúnd, potom 30 sekúnd bliká červené svetlo.

<farba> musí byť zapísaná vo formáte *[R,G,B]*, pričom R,G a B nadobúdaju honoty od 0 do 255 vrátane. 

**Vypínač (light switch)**

Je potrebné nainštalovať softvér na ovládanie GPIO pinov.
```
pip install RPi.GPIO
```
Pri zapnutí vypínača ``` python3 light_switch/light_switch_controller.py ``` začne odoberať nastavovaciu tému *settings/light_switch/<IP_adresa_vypínača>*.
Následne na túto tému môžme odosielať správy v tvare:

- *SETTOPIC <téma>* 
    
    Téma môže byť nastavená len jedna.
    Keď vypínač dostane správu *SETTOPIC home/room*, tak sa nastaví téma home/room, na ktorú budú posielané príkazy po stalčení tlačítka. 

- *SETCOLOR <farba>* 
    
    Dá sa nastaviť farba, s ktorou budú žiarovky svietiť pri ich zapnutí vypínačom.

Vypínač má tri tlačítka. Po stlačení prvého sa rozsvietia svetlá, druhého sa zmení intenzita jasu a tretieho sa svetlá vypnú.

**Detektor pohybu (motion controll)**

Je potrebné nainštalovať softvér na ovládanie GPIO pinov.
```
pip install RPi.GPIO
```
Pri zapnutí detektora pohybu ``` python3 motion/motion_controller.py ``` začne odoberať nastavovaciu tému *settings/motion_sensor/<IP_adresa_detektora>*.
Následne na túto tému môžme odosielať správy v tvare:

- *SETLOCATION <lokácia>* 
  
    Nastaví alebo zmení ovládaciu tému na *motion\_sensor/<lokácia>*.

- *SETLIGHTTOPIC <topic>* 
    
    Nastaví tému, ktorou budú ovládané svetlá.

- *SETCAMERANAME <názov>* 
    
    Nastaví kameru, ktorá bude spustená.

Na ovládaciu tému môžme zasielať správu:
    
- *switchmode* - detektor pohybu sa prepne do druhého módu.

Detektor pohybu má dva módy. Automatizačný mód pri zaznamenaní pohybu rozsvieti svetlá. Bezpečnostný mód pri zaznamenaní pohybu rozsvieti svetlá na bielo, zaznamená 20 sekundové video a potom svetlá začnú blikať na červeno.

**Kamera (camera)**

Je potrebné nainštalovať softvér na ovládanie GPIO pinov a na ovládanie kamery.
```
pip install RPi.GPIO.PWM
sudo apt-get install python3-picamera
```
Pri zapnutí kamery ``` python3 camera/camera_controller.py ``` začne odoberať nastavovaciu tému *settings/camera/<IP_adresa_kamery>*.
Následne na túto tému môžme odosielať správy v tvare:

- *SETNAME <názov>* 

    Po nastavení názvu sa ovládacia téma kamery zmení na *camera/<názov>*.

Na ovládaciu tému je možné posielať správy:

- *record* - kamera zaznamená 20 sekundové video na pamäťovú kartu
- *left* - servomotor otočí kameru o 10° do ľava
- *right* - servomotor otočí kameru o 10° do prava

Z bezpečnostnej kamery je možné pozerať živé vysielanie vo viacerých prehliadačoch zároveň na URL adrese *<IP_kamera>:8000*.

**Meteostanica (Meteostation)**

Je potrebne nainštalovať softvér na ovládanie Raspberry Pi SenseHat a následne Raspberry Pi reštartovať.
```
    sudo apt-get install sense-hat
    sudo reboot
```
Pri zapnutí meteostanice ``` python3 meteo_station/meteo_station_controller.py ``` začne odoberať nastavovaciu tému *settings/meteo_sensors/<IP_adresa_meteostanice>*.
Následne na túto tému môžme odosielať správy v tvare:

- *SETLOCATION <lokácia>*

    Nastaví alebo zmení tému, na ktorú sú každých 5 sekúnd odosielané namerané hodnoty zo senzorov, na *motion_sensor/<lokácia>*.

Správa s nameranými hodnotami vyzerá napríklad takto : *meteo_sensors/kitchen Wed, 15 May 2019 09:48:54 temperature is 22\,\textdegree C, humidity is 58\%, pressure is 997\,hPA, which is low pressure*

Namerané hodnoty sa tiež zobrazujú na LED displeji umiestnenom na Raspberry Pi Sense HAT. Pomocou joysticku je možné medzi veličinami prepínať. 

- Dohora - teplota
- Doľava - atmosferický tlak 
- Doprava - vlhkosť

**Ovládač**

Na ovládanie tohto systému zatiaľ slúži jednoduchý program, ktorý si v cykle pýta tému a správu. Po zadaní oboch odošle zadanú správu na zadanú správu.