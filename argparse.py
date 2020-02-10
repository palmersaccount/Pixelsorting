import argparse

# arg parsing arguments
def args():
    parse = argparse.ArgumentParser(description="pixel mangle an image")
    parse_util = argparse.ArgumentParser(description="misc. args used in program")
    """
    (Taken args)
    //user read//
    :-t,--bottom_threshold -> bottom/lower threshold
    :-u,--upper_threshold -> top/upper threshold
    :-c,--clength -> character length
    :-a,--angle -> angle for rotation
    :-r,--randomness -> randomness

    //not accessible to user//
    :-l,--url -> url
    :-i,--int_function -> interval function
    :-s,--sorting_function -> sorting function
    :-p --preset -> is preset used
    :-d --dbpreset -> is dbpreset used
    :-y --internet -> is internet there
    :-k --filelink -> for DBpreset
    :-b --presetname -> name of preset used
    """
    parse.add_argument(
        "-t",
        "--bottom_threshold",
        type=float,
        help="Pixels darker than this are not sorted, between 0 and 1",
        default=0.25,
    )
    parse.add_argument(
        "-u",
        "--upper_threshold",
        type=float,
        help="Pixels darker than this are not sorted, between 0 and 1",
        default=0.8,
    )
    parse.add_argument(
        "-c",
        "--clength",
        type=int,
        help="Characteristic length of random intervals",
        default=50,
    )
    parse.add_argument(
        "-a",
        "--angle",
        type=float,
        help="Rotate the image by an angle (in degrees) before sorting",
        default=0,
    )
    parse.add_argument(
        "-r",
        "--randomness",
        type=float,
        help="What percentage of intervals are NOT sorted",
        default=10,
    )

    # not accessible to user
    parse_util.add_argument(
        "-l",
        "--url",
        help="URL of a given image. Used as the input image.",
        default="https://s.put.re/QsUQbC1R.jpg",
    )
    parse_util.add_argument(
        "-i",
        "--int_function",
        help="random, threshold, edges, waves, snap, shuffle-total, shuffle-axis, file, file-edges, none",
        default="random",
    )
    parse_util.add_argument(
        "-s",
        "--sorting_function",
        help="lightness, intensity, hue, saturation, minimum",
        default="lightness",
    )
    parse_util.add_argument(
        "-p",
        "--preset",
        type=bool,
        help="Is a preset used or not? Boolean.",
        default=False,
    )
    parse_util.add_argument(
        "-d",
        "--dbpreset",
        help="Boolean for if preset is used or not.",
        type=bool,
        default=False,
    )
    parse_util.add_argument(
        "-y",
        "--internet",
        help="Boolean for if internet is preset or not.",
        type=bool,
        default=True,
    )
    parse_util.add_argument(
        "-b", "--presetname", help="Name of the preset used.", default="None"
    )
    parse_util.add_argument(
        "-k", "--filelink", help="File image used, only in DB preset mode.", default=""
    )

    return parse, parse_util
