# TwitterBot Version: Beta

Simple Twitter Bot with the following features:
    * Monitor RSS feeds and create tweets from RSS entries
    * Automatic retweet of monitored twitter accounts
    * Human emulation

[![platform](https://img.shields.io/badge/platform-linux-green)](https://ubuntu.com/)
[![python](https://img.shields.io/badge/python-3.9-blue.svg?logo=python&labelColor=yellow)](https://www.python.org/downloads/)


## Instalar desde fuentes

1. Clona el repositorio:
```
git clone https://github.com/mercaderd/TwitterBot.git
```

2. Instalar dependencias:

```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install wget python3 python3-pip python3-venv
```

3. Crear fichero .env a partir del ejemplo incluido:

```    
cp .env.dist .env
```

4. Edita .env para establecer los valores de configuración:
```  
nano .env
``` 

Modifica las siguientes líneas según la configuración de tu sistema:
```     
# CHANGE THIS SECTION enter the corresponding information from your Twitter application:
CONSUMER_KEY=put_here_your_twitter_consumer_key
CONSUMER_SECRET=put_here_your_twitter_consumer_secret
ACCESS_KEY=put_here_your_twitter_access_key
ACCESS_SECRET=put_here_your_twitter_access_secret

# CHANGE THIS SECTION add usernames for automatic retweet
usernames=AEPD_es,osiseguridad,incibe_cert,EU_EDPB
``` 
Pulsa Ctrl+x para salir y guarda los cambios.

5. Ejecuta la aplicación:
``` 
./run.sh
```