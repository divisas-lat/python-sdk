import argparse
import sys
from .client import DivisasClient
from .enums import Country, Currency
from .exceptions import DivisasException


def main():
    parser = argparse.ArgumentParser(description="Divisas.lat CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Command: today
    parser_today = subparsers.add_parser("today", help="Get today's exchange rate")
    parser_today.add_argument("country", type=str, help="Country code (e.g., GT, MX)")
    parser_today.add_argument("currency", type=str, nargs="?", help="Optional base currency (e.g., USD)")

    # Command: convert
    parser_convert = subparsers.add_parser("convert", help="Convert currencies")
    parser_convert.add_argument("amount", type=float, help="Amount to convert")
    parser_convert.add_argument("from_currency", type=str, help="Currency to convert from (e.g., USD)")
    parser_convert.add_argument("to", type=str, help="Literal word 'to'")
    parser_convert.add_argument("to_currency", type=str, help="Currency to convert to (e.g., GTQ)")
    parser_convert.add_argument("in_word", type=str, help="Literal word 'in'")
    parser_convert.add_argument("country", type=str, help="Country context (e.g., GT)")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    client = DivisasClient()

    try:
        if args.command == "today":
            try:
                country = Country(args.country.upper())
            except ValueError:
                print(f"Error: Invalid country code '{args.country}'.")
                sys.exit(1)

            query = client.query().for_country(country)
            
            if args.currency:
                try:
                    currency = Currency(args.currency.upper())
                    query.with_currency(currency)
                except ValueError:
                    print(f"Error: Invalid currency code '{args.currency}'.")
                    sys.exit(1)

            res = query.get_today()
            print(f"Country: {res.country} | Base: {res.base_currency} | Date: {res.date}")
            print(f"Rate: {res.rate.currency_code} - Buy: {res.rate.buy:.2f} / Sell: {res.rate.sell:.2f}")

        elif args.command == "convert":
            if args.to.lower() != "to" or args.in_word.lower() != "in":
                print("Usage: divisas convert <AMOUNT> <FROM> to <TO> in <COUNTRY>")
                sys.exit(1)
                
            try:
                country = Country(args.country.upper())
                from_c = Currency(args.from_currency.upper())
                to_c = Currency(args.to_currency.upper())
            except ValueError as e:
                print(f"Error: {str(e)}")
                sys.exit(1)

            res = client.query()\
                .for_country(country)\
                .with_currency(from_c)\
                .convert(to_c, args.amount)

            print(f"Conversion: {res.amount:.2f} {res.from_.currency} -> {res.result:.2f} {res.to.currency}")
            print(f"Effective Rate: {res.effective_rate:.2f} (Via {res.via})")

    except DivisasException as e:
        print(f"API Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
