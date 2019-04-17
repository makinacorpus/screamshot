from os import remove
import argparse
import asyncio
from pyppeteer import launch, connect


FILENAME_ENDPOINT = "endpointlist.txt"


# Write the websocket endpoint into the file
def set_endpoint(ws_endpoint):
    with open(FILENAME_ENDPOINT, "a") as f:
        f.write(ws_endpoint + "\n")
    return ws_endpoint


# Read the file to get the ws endpoints and return them into a list of string
def get_endpoints():
    endpoint_list = []
    try:
        with open(FILENAME_ENDPOINT, "r") as f:
            for line in f:
                line = line.split()[0]
                endpoint_list.append(line)
        remove(FILENAME_ENDPOINT)
        return endpoint_list
    except FileNotFoundError:
        print(FILENAME_ENDPOINT + " not found")
        exit(-1)


# Launch a browser which will be closed only when delete_browser(ws_endpoint_list) is called
async def open_browser(is_headless):
    browser = await launch(headless=is_headless, autoClose=False)
    endpoint = browser.wsEndpoint
    set_endpoint(endpoint)
    return endpoint


# Close all the browsers in the ws_endpoint_list
async def delete_browser(ws_endpoint_list):
    for ws_endpoint in ws_endpoint_list:
        browser = await connect(browserWSEndpoint=ws_endpoint)
        await browser.close()


# Figures out what to do with the arguments
async def do_it(args):
    if args.close:
        await delete_browser(get_endpoints())
    if args.open:
        await open_browser(args.headless)


# The name is expressive enought I guess, uses argparse
def arg_parsing():
    parser = argparse.ArgumentParser(description="Create or close a browser")
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
    asyncio.get_event_loop().run_until_complete(do_it(args))


arg_parsing()
