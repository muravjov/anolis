#!/usr/bin/env python
# coding=UTF-8
# Copyright (c) 2008 Geoffrey Sneddon
#           (c) 2011 Ms2ger
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""anolis [options] [input] [output]

Post-process a document, adding cross-references, table of contents, etc.
"""

from __future__ import unicode_literals

import sys
from argparse import ArgumentParser, SUPPRESS

from lxml import etree

from anolislib import generator, utils


def main():
    # Create the options parser
    optParser = getOptParser()
    args = optParser.parse_args()

    if args.input:
        try:
            input = open(args.input, "rb")
        except IOError as e:
            sys.stderr.write(str(e) + "\n")
            sys.exit(1)
    else:
        input = sys.stdin

    if args.output:
        try:
            output = open(args.output, "wb")
        except IOError as e:
            sys.stderr.write(str(e) + "\n")
            sys.exit(1)
    else:
        output = sys.stdout

    try:
        # Get options
        kwargs = vars(args)
        del kwargs['input']
        del kwargs['output']

        # Get input and generate

        tree = generator.fromFile(input, **kwargs)
        input.close()

        # Write output
        generator.toFile(tree, output, **kwargs)
        output.close()
    except (utils.AnolisException, IOError, etree.XMLSyntaxError) as e:
        sys.stderr.write(str(e) + "\n")
        sys.exit(1)


def getOptParser():
    parser = ArgumentParser(usage=__doc__)
    parser.add_argument('--version', action='version', version="%(prog)s 1.3pre")

    parser.add_argument("input", type=str, nargs='?',
                        help="Input file. Defaults to stdin.")

    parser.add_argument("output", type=str, nargs='?',
                        help="Output file. Defaults to stdout.")

    parser.add_argument("--enable", type=str, dest="processes",
                        action="append",
                        help="Enable the process given as the option value")

    parser.add_argument("--disable", type=str, action="append",
                        help="Disable the process given as the option value")

    parser.add_argument("--parser", type=str,
                        choices=("html5lib", "lxml.html"),
                        help="Choose what parser to use.")

    parser.add_argument("--serializer", type=str,
                        choices=("html5lib", "lxml.html"),
                        help="Choose what serializer to use.")

    parser.add_argument("--newline-char", action="store", type=str,
                        dest="newline_char",
                        help="Set the newline character/string used when "
                             "creating new newlines. This should match the "
                             "rest of the newlines in the document.")

    parser.add_argument("--indent-char", action="store", type=str,
                        dest="indent_char",
                        help="Set the character/string used when creating "
                             "indenting new blocks of (X)HTML. This should "
                             "match the rest of the indentation in the "
                             "document.")

    parser.add_argument("--filter", action="store", dest="filter",
                        help="CSS selector that matches elements to be "
                             "removed from the document before processing")

    parser.add_argument("--annotations", action="store", dest="annotation",
                        help="Path or URI of an annotations file containing "
                             "status annotations that should be added to "
                             "sections")

    parser.add_argument("--annotate-whatwg-status", action="store_true",
                        dest="annotate_whatwg_status",
                        help="Add WHATWG status markers in annotations")

    parser.add_argument("--annotate-w3c-issues", action="store_true",
                        dest="annotate_w3c_issues",
                        help="Add links to W3C issue tracker in status "
                             "annotations")

    parser.add_argument("--force-html4-id", action="store_true",
                        dest="force_html4_id",
                        help="Force the ID generation algorithm to create "
                             "HTML 4 compliant IDs regardless of the DOCTYPE.")

    parser.add_argument("--min-depth", action="store", type=int,
                        dest="min_depth",
                        help="Highest ranking header to number/insert into "
                             "TOC.")

    parser.add_argument("--max-depth", action="store", type=int,
                        dest="max_depth",
                        help="Lowest ranking header to number/insert into "
                             "TOC.")

    parser.add_argument("--allow-duplicate-dfns", action="store_true",
                        dest="allow_duplicate_dfns",
                        help="Allow multiple definitions of terms when "
                             "cross-referencing (the last instance of the "
                             "term is used when referencing it).")

    parser.add_argument("--xref", action="store", dest="xref",
                        help="Set directory for cross-references database "
                             "without trailing slash. E.g. '../xref'")

    profile = True
    try:
        import cProfile
        import pstats
    except ImportError:
        try:
            import hotshot
            import hotshot.stats
        except ImportError:
            profile = False

    if profile:
        parser.add_argument("--profile", action="store_true",
                            dest="profile", help=SUPPRESS)

    parser.add_argument("--inject-meta-charset", action="store_true",
                        dest="inject_meta_charset", help=SUPPRESS)

    parser.add_argument("--strip-whitespace", action="store_true",
                        dest="strip_whitespace", help=SUPPRESS)

    parser.add_argument("--omit-optional-tags", action="store_true",
                        dest="omit_optional_tags", help=SUPPRESS)

    parser.add_argument("--quote-attr-values", action="store_true",
                        dest="quote_attr_values", help=SUPPRESS)

    parser.add_argument("--use-best-quote-char", action="store_true",
                        dest="use_best_quote_char", help=SUPPRESS)

    parser.add_argument("--no-minimize-boolean-attributes",
                        action="store_false",
                        dest="minimize_boolean_attributes", help=SUPPRESS)

    parser.add_argument("--use-trailing-solidus", action="store_true",
                        dest="use_trailing_solidus", help=SUPPRESS)

    parser.add_argument("--space-before-trailing-solidus",
                        action="store_true",
                        dest="space_before_trailing_solidus", help=SUPPRESS)

    parser.add_argument("--escape-lt-in-attrs", action="store_true",
                        dest="escape_lt_in_attrs", help=SUPPRESS)

    parser.add_argument("--escape-rcdata", action="store_true",
                        dest="escape_rcdata", help=SUPPRESS)

    parser.add_argument("--no-alphabetical-attributes", action="store_false",
                        dest="alphabetical_attributes", help=SUPPRESS)

    parser.add_argument("--output-encoding", action="store", type=str,
                        dest="output_encoding", help="Output encoding")

    parser.add_argument("--dump-refs", action="store", type=str,
                        dest="dump_refs", help=SUPPRESS)

    parser.add_argument("--dump-xrefs", action="store", type=str,
                        dest="dump_xrefs", help=SUPPRESS)

    parser.add_argument("--use-strict", action="store_true",
                        dest="use_strict", help=SUPPRESS)

    parser.add_argument("--xref-use-a", action="store_true",
                        dest="xref_use_a", help=SUPPRESS)

    parser.add_argument("--pubdate", action="store", type=str,
                        dest="publication_date", metavar="1 Sep 2022",
                        help="Set the date this document will be published.")

    parser.add_argument("--localtime", action="store_true", dest="localtime",
                        help="Use local time for the publication date.")

    parser.add_argument("--dump-backrefs", action="store_true",
                        dest="dump_backrefs", help=SUPPRESS)

    parser.add_argument("--enable-woolly", action="store_true",
                        dest="enable_woolly", help=SUPPRESS)

    parser.add_argument("--w3c-compat", action="store_true",
                        dest="w3c_compat",
                        help="Behave in a (mostly) compatible way to the "
                             "W3C CSS WG's Postprocessor (this implies all of "
                             "the other --w3c-compat options with the "
                             "exception of --w3c-compat-crazy-substitution, "
                             "as that is too crazy).")

    parser.add_argument("--w3c-compat-xref-elements", action="store_true",
                        dest="w3c_compat_xref_elements",
                        help="Uses the same list of elements to look for "
                             "cross-references in as the W3C CSS WG's "
                             "Postprocessor, even when the elements shouldn't "
                             "semantically be used for cross-reference terms.")

    parser.add_argument("--w3c-compat-xref-a-placement", action="store_true",
                        dest="w3c_compat_xref_a_placement",
                        help="When cross-referencing elements apart from "
                             "span, put the a element inside the element "
                             "instead of outside the element.")

    parser.add_argument("--w3c-compat-xref-normalization", action="store_true",
                        dest="w3c_compat_xref_normalization",
                        help="Only use ASCII letters, numbers, and spaces in "
                             "comparison of cross-reference terms.")

    parser.add_argument("--w3c-compat-class-toc", action="store_true",
                        dest="w3c_compat_class_toc",
                        help="Add @class='toc' on every ol element in the "
                             "table of contents (instead of only the root ol "
                             "element).")

    parser.add_argument("--w3c-compat-substitutions", action="store_true",
                        dest="w3c_compat_substitutions",
                        help="Do W3C specific substitutions.")

    parser.add_argument("--w3c-compat-crazy-substitutions",
                        action="store_true",
                        dest="w3c_compat_crazy_substitutions",
                        help="Do crazy W3C specific substitutions, which may "
                             "cause unexpected behaviour (i.e., replacing "
                             "random strings within the document with no "
                             "special marker).")

    parser.add_argument("--w3c-status", action="store", type=str,
                        dest="w3c_status", help="Status of the document")

    parser.add_argument("--w3c-shortname", action="store", type=str,
                        dest="w3c_shortname", help="Shortname of the document")

    parser.add_argument("--split-references-section", action="store_true",
                        help=SUPPRESS)

    parser.set_defaults(
        processes=["filter", "sub", "toc", "xref", "annotate"],
        parser="html5lib",
        serializer="html5lib",
        newline_char="\n",
        indent_char=" ",
        filter=None,
        annotation=None,
        annotate_whatwg_status=False,
        annotate_w3c_issues=False,
        force_html4_id=False,
        min_depth=2,
        max_depth=6,
        allow_duplicate_dfns=False,
        xref="data",
        profile=False,
        inject_meta_charset=False,
        omit_optional_tags=False,
        quote_attr_values=False,
        use_best_quote_char=False,
        minimize_boolean_attributes=False,
        use_trailing_solidus=False,
        space_before_trailing_solidus=False,
        escape_lt_in_attrs=False,
        escape_rcdata=False,
        alphabetical_attributes=True,
        output_encoding="utf-8",
        dump_refs='',
        dump_xrefs='',
        use_strict=False,
        publication_date='',
        localtime=False,
        dump_backrefs=False,
        enable_woolly=False,
        w3c_compat=False,
        w3c_compat_xref_elements=False,
        w3c_compat_xref_a_placement=False,
        w3c_compat_xref_normalization=False,
        w3c_compat_class_toc=False,
        w3c_compat_substitutions=False,
        w3c_compat_crazy_substitutions=False,
        w3c_status='ED',
        w3c_shortname='',
        split_references_section=False
    )

    return parser

if __name__ == "__main__":
    main()
