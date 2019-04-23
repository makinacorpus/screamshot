"""
Take a screenshot
"""
from argparse import ArgumentParser

from screamshot import generate_bytes_img
from screamshot.utils import to_sync


def _arg_parsing():
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
                        help="How long do you want to wait for the page to be loaded")

    selector_group = parser.add_argument_group(title="CSS3 selectors (optional)",
                                               description="Using quotes is recommended for \
                                                   complex CSS3 selectors")
    selector_group.add_argument("--selector", metavar="seletor",
                                help="The CSS3 selector of the element you want in the screenshot")

    selector_group.add_argument("--wait_for", metavar="wait_for_selector",
                                help="The CSS3 selector of an element you want to wait to be \
                                    loaded before taking the screenshot")

    return parser.parse_args()


def main():
    args = _arg_parsing()
    if args.wait_until:
        to_sync(generate_bytes_img(args.url,
                                   path=args.path,
                                   width=args.width, height=args.height,
                                   full_page=args.fullpage,
                                   selector=args.selector,
                                   wait_for=args.wait_for,
                                   wait_until=args.wait_until))
    else:
        to_sync(generate_bytes_img(args.url,
                                   path=args.path,
                                   width=args.width, height=args.height,
                                   full_page=args.fullpage,
                                   selector=args.selector,
                                   wait_for=args.wait_for))


if __name__ == '__main__':
    main()
