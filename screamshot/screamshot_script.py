"""
Take a screenshot
"""
from argparse import ArgumentParser
from logging import getLogger
from re import search

from screamshot import generate_bytes_img
from screamshot.utils import to_sync, open_browser, close_browser


logger = getLogger('screamshot')


def main():
    parser = ArgumentParser(description=__doc__)

    # Mandatory arguments
    parser.add_argument("url", help="url to screenshot")

    parser.add_argument("path", help="path to image to be written")

    # Optionnal arguments
    parser.add_argument("-f", "--fullpage", action="store_true",
                        help="Take a screenshot of the whole scrollable page")

    parser.add_argument("--width", type=int, metavar="width", default=800,
                        help="Set the width of the page")

    parser.add_argument("--height", type=int, metavar="height", default=600,
                        help="Set the height of the page")

    parser.add_argument("--wait_until", nargs="+", type=str,
                        choices=["load", "domcontentloaded",
                                 "networkidle0", "networkidle2"],
                        default="load",
                        help="How long do you want to wait for the page to be loaded")

    # Credentials group
    credentials_group = parser.add_argument_group(title="Credentials (optional)")
    credentials_group.add_argument('--username', help='The username to use')
    credentials_group.add_argument('--password', help='The password to use')
    credentials_group.add_argument('--token', help='The header line to add. \
        Must be like the following expression: key:token')

    # CSS3 selectors group
    selector_group = parser.add_argument_group(title="CSS3 selectors (optional)",
                                               description="Using quotes is recommended for \
                                                   complex CSS3 selectors")
    selector_group.add_argument("--selector", metavar="seletor",
                                help="The CSS3 selector of the element you want in the screenshot")

    selector_group.add_argument("--wait_for", metavar="wait_for_selector",
                                help="The CSS3 selector of an element you want to wait to be \
                                    loaded before taking the screenshot")

    # Browser group
    browser_group = parser.add_argument_group(title='Browser (optional)',
                                              description='By default a headless browser is \
                                                  opened and closed')
    browser_group.add_argument('--no-browser', action='store_true', default=False,
                               help='No browser is opened')
    browser_group.add_argument('-g', '--graphic', dest="headless", action="store_false",
                               default=True, help="Open the browser in graphic mode")
    browser_group.add_argument("--no-sandbox", action="store_const", const=["--no-sandbox"],
                               default="[]", help="Open the browser without sandbox")
    browser_group.add_argument('--no-close', action='store_true', default=False,
                               help='The browser is not closed when the job is done')

    args = parser.parse_args()

    credentials = None
    if args.username and not args.password:
        logger.error('A password must be specified')
        exit(1)
    elif not args.username and args.password:
        logger.error('A username must be specified')
        exit(1)
    elif args.username and args.password:
        credentials = {'username': args.username, 'password': args.password}
    elif args.token:
        regex_token = search(r'(?P<key>[^<]+)\:(?P<token>[^<]+)', args.token)
        try:
            key = regex_token.group('key')
            token = regex_token.group('token')
            credentials = {key: token, 'token_in_header': True}
        except AttributeError as _:
            logger.error('Bad token argument, please read the documentation')
            exit(1)

    if not args.no_browser:
        to_sync(
            open_browser(args.headless, launch_args=args.no_sandbox))

    to_sync(
        generate_bytes_img(args.url, path=args.path, width=args.width, height=args.height,
                           full_page=args.fullpage, selector=args.selector,
                           wait_for=args.wait_for, wait_until=args.wait_until,
                           credentials=credentials))

    if not args.no_browser and not args.no_close:
        to_sync(close_browser())


if __name__ == '__main__':
    main()
