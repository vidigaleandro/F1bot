<h1>🏎️🤖 F1BOT 🤖🏎️</h1>

## Abstract:

### Development of a robot, an autonomous vehicle on a reduced scale, capable of performing trekking in completely autonomous ways, given a set of coordinates. 

### The strategy used for autonomous navigation was based on virtual potential fields.

### Worked with ROS Melodic: http://wiki.ros.org/melodic/Installation/Ubuntu

### Trekking coordinates: https://youtu.be/jMrno1yUcuE

### Obstacle Avoidance: https://www.youtube.com/shorts/B1dMoqXmQtM

## HOW TO INSTALL THE APPLICATION:

1) Use: `git clone https://github.com/vidigaleandro/F1bot` Inside Raspberry with ubuntu server 18.04 and ROS Melodic Installed. 
2) Go to the workspace: `catkin_make`
3) Setup: `source devel/setup.bash`
4) Run the applcation with: `roslaunch steering start.launch`

## Sctructure of the development:

![English - Arquitetura](https://user-images.githubusercontent.com/61214978/209714995-8e8a7655-10a5-4d28-a2d2-922287ca5286.png)

## Resume of ROS NODES Communication:

![EstruturaSoftwareENGLISH](https://user-images.githubusercontent.com/61214978/209715803-55102b5b-b7c3-422f-a6ef-91ee4c396ebe.png)

## Hardware Setup:

![Estrutura Hardware 3](https://user-images.githubusercontent.com/61214978/209715960-63f0fbae-fedf-4fc8-a206-92401a110c54.png)

![interiorcarro](https://user-images.githubusercontent.com/61214978/209718559-e13b2afa-c1b3-4e17-9cc0-ced0e00e6fe2.jpg)

![SuperiorCarro](https://user-images.githubusercontent.com/61214978/209718602-bd882a0e-df7a-4be6-b5d3-c8481419e1dd.jpg)


##  Chassi Storm Monster Truck:

![Carro](https://user-images.githubusercontent.com/61214978/209716051-c02f894d-d7ed-43dc-9873-4435206de8cc.png)

##  Raspberry Configuration:

1) Download ubuntu server 18.04: https://releases.ubuntu.com/18.04/ubuntu-18.04.6-live-server-amd64.iso
2) Build the image in a SD card: https://www.raspberrypi.com/software/
3) Insert the SD Card in Raspberry(Power On) and make a wired connection with you computer:

![ComputerCom](https://user-images.githubusercontent.com/61214978/209722254-520335d0-9502-4b62-90a9-6a960b8908db.png)

4) In your computer terminal write the command: `nm-connection-editor`
5) Change the IPV4 settings to: `Shared to other computers`
6) Back to terminal and write `cat /var/lib/misc/dnsmasq.leases` to find raspberry IP and name normally "ubuntu"
7) In terminal realize the ssh connection: `RASPBERRYNAME”@”RASPBERRYIP”`
8) Write de password: ubuntu
9) Enter a new password and try to ssh again to remote connection.


### WIFI Config:

1) Acess ubuntu terminal on Raspberry by the wired connection and update system: `sudo apt-get update`
2) Install HOSTAPD and DNSMASQ: `sudo apt-get install hostapd dnsmasq` -> Your computer need to be connected to internet by wifi.
3) Setup the acess point config: `sudo nano /etc/hostapd/hostapd.conf`
4) Inside the file copy this code(change ssid(WIFI NAME) and wpa_passphrase(WIFI PASSWORD):

```
interface=wlan0
driver=nl80211
ssid=MyWiFiNetwork
hw_mode=g
channel=7
wmm_enabled=0
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase=12345678
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP
```

5) Close and save the file and open this file: `sudo nano /etc/default/hostapd`
6) Inside the file copy this: DAEMON_CONF="/etc/hostapd/hostapd.conf"
7) restart HOSTAPD: 

```
sudo systemctl unmask hostapd
sudo systemctl enable hostapd
sudo systemctl start hostapd
```
8) Make a backup of dns config file: sudo cp /etc/dnsmasq.conf /etc/dnsmasq.conf.org
9) Make a new file: sudo nano /etc/dnsmasq.conf
10) Inside the file:
```
interface=wlan0
dhcp-range=192.168.4.2,192.168.4.20,255.255.255.0,24h
port=5353
```
11) Restart the dns system: `sudo systemctl reload dnsmasq`
12) Config initializate file: `sudo nano /lib/systemd/system/dnsmasq.service`
13) Change this lines:
```
After=network-online.target
Wants=network-online.target
```
14) Config a static IP in this file: `sudo nano /etc/netplan/50-cloud-init.yaml

15) Add to file the information(Need a correct identation, do not use TAB or Copy): 

```
       wlan0:
            dhcp4: false
            addresses:
            - 192.168.4.1/24
```

![NetworkSET](https://user-images.githubusercontent.com/61214978/209724555-e28c2238-9953-4749-8490-be3c06ec1121.png)

16) Test if the file is running: `sudo nano netplan apply` if correct, nothing will happen.

17) Reboot raspberry: 'sudo reboot'

18) Wait about five minutes to see the raspberry wifi in your computer.

19) Open the wifi , change the IPV4 to this config:

![WIFIconfig](https://user-images.githubusercontent.com/61214978/209725488-327ab9e4-640d-497a-8236-4af4e14f54aa.png)

20) Open computer terminal and make a ssh connection: `sudo ssh ubuntu@192.168.4.1`

21) In this case to have internet connection you need to a wired acess with router to your computer.



