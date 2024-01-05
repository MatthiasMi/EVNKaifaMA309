# Smartmeter :zap:

This repository contains (hobby) code and HowTo's to perform SmartMeter readout of Kaifa MA309. Particularly, this smartmeter is used by EVN (Netz NÖ GmbH) and read via its customer interface (EVN Kundenschnittstelle).

## Usage EN
Each measurement (every 3 seconds),
- a `html`-file is (over-)written such that the webserver yields the latest readout (indicated by a timestamp)
- a row is written to a MySQL Database

`git clone https://github.com/MatthiasMi/EVNKaifaMA309.git`
clones the repository
`cd EVNKaifaMA309`
to change into the folder and execute
`python3 EVNKaifaMA309/smartmeter.py`
or
`./EVNKaifaMA309/smartmeter.py`
if it has been made executable with
`chmod +x EVNKaifaMA309/smartmeter.py`

## Access
As a customer, get started by requesting the password [Kundenschnittstelle](https://www.netz-noe.at/Download-(1)/Smart-Meter/218_9_SmartMeter_Kundenschnittstelle_lektoriert_14.aspx) via `mailto:smartmeter@netz-noe.at` with "Kundennummer" / "Vertragskontonummer", and "Zählernummer".


## Software
`sudo apt install pip`
installs pip and all requirements
`pip install -r requirements.txt`
and to set them up system wide
`sudo pip --break-system-packages install -r requirements.txt`


### Webserver
Install a webserver via
`sudo apt install apache2`
and enable it
`systemctl status apache2`
before changing to the folder, 
`cd /var/www/`
moving the default page
`sudo mv html/index.html html/default.html`
and making it writable for the script
`sudo chown pi html`


## Database
To add a database, first install
`sudo apt-get -y install mariadb-server mysql-server`
and after testing the connection
`mysql -hlocalhost -upi -pP4ssw0rd!!!11oneELEVEN db`
provision the database structure
`cat EVNKaifaMA309/smartmeter.sql | mysql -hlocalhost -upi -P4ssw0rd!!!11oneELEVEN db`
of the MySQL Initialization file `smartmeter.sql`.

Needless to say, passing these parameters and in particular the password via environment variables is the preferred way.
