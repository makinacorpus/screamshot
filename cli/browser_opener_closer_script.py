from argparse import ArgumentParser

from browser_manager import get_endpoints, delete_browser, open_browser, to_sync


# Figures out what to do with the arguments
async def do_it(args):
    if args.close:
        await delete_browser(get_endpoints())
    if args.open:
        await open_browser(args.headless)


# The name is expressive enought I guess, uses argparse
def arg_parsing():
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
    # Calls the function to use the arguments using asyncio to handle the asynchronous function used
    to_sync(do_it(args))


arg_parsing()
