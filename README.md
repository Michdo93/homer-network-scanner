# homer-network-scanner
A scanner for [Homer](https://github.com/bastienwirtz/homer) (HOMepage for your servER), which scans the network and generates a configuration file.

Admittedly, you can configure this static page as you wish. You can also simply omit entries found or group them differently. You may also want to use other icons, etc. This program is just a little helper to save you a little time.

## Pre-installation

At first you have to install:

```
python3 -m pip install requests
python3 -m pip install bs4
```

## Usage

### Configuration

Please edit `scanner.py`:

```
start_ip = '192.168.3.1'
end_ip = '192.168.3.254'
ports = [80, 8080, 443]
```

You can scan different IPs, even individual ones. It currently scans standard ports, but you can also add additional ports. It is more common to run applications on ports 3000, 4000, 5000 or 8000.

### Execution

The you have to run:

```
python3 scanner.py
```

This will create a file named `homer_dashboard.yaml`

## Example

As example you will receive:

```
title: "Dashboard"
subtitle: "Your Dashboard"
logo: "logo.png"
header: true
footer: '<p>Your Dashboard - powered by Homer</p>'
defaults:
  layout: columns
  colorTheme: light
theme: default
services:
  - name: "Web"
    icon: "fas fa-earth-europe"
    items:
      - name: "FRITZ!Box"
        subtitle: "192.168.3.1:80"
        logo: "http://192.168.3.1:80/favicon.ico"
        tag: "80"
        url: "http://192.168.3.1:80"
      - name: "FRITZ!Box"
        subtitle: "192.168.3.1:443"
        logo: "http://192.168.3.1:443/favicon.ico"
        tag: "443"
        url: "https://192.168.3.1:443"
      - name: "FRITZ!Repeater"
        subtitle: "192.168.3.2:80"
        logo: "http://192.168.3.2:80/favicon.ico"
        tag: "80"
        url: "http://192.168.3.2:80"
      - name: "FRITZ!Repeater"
        subtitle: "192.168.3.2:443"
        logo: "http://192.168.3.2:443/favicon.ico"
        tag: "443"
        url: "https://192.168.3.2:443"
      - name: "No title"
        subtitle: "192.168.3.10:80"
        logo: "default_logo.png"
        tag: "80"
        url: "http://192.168.3.10:80"
      - name: "No title"
        subtitle: "192.168.3.10:443"
        logo: "default_logo.png"
        tag: "443"
        url: "https://192.168.3.10:443"
```

At least you can copy and paste parts from it to your configuration file.
Then you have to 
