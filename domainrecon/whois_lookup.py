import whois
from rich import print

def get_whois_info(domain):
    try:
        data = whois.whois(domain)
        print(f"[cyan]Domain:[/cyan] {data.domain_name}")
        print(f"[cyan]Registrar:[/cyan] {data.registrar}")
        print(f"[cyan]Registered:[/cyan] {data.creation_date}")
        print(f"[cyan]Expires at:[/cyan] {data.expiration_date}")
    except Exception as e:
        print(f"[red]Could not parse WHOIS-info:[/red] {e}")