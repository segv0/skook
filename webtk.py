"""
webtk: tarayicida calisan minimal bir tkinter koprusu.

letter.py'nin kullandigi tkinter parcalarini (Tk, Canvas, font.Font,
after, bind ...) taklit eder ve cizim komutlarini JavaScript tarafindaki
HTML <canvas>'a toplu halde gonderir. letter.py'de hicbir degisiklik
gerekmez.
"""
import sys
import types

import js
from pyodide.ffi import create_proxy

_ops = []
_next_id = [0]
_binds = {}
_proxies = {}


def _flush():
    if _ops:
        js.webtkApply("\x1e".join(_ops))
        _ops.clear()


def _clean(s):
    return str(s).replace("\x1e", " ").replace("\x1f", " ")


class Tk:
    def title(self, *_):
        pass

    def resizable(self, *_):
        pass

    def geometry(self, *_):
        pass

    def destroy(self):
        pass

    def bind(self, seq, fn):
        _binds[seq] = fn

    def winfo_screenheight(self):
        return int(js.WEBTK.screenH)

    def winfo_screenwidth(self):
        return int(js.WEBTK.screenW)

    def after(self, ms, fn):
        p = _proxies.get(fn)
        if p is None:
            def cb(*_a, _fn=fn):
                try:
                    _fn()
                finally:
                    _flush()
            p = create_proxy(cb)
            _proxies[fn] = p
        js.setTimeout(p, int(ms))

    def mainloop(self):
        # Tarayicida bloklayan dongu yok; zamanlayicilar JS tarafinda doner.
        _flush()


class Canvas:
    def __init__(self, master=None, width=0, height=0, bg="#000000", **_kw):
        _ops.append("b\x1f%d\x1f%d\x1f%s" % (int(width), int(height), bg))

    def pack(self, *_a, **_k):
        pass

    def create_text(self, x, y, text="", fill="#ffffff", **_kw):
        _next_id[0] += 1
        i = _next_id[0]
        _ops.append("c\x1f%d\x1f%r\x1f%r\x1f%s\x1f%s" % (i, float(x), float(y), _clean(text), fill))
        return i

    def itemconfig(self, item, text=" ", fill=None, **_kw):
        _ops.append("u\x1f%d\x1f%s\x1f%s" % (item, _clean(text), fill or ""))


class Font:
    def __init__(self, root=None, family=None, size=10, weight="normal", **_kw):
        pass

    def metrics(self, what):
        if what == "linespace":
            return int(js.WEBTK.CH)
        return 0

    def measure(self, s):
        return int(js.WEBTK.CW) * len(s)


def families(*_a):
    return ("Courier",)


def fire_key(seq):
    """JS tarafindan klavye / dokunma ile cagrilir (ornegin 'r')."""
    fn = _binds.get(seq)
    if fn is not None:
        try:
            fn(None)
        finally:
            _flush()


_tk = types.ModuleType("tkinter")
_tk.Tk = Tk
_tk.Canvas = Canvas
_font = types.ModuleType("tkinter.font")
_font.Font = Font
_font.families = families
_tk.font = _font
sys.modules["tkinter"] = _tk
sys.modules["tkinter.font"] = _font
