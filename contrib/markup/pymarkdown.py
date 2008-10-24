#! /usr/bin/python

# pymarkdown - text-to-html formatter.
# Copyright (C) Tollef Fog Heen, 2005
#
#    This program is free software; you can redistribute it and/or
#    modify it under the terms of the GNU General Public License
#    version 2 as published by the Free Software Foundation.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#    General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA
#    02111-1307 USA

# To use this as a pyblosxom plugin in the case that you want to use
# it for all your blog postings, just add:
#
# py['parser'] = 'markdown'
# py['load_plugins'].append("pymarkdown")
#
# to your config.py

PREFORMATTER_ID = 'markdown'
FILE_EXT = 'mdwn'

__version__ = 'pymarkdown 0.1'
__author__ = 'Tollef Fog Heen <tfheen@err.no>'

import re, md5, sys, string, random

try:
    from Pyblosxom import tools
except ImportError:
    pass

# Used by pyblosxom
def cb_preformat(args):
    if args['parser'] == PREFORMATTER_ID:
        return Markdown(''.join(args['story']))
    if args['parser'] == PREFORMATTER_ID and \
           args['request'].getData()['flavour'] == "html":
        return Markdown(''.join(args['story']))
    else:
        return ''.join(args['story']).replace("&amp;","&")

def cb_entryparser(entryparsingdict):
       """
       Register self as markdown file handler
       """
       entryparsingdict['markdown'] = Markdown
       return entryparsingdict

# Regular pymarkdown stuff.

g_urls = {}
g_titles = {}
g_html_blocks = {}
g_escape_table = {}
escapechars = r"\`*_{}[]()#.!"
g_empty_element_suffix = " />"

def sub(pattern, repl, string, count = 0, flags = None):
    if flags:
        pat = re.compile(pattern, flags)
        return pat.sub(repl, string, count)
    else:
        return re.sub(pattern, repl, string, count)

for char in escapechars:
    g_escape_table[char] = md5.new(char).hexdigest()

g_tab_width = 4

stripspace = re.compile(r"^[ \t]+$", re.MULTILINE)

def _Detab(text):
    ret = re.sub(r"(.*?)\t", "\\1", text)
    ret += " " * (g_tab_width - len(ret) % g_tab_width)
    return ret

def _HashHTMLBlocks(text):
    def handler(m):
        key = md5.new(m.group(1)).hexdigest()
        g_html_blocks[key] = m.group(1)
        return "\n\n%s\n\n" % key

    block_tags_a = r"p|div|h[1-6]|blockquote|pre|table|dl|ol|ul|script|math|ins|del"
    block_tags_b = r"p|div|h[1-6]|blockquote|pre|table|dl|ol|ul|script|math"
#    match_a = r"(^<(%s)\b(.*\n)*?</\2>[ \t]*$)" % block_tags_a
#    match_b = r"(^<(%s)\b(.*\n)*?.*</\2>[ \t]*$)" % block_tags_b
#    match_c = r"(?:(?<=\n\n)|\A\n?)([ \t]*<(hr)\b([^<>])*?/?>(?=\n{2,}|\Z))"

    match_a = r"""
    (                                               # save in $1
    ^                                       # start of line  (with /m)
    <(%s)        # start tag = $2
    \b                                      # word break
    (.*\n)*?                        # any number of lines, minimally matching
    </\2>                           # the matching end tag
    [ \t]*                          # trailing spaces/tabs
    (?=\n+|$)      # followed by a newline or end of document
                                )
    """ % block_tags_a

    match_b = r"""
    (                                               # save in $1
    ^                                       # start of line  (with /m)
    <(%s)        # start tag = $2
    \b                                      # word break
    (.*\n)*?                        # any number of lines, minimally matching
    .*</\2>                         # the matching end tag
    [ \t]*                          # trailing spaces/tabs
    (?=\n+|\Z)      # followed by a newline or end of document
    )    """ % block_tags_b

    match_c = r"""
    (?:
    (?<=\n\n)               # Starting after a blank line
    |                               # or
    \A\n?                   # the beginning of the doc
    )
    (                                               # save in $1
    [ \t]*
    <(hr)                           # start tag = $2
    \b                                      # word break
    ([^<>])*?                       # 
    /?>                                     # the matching end tag
    (?=\n{2,}|\Z)           # followed by a blank line or end of document
    )
    """

    pat_a = re.compile(match_a, re.MULTILINE + re.VERBOSE)
    pat_b = re.compile(match_b, re.MULTILINE + re.VERBOSE)
    pat_c = re.compile(match_c, re.VERBOSE)

    text = pat_a.sub(handler, text)
    text = pat_b.sub(handler, text)
    text = pat_c.sub(handler, text)
    return text;

def _EncodeAmpsAndAngles(text):
    text = re.sub(r"&(?!#?[xX]?(?:[0-9a-fA-F]+|\w+);)","&amp;", text)
    text = re.sub(r"<(?![a-z/?\$!])","&lt;", text)
    return text

def _StripLinkDefinitions(text):
    def replacefunc(matchobj):
        (t1, t2, t3) = matchobj.groups()
        g_urls[t1.lower()] = _EncodeAmpsAndAngles(t2)
        if (t3 is not None):
            g_titles[t1.lower()] = re.sub(r'"',r'&quot',t3)
        return ""

    match_a = r"""
^[ \t]*\[(.+)\]:        # id = $1
[ \t]*\n?[ \t]*
<?(\S+?)>?                      # url = $2
[ \t]*\n?[ \t]*
(?:[\"\(]  # Harmless quoting to prevent emacs from fucking up
(.+?)                   # title = $3
[\"\)]     # more quoting
[ \t]*
)?      # title is optional
(?:\n+|\Z)
"""
    
    pat_a = re.compile(match_a, re.MULTILINE + re.VERBOSE)
    text = pat_a.sub(replacefunc, text)
    return text


def _TokenizeHTML(text):
            
    pos = 0
    tokens = []
    depth = 1
    nested_tags = string.join([r'(?:<[a-z/!$](?:[^<>]'] * depth,"|") + (')*>)') * depth
    match = r"""(?: <! ( -- .*? -- \s* )+ > ) |  # comment
                   (?: <\? .*? \?> ) |              # processing instruction
                   %s                   # nested tags
                   """ % nested_tags
    pat = re.compile(match, re.I + re.VERBOSE + re.S)
    matchobj = pat.search(text, pos)
    while matchobj:
        whole_tag = matchobj.string[matchobj.start():matchobj.end()]
        sec_start = matchobj.end()
        tag_start = sec_start - len(whole_tag)
        if pos < tag_start:
            tokens.append(["text", matchobj.string[pos:tag_start]])

        tokens.append(["tag", whole_tag])
        pos = sec_start
        matchobj = pat.search(text, pos)

    if pos < len(text):
        tokens.append(["text", text[pos:]])
    return tokens;

def _EncodeBackslashEscapes(text):

    for char in escapechars:
        text = text.replace("\\" + char, g_escape_table[char])
    return text


def _EscapeSpecialChars(text):
    tokens = _TokenizeHTML(text)
    text = ""

    for cur_token in tokens:
        if cur_token[0] == "tag":
            cur_token[1] = re.sub("\*", g_escape_table["*"], cur_token[1])
            cur_token[1] = re.sub("_", g_escape_table["_"], cur_token[1])
            text += cur_token[1]
        else:
            text += _EncodeBackslashEscapes(cur_token[1])
    return text

def _EncodeCode(text):
    text = text.replace("&","&amp;")
    text = text.replace("<","&lt;")
    text = text.replace(">","&gt;")
    for c in "*_{}[]\\":
        text = text.replace(c,g_escape_table[c])
    return text

def _DoCodeSpans(text):
    def handler(m):
        c = m.group(2)
        c = c.strip()
        c = _EncodeCode(c)
        return "<code>%s</code>" % c

    match = r"""
    (`+)            # $1 = Opening run of `
    (.+?)           # $2 = The code block
    (?<!`)
    \1                      # Matching closer
    (?!`)
    """
    pat = re.compile(match, re.S + re.I + re.VERBOSE)

    text = pat.sub(handler, text)

    return text

def _DoAnchors(text):
    # We here don't do the same as the perl version, as python's regex
    # engine gives us no way to match brackets.

    def handler1(m):
        whole_match = m.group(1)
        link_text = m.group(2)
        link_id = m.group(3).lower()
        title = None
        res = ""

        if not link_id:
            link_id = link_text.lower()

        if g_urls.has_key(link_id):
            url = g_urls[link_id]
            url = url.replace("*",g_escape_table["*"])
            url = url.replace("_",g_escape_table["_"])
            res = '''<a href="%s"''' % (url)

            if len(m.groups()) >= 7 and m.group(6):
                title = m.group(6)
            elif g_titles.has_key(link_id):
                title = g_titles[link_id]
            if title:
                title = title.replace("*",g_escape_table["*"])
                title = title.replace("_",g_escape_table["_"])
                res += ' title="%s"' % title
            res += ">%s</a>" % link_text
        else:
            res = whole_match
        return res

    def handler2(m):
        whole_match = m.group(1)
        link_text = m.group(2)
        url = m.group(3)
        title = None
        res = ""

        url = url.replace("*",g_escape_table["*"])
        url = url.replace("_",g_escape_table["_"])

        res = '''<a href="%s"''' % url
        if len(m.groups()) >= 6 and m.group(6):
            title = m.group(6)
        if title:
            title = title.replace("*",g_escape_table["*"])
            title = title.replace("_",g_escape_table["_"])
            res += ' title="%s"' % title
        res += ">%s</a>" % link_text
        return res


    match_1 = r""" (                                       # wrap whole match in $1
                  \[
                    (.*?)        # link text = $2
                  \]

                  [ ]?                          # one optional space
                  (?:\n[ ]*)?           # one optional newline followed by spaces

                  \[
                    (.*?)               # id = $3
                  \]
                )
                """
    pat_1 = re.compile(match_1, re.S + re.VERBOSE)
    text = pat_1.sub(handler1, text)

    match_2 = r""" (                                       # wrap whole match in $1
                  \[
                    (.*?)        # link text = $2
                  \]
                  \(                    # literal paren
                        [ \t]*
                        <?(.+?)>?       # href = $3
                        [ \t]*
                        (                       # $4
                          ([\'\"])        # quote char = $5
                          (.*?)         # Title = $6
                          \5            # matching quote
                        )?                      # title is optional
                  \)
                )
                """
    pat_2 = re.compile(match_2, re.S + re.VERBOSE)
    text = pat_2.sub(handler2, text)

    return text

def _DoImages(text):
    def handler1(m):
        whole_match = m.group(1)
        alt_text = m.group(2)
        link_id = m.group(3).lower()
        res = ""

        if not link_id:
            link_id = alt_text.lower()

        alt_text = alt_text.replace('"', "&quot")
        if g_urls.has_key(link_id):
            url = g_urls[link_id]
            url = url.replace("*",g_escape_table["*"])
            url = url.replace("_",g_escape_table["_"])
            res = '''<img src="%s" alt="%s"''' % (url, alt_text)
            if (g_titles.has_key(link_id)):
                title = g_titles[link_id]
                title = title.replace("*",g_escape_table["*"])
                title = title.replace("_",g_escape_table["_"])
                res += ' title="%s"' % title
            res += g_empty_element_suffix
        else:
            res = whole_match
        return res

    def handler2(m):
        whole_match = m.group(1)
        alt_text = m.group(2)
        url = m.group(3)
        title = m.group(6)
        if not title:
            title = ""
        alt_text = alt_text.replace('"', "&quot;")
        title = title.replace('"', "&quot;")
        url = url.replace("*", g_escape_table["*"])
        url = url.replace("_", g_escape_table["_"])
        res = '<img src="%s" alt="%s"' % (url, alt_text)
        title = title.replace("*", g_escape_table["*"])
        title = title.replace("_", g_escape_table["_"])
        res += ' title="%s"' % title
        res += g_empty_element_suffix
        return res

    match_1 = r""" (                               # wrap whole match in $1
                  !\[
                    (.*?)               # alt text = $2
                  \]

                  [ ]?                          # one optional space
                  (?:\n[ ]*)?           # one optional newline followed by spaces

                  \[
                    (.*?)               # id = $3
                  \]

                )
"""
    pat_1 = re.compile(match_1, re.VERBOSE + re.S)
    text = pat_1.sub(handler1, text)

    match_2 = r""" (                               # wrap whole match in $1
                  !\[
                    (.*?)               # alt text = $2
                  \]
                  \(                    # literal paren
                        [ \t]*
                        <?(\S+?)>?      # src url = $3
                        [ \t]*
                        (                       # $4
                        ([\'\"])        # quote char = $5
                          (?P<title>.*?)         # title = $6
                          \5            # matching quote
                          [ \t]*
                        )?                      # title is optional
                  \)
                )
"""
    pat_2 = re.compile(match_2, re.VERBOSE + re.S)
    text = pat_2.sub(handler2, text)
    
    return text

def _DoItalicsAndBold(text):

    pat1 = re.compile(r"(\*\*|__) (?=\S) (.+?[*_]*) (?<=\S) \1", re.VERBOSE + re.S)
    pat2 = re.compile(r"(\*|_) (?=\S) (.+?) (?<=\S) \1", re.VERBOSE + re.S)
    text = pat1.sub(r"<strong>\2</strong>", text)
    text = pat2.sub(r"<em>\2</em>", text)
    return text

def _RunSpanGamut(text):

    text = _DoCodeSpans(text)

    text = _EncodeAmpsAndAngles(text);

    text = _DoImages(text)
    text = _DoAnchors(text)

    text = _DoItalicsAndBold(text)

    text = re.sub(" {2,}\n", " <br%s\n" % g_empty_element_suffix, text)

    return text

def _DoHeaders(text):

    def handler(m):
        length = len(m.group(1))
        header = _RunSpanGamut(m.group(2))
        return "<h%(len)s>%(header)s</h%(len)s>\n\n" % {
        "len": length,
        "header": header }


    text = re.sub(r"(.+)[ \t]*\n=+[ \t]*\n+", "<h1>" + _RunSpanGamut(r"\1") + "</h1>\n\n", text)
    text = re.sub(r"(.+)[ \t]*\n-+[ \t]*\n+", "<h2>" + _RunSpanGamut(r"\1") + "</h2>\n\n", text)

    match = r"^(\#{1,6})[ \t]*(.+?)[ \t]*\#*\n+"
    pat = re.compile(match, re.VERBOSE + re.M)

    text = pat.sub(handler, text)

    return text

def _Outdent(text):
    match = r"""^(\t|[ ]{1,%d})""" % g_tab_width
    pat = re.compile(match, re.M)
    text = pat.sub("", text)
    return text;

def _ProcessListItems(text):
    def handler(m):
        item = m.group(4)
        leading_line = m.group(1)
        leading_space = m.group(2)

        if leading_line or re.search("\n{2,}", item):
            item = _RunBlockGamut(_Outdent(item))
        else:
            item = _DoLists(_Outdent(item))
            if item[-1] == "\n":
                item = item[:-1]
            item = _RunSpanGamut(item)
        return "<li>%s</li>\n" % item
    text = re.sub(r"\n{2,}\Z","\n", text)
    match = r"""
    (\n)?                            # leading line =  $1
    (^[ \t]*)                        # leading whitespace = $2
    ([*+-]|\d+[.]) [ \t]+            # list marker = $3
    ((?:.+?)                         # list item text = $4
    (\n{1,2}))
    (?= \n* (\Z | \2 ([*+-]|\d+[.]) [ \t]+))
    """
    pat = re.compile(match, re.VERBOSE + re.M + re.S)

    text = pat.sub(handler, text)
    return text

def _DoLists(text):
    def handler(m):
        list_type = "ol"
        if m.group(3) in [ "*", "-", "+" ]:
            list_type = "ul"
        list = m.group(1)

        list = re.sub(r"\n{2,}", "\n\n\n", list)
        res = _ProcessListItems(list)
        res = "<%s>\n%s</%s>\n" % (list_type, res, list_type)
        return res

    less_than_tab = g_tab_width - 1

    match = r"""(
    (
    ^[ ]{0,%d}
    ([*+-]|\d+[.])
    [ \t]+
    )
    (?:.+?)
    (
      \Z
    |
      (\n{2,}
      (?=\S)
      (?![ \t]* (\*|\d+[.]) [ \t]+)
    )
    ))
    """ % less_than_tab
    pat = re.compile(match, re.M + re.VERBOSE + re.S)

    text = pat.sub(handler, text)

    return text

def _DoCodeBlocks(text):
    def handler(m):
        codeblock = m.group(1)
        codeblock = _EncodeCode(_Outdent(codeblock))
        codeblock = codeblock.lstrip("\n")
        codeblock = codeblock.rstrip()
        res = "\n\n<pre><code>%s\n</code></pre>\n\n" % codeblock
        return res

    match = r"""
    (?:\n\n|\A)
    (                   # $1 = the code block -- one or more lines, starting with a space/tab
    (?:
    (?:[ ]{%d} | \t)  # Lines must start with a tab or a tab-width of spaces
    .*\n+
    )+
    )
    ((?=^[ ]{0,%d}\S)|\Z) # Lookahead for non-space at line-start, or end of doc
    """ % (g_tab_width, g_tab_width)
    pat = re.compile(match, re.M + re.VERBOSE)
    text = pat.sub(handler, text)
    return text

def _DoBlockQuotes(text):
    def handler(m):
        bq = m.group(1)
        bq = sub(r"^[ \t]*>[ \t]?", "", bq, flags = re.M)
        bq = sub(r"^[ \t]+$", "", bq, flags = re.M)
        bq = _RunBlockGamut(bq)
        bq = sub(r"^", "  ", bq, flags= re.M)
        return "<blockquote>\n%s\n</blockquote>\n\n" % bq
    
    match = r"""
                  (                                                             
# Wrap whole match in $1
                        (
                          ^[ \t]*>[ \t]?                        # '>' at the start of a line
                            .+\n                                        # rest of the first line
                          (.+\n)*                                       # subsequent consecutive lines
                          \n*                                           # blanks
                        )+
                  )
    """
    pat = re.compile(match, re.M + re.VERBOSE)
    text = pat.sub(handler, text)
    return text

def _EncodeEmailAddress(text):

    random.seed()

    encode = [
        lambda x: "&#%s;" % ord(x),
        lambda x: "&#x%X;" % ord(x),
        lambda x: x
        ]

    text = "mailto:%s" % text
    addr = ""
    for c in text:
        if c == "@":
            addr += random.choice(encode)(c)
        elif c != ":":
            r = random.random()
            if r > 0.9:
                addr += encode[2](c)
            elif r < 0.45:
                addr += encode[1](c)
            else:
                addr += encode[0](c)
        else:
            addr += c
    text = '<a href="%s">%s</a>' % (addr, addr)
    text = sub(r">.+?:",r">", text)

    return text

def _UnescapeSpecialChars(text):

    for key in g_escape_table.keys():
        text = text.replace(g_escape_table[key], key)

    return text
    
def _DoAutoLinks(text):

    def handler(m):
        l = m.group(1)
        return _EncodeEmailAddress(_UnescapeSpecialChars(l))
    
    text = sub(r"<((https?|ftp):[^\'\">\s]+)>", r'<a href="\1">\1</a>',
               text, flags = re.I)
    text = sub(r"""<
                (
                        [-.\w]+
                        \@
                        [-a-z0-9]+(\.[-a-z0-9]+)*\.[a-z]+
                )
                >""", handler, text, flags = re.VERBOSE + re.I)

    return text

def _FormParagraphs(text):

    text = text.strip("\n")

    grafs = re.split("\n{2,}", text)
    count = len(grafs)
    for g in range(len(grafs)):
        t = grafs[g].strip()
        if not g_html_blocks.has_key(t):
            t = _RunSpanGamut(t)
            t = sub(r"^([ \t]*)", r"<p>", t)
            t += "</p>"
            grafs[g] = t

    for g in range(len(grafs)):
        t = grafs[g].strip()
        if g_html_blocks.has_key(t):
            grafs[g] = g_html_blocks[t]

    return "\n\n".join(grafs)

def _RunBlockGamut(text):
    
    text = _DoHeaders(text)

    pat1 = re.compile(r"^[ ]{0,2}([ ]?[-*_][ ]?){3,}[ \t]*$", re.M)

    text = pat1.sub("\n<hr%s\n" % g_empty_element_suffix, text);

    text = _DoLists(text)

    text = _DoCodeBlocks(text)

    text = _DoBlockQuotes(text)

    text = _DoAutoLinks(text)

    text = _HashHTMLBlocks(text)
    text = _FormParagraphs(text)

    return text

def Markdown(text):

    g_urls = {}
    g_titles = {}
    g_html_blocks = {}

    text = re.sub("\r\n", "\n", text)
    text = re.sub("\r", "\n", text)

    text += "\n\n"

    text = _Detab(text)

    text = stripspace.sub("", text)

    text = _HashHTMLBlocks(text)

    text = _StripLinkDefinitions(text)

    text = _EscapeSpecialChars(text)

    text = _RunBlockGamut(text)

    text = _UnescapeSpecialChars(text)
    
    return "%s\n" % text

if __name__ == '__main__':
    print Markdown(sys.stdin.read())
