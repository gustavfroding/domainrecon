import aiohttp
from rich import print
from rich.table import Table
import asyncio
import dns.asyncresolver
from ipwhois import IPWhois
from domainrecon.web_tech import inspect_https_site

async def resolve_asn(ip):
    try:
        obj = IPWhois(ip)
        data = obj.lookup_rdap()
        asn = data.get('asn')
        org = data.get('network', {}).get('name')
        return (ip, asn, org)
    except Exception as e:
        return (ip, "Error", str(e))

async def get_cert_subdomains(domain):
    url = f"https://crt.sh/?identity={domain}&output=json&exclude=expired"
    seen = set()
    resolver = dns.asyncresolver.Resolver()
    table = Table()
    table.add_column("Domain", style="cyan")
    table.add_column("IP", style="green")
    table.add_column("ASN", style="yellow")
    table.add_column("Organization", style="magenta")
    table.add_column("HTTPS", style="bold")
    table.add_column("Code", style="bold")
    table.add_column("Server", style="dim")
    table.add_column("Powered-By", style="dim")
    table.add_column("Framework", style="bold magenta")

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=20) as resp:
                if resp.status != 200:
                    print(f"[red]Error fetching data from crt.sh: {resp.status}[/red]")
                    return

                data = await resp.json()
                for entry in data:
                    names = entry.get("name_value", "").split("\n")
                    for name in names:
                        name = name.strip().lower()
                        if name.endswith(domain):
                            seen.add(name)

        async def process_subdomain(sub):
            try:
                a_records = await resolver.resolve(sub, 'A')
                ip = a_records[0].to_text()
                ip, asn, org = await resolve_asn(ip)
                https_ok, status, server, powered_by, tech = await inspect_https_site(sub)
                table.add_row(sub, ip, asn or "-",  org or "-",  "✅" if https_ok else "❌", str(status), server or "-", powered_by or "-", tech or "-")
            except Exception as e:
                table.add_row(sub, "-", "-", "-", "-", "-", "-", "-", f"SSL fel: {e}")

        await asyncio.gather(*(process_subdomain(sub) for sub in sorted(seen)))
        print(table)

    except Exception as e:
        print(f"[red]Error getting data from crt.sh: [/red] {e}")
