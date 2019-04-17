from os import remove
import argparse
import asyncio
from pyppeteer import launch, connect


def set_endpoint(ws_endpoint):
    with open("endpointlist.txt", "a") as f:
        f.write(ws_endpoint + "\n")


def get_endpoints():
    endpoint_list = []
    try:
        with open("endpointlist.txt", "r") as f:
            for line in f:
                line = line.split()[0]
                endpoint_list.append(line)
        remove("endpointlist.txt")
        print(endpoint_list)
        return endpoint_list
    except:
        print("No browser in the 'endpointlist.txt' file to be closed")
        exit(-1)


async def open_browser(is_headless=True):
    browser = await launch(headless=is_headless, autoClose=False)
    endpoint = browser.wsEndpoint
    set_endpoint(endpoint)
    return endpoint


async def delete_browser(ws_endpoint_list):
    for ws_endpoint in ws_endpoint_list:
        browser = await connect(browserWSEndpoint=ws_endpoint)
        await browser.close()


async def do_it(args):
    if args.close:
        await delete_browser(get_endpoints())
    if args.open:
        await open_browser(is_headless=args.headless)


def arg_parsing():
    parser = argparse.ArgumentParser(description="Create or close a browser")
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-c", "--close", action="store_true", help="""Close the browser
		with the WS_ENDPOINT_SCREAMSHOT websocket endpoint """)
    group.add_argument(
        "-o", "--open", action="store_true", help="""Open a browser and store its websocket
		endpoint in the WS_ENDPOINT_SCREAMSHOT shell variable """)
    parser.add_argument("-g", "--graphic", dest="headless", action="store_false",
                        help="""Open the browser in graphic mode""")

    args = parser.parse_args()
    asyncio.get_event_loop().run_until_complete(do_it(args))


arg_parsing()
