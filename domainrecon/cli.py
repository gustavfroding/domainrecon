import argparse
from rich import print
from domainrecon.whois_lookup import get_whois_info
from domainrecon.dns_lookup import get_dns_info
from domainrecon.cert_lookup import get_cert_subdomains
import asyncio


def main():
    parser = argparse.ArgumentParser(
        prog="domainrecon",
        description="Map the tech stack of a domain using WHOIS, DNS, certificates, etc.",
    )
    parser.add_argument("domain", help="Domain to analyze")
    parser.add_argument("--whois", action="store_true", help="Show WHOIS information")
    parser.add_argument("--dns", action="store_true", help="Show DNS information (A, MX, TXT, etc.)")
    parser.add_argument("--certs", action="store_true", help="Enumerate subdomains via crt.sh")
    parser.add_argument("--all", action="store_true", help="Run all modules")

    args = parser.parse_args()

    if not any([args.whois, args.dns, args.certs, args.all]):
        parser.print_help()
        return

    async def run():
        if args.all or args.whois:
            print("[bold green]\n[ WHOIS Information ]\n")
            get_whois_info(args.domain)
        if args.all or args.dns:
            print("[bold blue]\n[ DNS Information ]\n")
            await get_dns_info(args.domain)
        if args.all or args.certs:
            print("[bold magenta]\n[ Subdomains from crt.sh ]\n")
            await get_cert_subdomains(args.domain)

    asyncio.run(run())