from argparse import ArgumentParser

from screamshot.utils import get_endpoint, delete_browser, open_browser, to_sync


async def _execute(args):
    if args.close:
        await delete_browser(get_endpoint())
    if args.open:
        await open_browser(args.headless)


def _parse_arg():
    parser = ArgumentParser(description="Create or close a browser")
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-c", "--close", action="store_true", help="""Close the browsers
		in the endpointlist.txt file""")
    group.add_argument(
        "-o", "--open", action="store_true", help="""Open a browser and store its websocket
		endpoint in endpointlist.txt """)
    parser.add_argument("-g", "--graphic", dest="headless", action="store_false",
                        help="""Open the browser in graphic mode""")

    args = parser.parse_args()
    return args


def main():
    args = _parse_arg()
    to_sync(_execute(args))


if __name__ == '__main__':
    main()
