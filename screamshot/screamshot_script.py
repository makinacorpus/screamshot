"""
Take a screenshot
"""
from argparse import ArgumentParser

from screamshot import generate_bytes_img
from screamshot.utils import to_sync, open_browser, close_browser


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

    if not args.no_browser:
        to_sync(
            open_browser(args.headless, launch_args=args.no_sandbox))

    to_sync(
        generate_bytes_img(args.url, path=args.path, width=args.width, height=args.height,
                           full_page=args.fullpage, selector=args.selector,
                           wait_for=args.wait_for, wait_until=args.wait_until))

    if not args.no_browser and not args.no_close:
        to_sync(close_browser())


if __name__ == '__main__':
    main()
