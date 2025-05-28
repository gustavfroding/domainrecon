import dns.asyncresolver
from rich import print
from ipwhois import IPWhois
import asyncio

async def resolve_asn(ip):
    try:
        obj = IPWhois(ip)
        data = obj.lookup_rdap()
        asn = data.get('asn')
        org = data.get('network', {}).get('name')
        return (ip, asn, org)
    except Exception as e:
        return (ip, "Error", str(e))

async def get_dns_info(domain):
    resolver = dns.asyncresolver.Resolver()

    # A records
    try:
        a_records = await resolver.resolve(domain, 'A')
        print("[yellow]A records:[/yellow]")
        for r in a_records:
            ip = r.to_text()
            ip, asn, org = await resolve_asn(ip)
            print(f"  {ip} (ASN: {asn}, Org: {org})")
    except Exception as e:
        print(f"[red]No A records found:[/red] {e}")

    # MX records + first A record for each
    try:
        mx_records = await resolver.resolve(domain, 'MX')
        print("[yellow]MX records:[/yellow]")
        for r in mx_records:
            mx_host = r.exchange.to_text().rstrip('.')
            print(f"  MX: {mx_host}")
            try:
                mx_a_records = await resolver.resolve(mx_host, 'A')
                if mx_a_records:
                    ip = mx_a_records[0].to_text()
                    ip, asn, org = await resolve_asn(ip)
                    print(f"    {ip} (ASN: {asn}, Org: {org})")
            except Exception as e:
                print(f"    [red]Could not resolve A record for {mx_host}:[/red] {e}")
    except Exception as e:
        print(f"[red]No MX records found:[/red] {e}")

    # TXT records
    try:
        txt_records = await resolver.resolve(domain, 'TXT')
        print("[yellow]TXT records:[/yellow]")
        for r in txt_records:
            print(f"  {r.to_text()}")
    except Exception as e:
        print(f"[red]No TXT records found:[/red] {e}")