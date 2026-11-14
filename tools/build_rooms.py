"""Builds both chat rooms from one layout.

chat-layout.html is the shared chat app. Each room supplies its own cast
(portraits, answers, questions) taken from its source file, plus a few words.
Run:  python3 tools/build_rooms.py
"""
import re, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
LAYOUT = (ROOT / 'tools' / 'chat-layout.html').read_text()
SOURCES = ROOT / 'tools' / 'sources'


def data_block(src):
    lines = src.split('\n')
    start = next(i for i, l in enumerate(lines) if 'const SVGNS = ' in l)
    end = next(i for i, l in enumerate(lines) if '// ---------- helpers' in l)
    return '\n'.join(lines[start:end])


ROOMS = {
    'designers': dict(
        out='designers/index.html',
        source='designers.html',
        title='What Would Dead Designers Do?',
        thick='Dead Designers',
        desc='A group chat with the design greats. Paul Rand, Massimo Vignelli, Coco Chanel and friends answer from the afterlife. A parody by Nino Studio.',
        og_desc='A group chat with the design greats. A parody by Nino Studio.',
        og='https://stilllife.nino.studio/designers/og.png?v=2',
        intro='A group chat with the design greats. Ask anything about design, AI or life. Parody: every word is made up.',
        kind='designer', kinds='designers',
        sample=('Is the design profession dead because of AI?', 'designdead'),
        alias="{ pr: /\\brand\\b|paul/i, sb: /saul|\\bbass\\b/i, mv: /vignelli|massimo/i, mg: /glaser|milton/i, ce: /eames|charles|\\bray\\b/i, rl: /loewy|raymond/i, sj: /jobs|steve/i, cc: /chanel|coco/i, fw: /frank|lloyd wright|\\bwright\\b/i, mr: /\\bmies\\b|van der rohe/i, es: /schiap|\\belsa\\b/i }",
        nino_chat=['Hi, I’m Nino. The only designer in this chat with a pulse.', 'Nearly 30 years designing products, at Microsoft, Amazon and Oracle among others. Also a painter in Seattle.'],
        links=[['See my design work', 'https://nino.studio/pages/design'], ['LinkedIn', 'https://www.linkedin.com/in/ninoy'], ['The dead artists', '/']],
        about_h='Made by a living designer.',
        about_body=['I’m Nino, a designer and painter in Seattle. Nearly thirty years of designing products, at Microsoft, Amazon and Oracle among others.', 'Curious what a living designer is making?'],
        fine=['This is a comedy. These designers never said any of this. The jokes are built on real facts from their lives, but every word is made up.', 'Please don’t make the logo bigger because a dead designer told you to. Nothing here is professional, financial, legal or medical advice.'],
        theme=None,
    ),
    'artists': dict(
        out='index.html',
        source='artists.html',
        title='What Would Dead Artists Do?',
        thick='Dead Artists',
        desc='A group chat with the art greats. Van Gogh, Frida, Picasso, Monet and friends answer from the afterlife. A parody by Nino Studio.',
        og_desc='A group chat with the art greats. A parody by Nino Studio.',
        og='https://stilllife.nino.studio/og.png?v=2',
        intro='A group chat with the art greats. Ask anything about art, making a living or life. Parody: every word is made up.',
        kind='artist', kinds='artists',
        sample=('Should I quit my job to paint full time?', 'quit'),
        alias="{ vg: /van gogh|vincent/i, pp: /picasso|pablo/i, cm: /monet/i, fk: /frida|kahlo/i, aw: /warhol|\\bandy\\b/i, sd: /dal[ií]|salvador/i, jp: /pollock|jackson/i, br: /bob ross|\\bross\\b/i }",
        nino_chat=['Hi, I’m Nino. The only one in this chat with a pulse.', 'I’m a painter in Seattle. I made this because the greats figured out creative life the hard way. You don’t have to.'],
        links=[['Explore the art', 'https://nino.studio'], ['Spice Art Club', 'https://nino.studio/pages/spice-art-club'], ['Instagram', 'https://www.instagram.com/ninoyuniardi'], ['The dead designers', '/designers']],
        about_h='Made by a living artist.',
        about_body=['I’m Nino, a painter in Seattle. I made this because the greats figured out creative life the hard way. You don’t have to.', 'Want feedback from a living artist? Come paint with us.'],
        fine=['This is a comedy. These artists never said any of this. The jokes are built on real facts from their lives, but every word is made up.', 'Please don’t quit your job, cut off an ear or tape fruit to a wall because a dead painter told you to. Nothing here is professional, financial, legal or medical advice.'],
        # a warm paper ground, the artists room's own colours
        theme=dict(
            light='--bg: #f3eee6; --surface: #fdfbf7; --ink: #1a1714; --muted: #655d53; --line: #e0d7ca;',
            dark='--bg: #171412; --surface: #221d19; --ink: #f2eeea; --muted: #b1a79c; --line: #352d27;',
            colors='--c-vg: #d4a849; --c-pp: #6f8fa8; --c-cm: #8fa77f; --c-fk: #d2826b;\n  --c-aw: #cf93a6; --c-sd: #a5543f; --c-jp: #a8a29a; --c-br: #4f735c;',
            meta='#f3eee6',
        ),
    ),
}


def js(s):
    return "'" + s.replace('\\', '\\\\').replace("'", "\\'") + "'"


def build(room):
    r = ROOMS[room]
    src = (SOURCES / r['source']).read_text()
    h = LAYOUT
    rep = {
        '{{TITLE}}': r['title'], '{{DESC}}': r['desc'], '{{OG_DESC}}': r['og_desc'], '{{OG}}': r['og'],
        '{{THICK}}': r['thick'], '{{KINDS}}': r['kinds'], '{{KIND}}': r['kind'],
        '{{INTRO}}': js(r['intro']), '{{ALIAS}}': r['alias'],
        '{{SAMPLE_Q}}': js(r['sample'][0]), '{{SAMPLE_T}}': js(r['sample'][1]),
        '{{NINO_CHAT}}': '[' + ', '.join(js(x) for x in r['nino_chat']) + ']',
        '{{LINKS}}': '[' + ', '.join('[' + js(a) + ', ' + js(b) + ']' for a, b in r['links']) + ']',
        '{{ABOUT_H}}': js(r['about_h']),
        '{{ABOUT_BODY}}': '[' + ', '.join(js(x) for x in r['about_body']) + ']',
        '{{FINE}}': '[' + ', '.join(js(x) for x in r['fine']) + ']',
    }
    for k, v in rep.items():
        assert k in h, k
        h = h.replace(k, v)
    h = h.replace('/*DATA*/', data_block(src))
    t = r['theme']
    if t:
        h = re.sub(r'  --bg: #f4f2ee;[^\n]*', '  ' + t['light'], h, count=1)
        h = re.sub(r'  --bg: #0b0b0b;[^;]*;[^;]*;[^;]*;[^;]*;[^;]*;', '  ' + t['dark'], h, count=1)
        h = re.sub(r'  --c-pr: [^\n]*\n  --c-sj: [^\n]*', '  ' + t['colors'], h, count=1)
        h = h.replace('content="#f4f2ee"', 'content="' + t['meta'] + '"')
    assert '{{' not in h
    (ROOT / r['out']).write_text(h)
    print('built', r['out'])


if __name__ == '__main__':
    for room in ROOMS:
        build(room)
