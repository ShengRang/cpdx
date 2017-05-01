# coding: utf-8

import c
import cpp


def parser_dispatch(lang="cpp"):
    """ Return an cls of spec parser
    """
    parser_cls = {
        "cpp": cpp.Parser,
        "c": c.Parser,
    }.get(lang)
    return parser_cls