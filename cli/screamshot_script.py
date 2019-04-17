from argparse import ArgumentParser


def do_it(args):
    print("URL : " + args.url)
    print("Path : " + args.path)
    print("fullPage : " + str(args.fullpage))
    if args.width:
        print("width : " + str(args.width))
    if args.height:
        print("height : " + str(args.height))


def argParsing():
    parser = ArgumentParser(description="Take a screenshot")
    parser.add_argument("url", help="url to screenshot")
    parser.add_argument("path", help="path to image to be written")
    parser.add_argument("-f", "--fullpage", action="store_true",
                        help="Take a screenshot of the whole scrollable page")
    parser.add_argument("--width", type=int, help="Set the width of the page")
    parser.add_argument("--height", type=int,
                        help="Set the height of the page")

    args = parser.parse_args()
    do_it(args)


argParsing()
