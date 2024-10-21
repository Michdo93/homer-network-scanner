import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup

# Warnungen unterdrücken
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def check_website(ip, port):
    try:
        # Erstellen der URL aus IP und Port (sowohl HTTP als auch HTTPS)
        url = f"http://{ip}:{port}" if port != 443 else f"https://{ip}:{port}"
        
        # Zeitüberschreitung nach 3 Sekunden, Verbindungen mit unsicherem SSL zulassen
        response = requests.get(url, timeout=3, verify=False)
        
        # Überprüfen, ob die Seite erreichbar ist (Statuscode 200)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Titel der Seite extrahieren
            title = soup.title.string.strip() if soup.title else "No title"
            
            # Suchen nach dem Icon (verschiedene Möglichkeiten)
            icon_link = None
            icon_tags = soup.find_all('link', rel=['icon', 'shortcut icon', 'apple-touch-icon'])
            if icon_tags:
                icon_link = icon_tags[0].get('href')
                if not icon_link.startswith('http'):
                    icon_link = f"http://{ip}:{port}/{icon_link.lstrip('/')}"
            
            # Suche nach einem Bild (z. B. Firmenlogo) im <img>-Tag
            logo_link = None
            img_tags = soup.find_all('img')
            for img in img_tags:
                src = img.get('src')
                if 'logo' in src.lower() or 'icon' in src.lower():
                    logo_link = src
                    if not logo_link.startswith('http'):
                        logo_link = f"http://{ip}:{port}/{logo_link.lstrip('/')}"
                    break
            
            # Titel, Icon oder Logo zurückgeben
            return {"ip": ip, "port": port, "url": url, "title": title, "icon": icon_link or logo_link}
        else:
            return None
    except (requests.ConnectionError, requests.Timeout):
        return None


def scan_ip_range(start_ip, end_ip, ports):
    # Funktion zum Iterieren der IP-Adressen im Bereich
    def ip_range(start_ip, end_ip):
        start = list(map(int, start_ip.split('.')))
        end = list(map(int, end_ip.split('.')))
        temp = start
        ip_list = []
        
        ip_list.append(start_ip)
        while temp != end:
            temp[3] += 1
            for i in (3, 2, 1, 0):
                if temp[i] == 256:
                    temp[i] = 0
                    temp[i-1] += 1
            ip_list.append('.'.join(map(str, temp)))
        return ip_list

    results = []
    ip_addresses = ip_range(start_ip, end_ip)

    for ip in ip_addresses:
        for port in ports:
            result = check_website(ip, port)
            if result:
                results.append(result)

    return results


def generate_homer_yaml(websites):
    yaml_output = []
    
    yaml_output.append('title: "Dashboard"')
    yaml_output.append('subtitle: "Your Dashboard"')
    yaml_output.append('logo: "logo.png"')
    yaml_output.append('header: true')
    yaml_output.append('footer: \'<p>Your Dashboard - powered by Homer</p>\'')
    yaml_output.append('defaults:')
    yaml_output.append('  layout: columns')
    yaml_output.append('  colorTheme: light')
    yaml_output.append('theme: default')
    yaml_output.append('services:')
    yaml_output.append('  - name: "Web"')
    yaml_output.append('    icon: "fas fa-earth-europe"')
    yaml_output.append('    items:')

    # Durch alle Webseiten iterieren und YAML-Einträge hinzufügen
    for site in websites:
        yaml_output.append(f'      - name: "{site["title"]}"')
        yaml_output.append(f'        subtitle: "{site["ip"]}:{site["port"]}"')
        yaml_output.append(f'        logo: "{site["icon"] or "default_logo.png"}"')
        yaml_output.append(f'        tag: "{site["port"]}"')  # Port als Tag verwenden
        yaml_output.append(f'        url: "{site["url"]}"')
    
    return '\n'.join(yaml_output)


# Beispielaufruf: IP-Bereich 192.168.3.1 bis 192.168.3.254 scannen, Ports 80, 8080 und 443 prüfen
start_ip = '192.168.3.1'
end_ip = '192.168.3.254'
ports = [80, 8080, 443]

websites = scan_ip_range(start_ip, end_ip, ports)

# YAML-Datei für Homer generieren
yaml_content = generate_homer_yaml(websites)

# YAML-Datei speichern
with open('homer_dashboard.yaml', 'w') as yaml_file:
    yaml_file.write(yaml_content)

print("Homer YAML-Datei erfolgreich generiert!")
