"""
Create or close a browser
"""
from argparse import ArgumentParser

from screamshot.utils import close_browser, open_browser, to_sync


def main():
    parser = ArgumentParser(description=__doc__)

    # Mandatory arguments
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-c", "--close", action="store_true", help="Close the browsers in the \
        endpointlist.txt file")
    group.add_argument("-o", "--open", action="store_true", help="Open a browser and store its \
        websocket endpoint in endpointlist.txt")

    # Optionnal argument
    parser.add_argument("-g", "--graphic", dest="headless", action="store_false", help="Open the \
        browser in graphic mode")

    parser.add_argument("-ns", "--no-sandbox", action="store_const", const=["--no-sandbox"],
                        default="[]", help="Open the browser without sandbox")

    args = parser.parse_args()

    if args.close:
        to_sync(close_browser())
    if args.open:
        to_sync(open_browser(args.headless, launch_args=args.no_sandbox))


if __name__ == '__main__':
    main()
