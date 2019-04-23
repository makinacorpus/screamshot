from argparse import ArgumentParser

from screamshot.utils import get_endpoint, close_browser, open_browser, to_sync


async def do_it(args):
    """
    Figures out what to do with the arguments
    :param args: the parsed arguments
    :type args: argparse.Namespace class
    """
    if args.close:
        await close_browser(get_endpoint())
    if args.open:
        await open_browser(args.headless, no_sandbox_arg=args.no_sandbox)


def _arg_parsing():
    parser = ArgumentParser(description="Create or close a browser")

    # Mandatory arguments
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-c", "--close", action="store_true", help="""Close the browsers
		in the endpointlist.txt file""")
    group.add_argument(
        "-o", "--open", action="store_true", help="""Open a browser and store its websocket
		endpoint in endpointlist.txt """)

    # Optionnal argument
    parser.add_argument("-g", "--graphic", dest="headless", action="store_false",
                        help="""Open the browser in graphic mode""")
    parser.add_argument('-ns', "--no-sandbox",
                        action="store_const", const=["--no-sandbox"], help="Desactivate sandbox")

    args = parser.parse_args()
    return args


def main():
    """
    Open or close a browser
    """
    args = _arg_parsing()
    to_sync(do_it(args))


if __name__ == '__main__':
    main()
