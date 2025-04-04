from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt
import time
import subprocess
import requests
from shodan import Shodan

# shodan api
SHODAN_API_KEY = "put youre key here"
shodan_client = Shodan(SHODAN_API_KEY)


console = Console()


def gradient_text(text, start_color=(0,0,255), end_color=(255,255,255)):
    result = ""
    n = len(text)
    if n == 0:
        return ""
    for i, char in enumerate(text):
        r = int(start_color[0] + (end_color[0] - start_color[0]) * i / (n - 1))
        g = int(start_color[1] + (end_color[1] - start_color[1]) * i / (n - 1))
        b = int(start_color[2] + (end_color[2] - start_color[2]) * i / (n - 1))
        result += f"[rgb({r},{g},{b})]{char}[/rgb({r},{g},{b})]"
    return result

# main banner
BANNER_TEXT = """\

╔═╗╔═╗╔╦╗  ╔╦╗╔═╗╔═╗╦  
╠╣ ║╣  ║║   ║ ║ ║║ ║║  
 ╚  ╚═╝═╩╝   ╩ ╚═╝╚═╝╩═╝"""


# banner 2
MAIN_BANNER = """\
┌──────────────────────────────┐
│         @D3XON/FED           │
│ https://discord.gg/NM7hceAvsp│
└──────────────────────────────┘"""

# categories banner
CATEGORY_BANNER = """\
+--^----------,--------,-----,--------^-,
 | |||||||||   `--------'     |          O
 `+---------------------------^----------|
   `\\_,---------,---------,--------------'
     / XXXXXX /'|       /'
    / XXXXXX /  `\\    /'
   / XXXXXX /`-------'
  / XXXXXX /
 / XXXXXX /
(________(                
 `------'  
"""

def clear_screen():
    print("\033c", end="")

def display_banner(category_name=None):
    """Zeigt das Hauptbanner (mit Farbverlauf) und optional ein Kategorie-Banner an."""
    clear_screen()
    # main banner color
    console.print(Panel(gradient_text(BANNER_TEXT), expand=False), justify="center")
    if category_name:
        # categories banner color
        console.print(f"[bold cyan]{CATEGORY_BANNER}[/bold cyan]")
        console.print(Panel(f"[bold cyan]{category_name}[/bold cyan]", style="bold cyan", expand=False), justify="center")

def print_category_header(title):
    """Zeigt den Header für eine Kategorie an (Banner + Überschrift)."""
    display_banner(title)
    console.print(f"\n[blue]                +----------------------+[/blue]")
    console.print(f"[blue]                | {title.center(20)} |[/blue]")
    console.print(f"[blue]                +----------------------+[/blue]\n")

# ========================== OSINT & RECON ==========================

def osint_ip_lookup():
    """Funktion: IP Lookup"""
    print_category_header("IP Lookup")
    ip = Prompt.ask("Enter IP address")
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}").json()
        if response["status"] == "success":
            console.print(Panel(
                f"IP: {response['query']}\n"
                f"Country: {response['country']}\n"
                f"Region: {response['regionName']}\n"
                f"City: {response['city']}\n"
                f"ISP: {response['isp']}",
                title="[bold blue]IP Lookup Result[/bold blue]", border_style="green"
            ))
        else:
            console.print("[red]Invalid IP or API issue[/red]")
    except requests.exceptions.RequestException as e:
        console.print(f"[red]Error: {e}[/red]")
    time.sleep(2)
    osint_menu()

def osint_dns_lookup():
    """Funktion: DNS Lookup via nslookup"""
    print_category_header("DNS Lookup")
    domain = Prompt.ask("Enter domain for DNS lookup")
    try:
        result = subprocess.run(["nslookup", domain], capture_output=True, text=True)
        console.print(Panel(result.stdout, title="[bold blue]DNS Lookup Result[/bold blue]", border_style="green"))
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
    time.sleep(2)
    osint_menu()

def osint_whois_lookup():
    """Funktion: WHOIS Lookup"""
    print_category_header("WHOIS Lookup")
    domain = Prompt.ask("Enter domain for WHOIS lookup")
    try:
        result = subprocess.run(["whois", domain], capture_output=True, text=True)
        console.print(Panel(result.stdout, title="[bold blue]WHOIS Lookup Result[/bold blue]", border_style="green"))
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
    time.sleep(2)
    osint_menu()

def osint_geolocation():
    """Funktion: IP Geolocation"""
    print_category_header("IP Geolocation")
    ip = Prompt.ask("Enter IP address for geolocation")
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}").json()
        if response["status"] == "success":
            console.print(Panel(
                f"IP: {response['query']}\n"
                f"Country: {response['country']}\n"
                f"Region: {response['regionName']}\n"
                f"City: {response['city']}\n"
                f"ISP: {response['isp']}",
                title="[bold blue]IP Geolocation Result[/bold blue]", border_style="green"
            ))
        else:
            console.print("[red]Invalid IP or API issue[/red]")
    except requests.exceptions.RequestException as e:
        console.print(f"[red]Error: {e}[/red]")
    time.sleep(2)
    osint_menu()

def osint_menu():
    """Menü für OSINT & Recon"""
    print_category_header("OSINT & Recon")
    menu = Panel(
        Text(
            "[1] IP Lookup   |  [2] DNS Lookup\n"
            "[3] WHOIS Lookup|  [4] IP Geolocation\n"
            "[0] Back",
            style="cyan"
        ),
        title="[bold blue]OSINT & Recon Menu[/bold blue]",
        border_style="blue",
        width=70
    )
    console.print(menu, justify="center")
    choice = Prompt.ask("╚═> ", choices=["0", "1", "2", "3", "4"], default="0")
    if choice == "1":
        osint_ip_lookup()
    elif choice == "2":
        osint_dns_lookup()
    elif choice == "3":
        osint_whois_lookup()
    elif choice == "4":
        osint_geolocation()
    else:
        main_menu()

# ========================== PENTESTING ==========================

def pentest_nmap_scan():
    """Funktion: Nmap Scan"""
    print_category_header("Nmap Scan")
    target = Prompt.ask("Enter target IP or domain for Nmap scan")
    try:
        result = subprocess.run(["nmap", "-sV", target], capture_output=True, text=True)
        console.print(Panel(result.stdout, title="[bold blue]Nmap Scan Result[/bold blue]", border_style="green"))
    except FileNotFoundError:
        console.print("[red]Error: nmap not found. Please install nmap and ensure it's in your PATH.[/red]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
    time.sleep(2)
    pentest_menu()

def pentest_exploit_search():
    """Funktion: Exploit Search (Platzhalter)"""
    print_category_header("Exploit Search")
    target = Prompt.ask("Enter target IP or domain for vulnerability search")
    try:
        response = requests.get(f"https://www.cvedetails.com/vulnerability-list/vendor_id-0/product_id-0/version_id-0/CVE-Details.html?search={target}")
        if response.status_code == 200:
            console.print("[green]Exploits found for target![/green]")
            console.print(response.text)
        else:
            console.print("[red]No exploits found for the target.[/red]")
    except requests.exceptions.RequestException as e:
        console.print(f"[red]Error: {e}[/red]")
    time.sleep(2)
    pentest_menu()

def pentest_menu():
    """Menü für Pentesting"""
    print_category_header("Pentesting")
    menu = Panel(
        Text(
            "[1] Nmap Scan   |  [2] Exploit Search\n"
            "[0] Back",
            style="cyan"
        ),
        title="[bold blue]Pentesting Menu[/bold blue]",
        border_style="blue",
        width=70
    )
    console.print(menu, justify="center")
    choice = Prompt.ask("╚═> ", choices=["0", "1", "2"], default="0")
    if choice == "1":
        pentest_nmap_scan()
    elif choice == "2":
        pentest_exploit_search()
    else:
        main_menu()

# ========================== DISCORD TOOLS ==========================

def discord_webhook_spammer():
    """Funktion: Discord Webhook Spammer"""
    print_category_header("Webhook Spammer")
    webhook_url = Prompt.ask("Enter Webhook URL")
    message = Prompt.ask("Enter message to spam")
    count = int(Prompt.ask("How many messages?"))
    for _ in range(count):
        try:
            requests.post(webhook_url, json={"content": message})
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            break
    console.print("[green]Spamming completed![/green]")
    time.sleep(2)
    discord_menu()

def discord_token_checker():
    """Funktion: Discord Token Checker"""
    print_category_header("Token Checker")
    token = Prompt.ask("Enter Discord token")
    headers = {"Authorization": token}
    try:
        response = requests.get("https://discord.com/api/v9/users/@me", headers=headers)
        if response.status_code == 200:
            console.print("[green]Valid Token![/green]")
        else:
            console.print("[red]Invalid Token![/red]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
    time.sleep(2)
    discord_menu()

def discord_menu():
    """Menü für Discord Tools"""
    print_category_header("Discord Tools")
    menu = Panel(
        Text(
            "[1] Webhook Spammer   |  [2] Token Checker\n"
            "[0] Back",
            style="cyan"
        ),
        title="[bold blue]Discord Tools Menu[/bold blue]",
        border_style="blue",
        width=70
    )
    console.print(menu, justify="center")
    choice = Prompt.ask("╚═> ", choices=["0", "1", "2"], default="0")
    if choice == "1":
        discord_webhook_spammer()
    elif choice == "2":
        discord_token_checker()
    else:
        main_menu()

# ========================== EXPLOIT FINDER ==========================

def exploit_finder_menu():
    """Platzhalter: Exploit Finder"""
    print_category_header("Exploit Finder")
    console.print(Panel("[yellow]Exploit Finder kommt bald![/yellow]", border_style="green"), justify="center")
    time.sleep(2)
    main_menu()

# ========================== STEALTH TOOLS ==========================

def stealth_tools_menu():
    """Menü für Stealth Tools"""
    print_category_header("Stealth Tools")
    menu = Panel(
        Text("[1] Use Tor for IP Anonymity\n[0] Back", style="cyan"),
        title="[bold blue]Stealth Tools Menu[/bold blue]",
        border_style="blue",
        width=70
    )
    console.print(menu, justify="center")
    choice = Prompt.ask("╚═> ", choices=["0", "1"], default="0")
    if choice == "1":
        console.print("[green]Switching to Tor for anonymous browsing...[/green]")
        time.sleep(2)
    main_menu()

# ========================== MAIN MENU ==========================

def main_menu():
    """Hauptmenü des Tools"""
    clear_screen()
    # Hauptbanner oben (mit Gradient von Blau zu Weiß)
    console.print(Panel(gradient_text(BANNER_TEXT), expand=False), justify="center")
    
    # Menü-Panel (zentriert)
    menu = Panel(
        Text(
            "[1] OSINT & Recon   |  [2] Pentesting   |  [3] Discord Tools\n"
            "[4] Exploit Finder |  [5] Stealth Tools\n"
            "[0] Exit",
            style="cyan"
        ),
        title="[bold blue]Main Menu[/bold blue]",
        border_style="cyan",
        width=70
    )
    console.print(menu, justify="center")
    
    # main menu
    console.print(Panel(f"[blue]{MAIN_BANNER}[/blue]", expand=False), justify="center")
    
    try:
        choice = Prompt.ask("╚═>[~FED{@ROOT}] ", default="0")
        handle_choice(choice)
    except KeyboardInterrupt:
        console.print("\n[red]User interrupted. Exiting...[/red]")
        time.sleep(1)
        exit()

def handle_choice(choice):
    """Verarbeitet die Menüauswahl im Hauptmenü"""
    if choice == "0":
        console.print("[red]Exiting...[/red]")
        time.sleep(1)
        exit()
    elif choice == "1":
        osint_menu()
    elif choice == "2":
        pentest_menu()
    elif choice == "3":
        discord_menu()
    elif choice == "4":
        exploit_finder_menu()
    elif choice == "5":
        stealth_tools_menu()
    else:
        console.print(f"[green]Selected Option: {choice} (Feature coming soon!)[/green]")
        time.sleep(1)
        main_menu()

# ========================== PROGRAMM START ==========================

if __name__ == "__main__":
    main_menu()
