import os, subprocess, shutil, re, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import imageio_ffmpeg

FF = imageio_ffmpeg.get_ffmpeg_exe()
W, H, FPS = 1280, 720, 24
BG = "build4"
shutil.rmtree(BG, ignore_errors=True)
os.makedirs(BG)

FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
FONT_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"

def font(p, s): return ImageFont.truetype(p, s)

_VIG = None
def vignette(img, strength=0.45):
    global _VIG
    if _VIG is None:
        m = Image.new("L", (W, H), 0); d = ImageDraw.Draw(m)
        d.ellipse([-W*0.25, -H*0.25, W*1.25, H*1.25], fill=255)
        m = m.filter(ImageFilter.GaussianBlur(130))
        _VIG = m.point(lambda p: int(255 - (255 - p) * strength))
    return Image.composite(img, Image.new("RGB", (W, H), (0, 0, 0)), _VIG)

def fit(img, w=W, h=H):
    img = img.convert("RGB")
    s = max(w / img.width, h / img.height)
    img = img.resize((int(img.width * s), int(img.height * s)), Image.LANCZOS)
    x = (img.width - w) // 2; y = (img.height - h) // 2
    return img.crop((x, y, x + w, y + h))

def img(n): return fit(Image.open(f"images/{n}"))

_BRAND = None
def brand_overlay():
    global _BRAND
    if _BRAND is None:
        sc = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(sc)
        d.text((40, 40), "ECHOES OF EMPIRES", font=font(FONT_B, 17), fill=(255, 226, 170, 235))
        _BRAND = sc
    return _BRAND

def wrap(d, text, f, maxw):
    words = text.split(); lines = []; cur = ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=f) > maxw:
            lines.append(cur); cur = w_
        else:
            cur = t
    if cur: lines.append(cur)
    return lines

def caption_overlay(text, sub=None):
    sc = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(sc)
    f = font(FONT_B, 32)
    lines = wrap(d, text, f, W - 220)
    lh = 44; bh = lh * len(lines) + (28 if sub else 0); y0 = H - bh - 58
    d.rectangle([0, y0 - 12, W, H], fill=(0, 0, 0, 145))
    y = y0
    for ln in lines:
        tw = d.textlength(ln, font=f); x = (W - tw) // 2
        d.text((x + 2, y + 2), ln, font=f, fill=(0, 0, 0, 255)); d.text((x, y), ln, font=f, fill=(255, 214, 120, 255)); y += lh
    if sub:
        fs = font(FONT_R, 24); tw = d.textlength(sub, font=fs); x = (W - tw) // 2
        d.text((x + 1, y + 1), sub, font=fs, fill=(0, 0, 0, 255)); d.text((x, y), sub, font=fs, fill=(228, 228, 228, 255))
    return sc

def lower_overlay(text):
    sc = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(sc)
    f = font(FONT_B, 26); tw = d.textlength(text, font=f)
    bw = tw + 40; bh = 44; x0 = 60; y0 = H - 152
    d.rectangle([x0, y0, x0 + bw, y0 + bh], fill=(0, 0, 0, 175))
    d.rectangle([x0, y0, x0 + 5, y0 + bh], fill=(255, 214, 120, 255))
    d.text((x0 + 22, y0 + 8), text, font=f, fill=(255, 236, 200, 255))
    return sc

def badge_overlay(text):
    sc = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(sc)
    f = font(FONT_B, 22); tw = d.textlength(text, font=f)
    bw = tw + 32; bh = 38; x0 = W - bw - 40; y0 = 34
    d.rectangle([x0, y0, x0 + bw, y0 + bh], fill=(0, 0, 0, 170))
    d.rectangle([x0, y0, x0 + bw, y0 + bh], outline=(212, 162, 74, 255), width=2)
    d.text((x0 + 16, y0 + 6), text, font=f, fill=(255, 214, 120, 255))
    return sc

def chapter_card(title, sub=None):
    im = Image.new("RGB", (W, H), (10, 8, 6)); d = ImageDraw.Draw(im)
    for r in range(700, 0, -4):
        c = int(16 + (r / 700) * 26)
        d.ellipse([W/2 - r, H/2 - r, W/2 + r, H/2 + r], fill=(c, c - 2, c - 6))
    f = font(FONT_B, 58)
    lines = title.split("\n"); y = H/2 - 42 * len(lines)
    for ln in lines:
        tw = d.textlength(ln, font=f)
        d.text(((W - tw)/2 + 3, y + 3), ln, font=f, fill=(0, 0, 0))
        d.text(((W - tw)/2, y), ln, font=f, fill=(255, 214, 120)); y += 82
    if sub:
        fs = font(FONT_R, 28); tw = d.textlength(sub, font=fs)
        d.text(((W - tw)/2, y + 6), sub, font=fs, fill=(206, 196, 176))
    return im

def date_card(date, place):
    im = Image.new("RGB", (W, H), (10, 8, 6)); d = ImageDraw.Draw(im)
    f = font(FONT_B, 86); tw = d.textlength(date, font=f)
    d.text(((W - tw)/2 + 4, H/2 - 70 + 4), date, font=f, fill=(0, 0, 0))
    d.text(((W - tw)/2, H/2 - 70), date, font=f, fill=(255, 214, 120))
    fs = font(FONT_R, 32); tw = d.textlength(place, font=fs)
    d.text(((W - tw)/2, H/2 + 40), place, font=fs, fill=(210, 200, 180))
    return im

def end_card():
    im = Image.new("RGB", (W, H), (10, 8, 6)); d = ImageDraw.Draw(im)
    for r in range(700, 0, -4):
        c = int(16 + (r / 700) * 26)
        d.ellipse([W/2 - r, H/2 - r, W/2 + r, H/2 + r], fill=(c, c - 2, c - 6))
    f = font(FONT_B, 64); t = "SUBSCRIBE"
    tw = d.textlength(t, font=f)
    d.text(((W - tw)/2 + 3, H/2 - 90 + 3), t, font=f, fill=(0, 0, 0))
    d.text(((W - tw)/2, H/2 - 90), t, font=f, fill=(255, 214, 120))
    fs = font(FONT_R, 30); t2 = "Next story: THE MONGOL EMPIRE?"
    tw = d.textlength(t2, font=fs); d.text(((W - tw)/2, H/2 + 10), t2, font=fs, fill=(226, 216, 196))
    f3 = font(FONT_R, 22); t3 = "Echoes of Empires  -  History that hits like a movie"
    tw = d.textlength(t3, font=f3); d.text(((W - tw)/2, H/2 + 70), t3, font=f3, fill=(150, 140, 124))
    return im

def write_plate(tag, base, dur, caption=None, sub=None, lower=None, badge_txt=None, zoom=1.14, fade=0.7):
    d = f"{BG}/{tag}"; os.makedirs(d, exist_ok=True)
    cap = caption_overlay(caption, sub) if caption else None
    low = lower_overlay(lower) if lower else None
    bad = badge_overlay(badge_txt) if badge_txt else None
    brand = brand_overlay()
    black = Image.new("RGB", (W, H), (0, 0, 0))
    n = int(dur * FPS); nf = int(fade * FPS)
    for i in range(n):
        t = i / max(1, n - 1); z = 1.0 + (zoom - 1.0) * t
        cw, ch = int(W / z), int(H / z)
        dx = (z - 1) * W * 0.07; dy = (z - 1) * H * 0.045
        x = int((base.width - cw)/2 - dx); y = int((base.height - ch)/2 - dy)
        x = max(0, min(base.width - cw, x)); y = max(0, min(base.height - ch, y))
        fr = base.crop((x, y, x + cw, y + ch)).resize((W, H), Image.LANCZOS)
        fr = Image.composite(fr, black, _VIG)
        rgba = fr.convert("RGBA")
        if cap is not None: rgba = Image.alpha_composite(rgba, cap)
        if low is not None: rgba = Image.alpha_composite(rgba, low)
        if bad is not None: rgba = Image.alpha_composite(rgba, bad)
        rgba = Image.alpha_composite(rgba, brand)
        fr = rgba.convert("RGB")
        if i < nf: fr = ImageEnhance.Brightness(fr).enhance(i / max(1, nf))
        if i >= n - nf: fr = ImageEnhance.Brightness(fr).enhance((n - i) / max(1, nf))
        fr.save(f"{d}/f_{i:05d}.jpg", quality=88)
    return d

def write_hold(tag, card, dur):
    d = f"{BG}/{tag}"; os.makedirs(d, exist_ok=True)
    for i in range(int(dur * FPS)):
        card.save(f"{d}/f_{i:05d}.jpg", quality=90)
    return d

def write_black(tag, dur):
    d = f"{BG}/{tag}"; os.makedirs(d, exist_ok=True)
    for i in range(int(dur * FPS)):
        Image.new("RGB", (W, H), (0, 0, 0)).save(f"{d}/f_{i:05d}.jpg", quality=88)
    return d

CH = [108.6, 102.5, 95.8, 88.9, 99.8, 90.7, 89.6, 101.0, 88.3, 90.8, 93.68, 48.27]
C = 2.4

SEG = [
    ("black", 1.0, None, None, None, None, None),
    ("card", 2.2, date_card("29 MAY 1453", "CONSTANTINOPLE"), None, None, None, None),
    ("plate", CH[0]-3.2, "background-walls.png",
     "On the morning of May 29th, 1453, the most famous city in the world died.",
     "For a thousand years, its walls had never been breached.", None, "DAY 53"),

    ("card", C, chapter_card("THE WORLD BEFORE", "Act 1"), None, None, None, None),
    ("plate", CH[1]-C, "background-walls.png",
     "The walls were the whole point. As long as they stood, the city could wait for help.",
     "Constantine XI - last Roman emperor, 49", "CONSTANTINE XI  -  LAST ROMAN EMPEROR, 49", None),
    ("plate", CH[2], "character-mehmed.png",
     "'He'll be easy,' they said. Mehmed smiled, signed friendly treaties...",
     "Mehmed II - the boy sultan", "MEHMED II  -  THE BOY SULTAN, 19", None),

    ("card", C, chapter_card("1452 - THE YEAR OF THE KNIFE", "Act 2"), None, None, None, None),
    ("plate", CH[3]-C, "prop-great-bombard.png",
     "The Great Bombard - a stone ball of 600 kilos, over a mile.",
     "60 oxen - 400 men - 7 shots a day", "ORBAN  -  THE CANNON MAKER", None),
    ("plate", CH[4], "bg-golden-horn.png",
     "Across the mouth of the Golden Horn, the Byzantines stretched a great chain.",
     "The second trump card", "THE GREAT CHAIN  -  GOLDEN HORN", None),

    ("card", C, chapter_card("DAY 1 - 6 APRIL 1453", "Act 3 - The Siege"), None, None, None, None),
    ("plate", CH[5]-C, "bg-siege-camp.png",
     "The sultan did not. He stripped his admiral, Baltoghlu, of everything.",
     "20 April - the convoy that embarrassed a sultan", None, "DAY 15"),
    ("plate", CH[6], "bg-underground.png",
     "Serbian sappers started tunneling under the walls.",
     "The war underground", "THE WAR UNDERGROUND", "DAY 17"),
    ("plate", CH[7], "bg-hagia-sophia.png",
     "On May 21st, Mehmed made one last offer.",
     "21 May - the refusal", None, "DAY 46"),

    ("card", C, chapter_card("DAY 53 - 29 MAY 1453", "Act 4 - The Last Day"), None, None, None, None),
    ("plate", CH[8]-C, "bg-final-assault.png",
     "Wave two: the azaps - poorly trained, poorly equipped, and absolutely everywhere.",
     "Midnight - three waves", "THE FINAL ASSAULT", "DAY 53"),
    ("plate", CH[9], "character-constantine.png",
     "But something happened at that gate.",
     "The gate that may have decided everything", "CONSTANTINE XI  -  LAST ROMAN EMPEROR", "DAY 53"),

    ("card", C, chapter_card("THE ECHO", "Act 5"), None, None, None, None),
    ("plate", CH[10]-C, "bg-echo.png",
     "Mehmed rode in and, by most accounts, stopped the worst of it.",
     "Mehmed - 'Caesar of Rome'", "MEHMED II  -  'CAESAR OF ROME'", None),
    ("plate", CH[11], "bg-two-thrones.png",
     "Two young men. One city. Fifty-three days.",
     "One got the city. The other got the legend.", None, None),

    ("card", 6.0, end_card(), None, None, None, None),
    ("black", 1.5, None, None, None, None, None),
]

print("rendering scenes...", flush=True)
dirs = []
for idx, s in enumerate(SEG):
    kind, dur = s[0], s[1]
    if kind == "black":
        d = write_black(f"s{idx:02d}", dur)
    elif kind == "card":
        d = write_hold(f"s{idx:02d}", s[2], dur)
    else:
        _, _, fn, cap, sub, lower, badgetxt = s
        d = write_plate(f"s{idx:02d}", img(fn), dur, cap, sub, lower, badgetxt)
    dirs.append(d)
    print(f"  s{idx:02d} {kind} done", flush=True)

print("concat...", flush=True)
big = f"{BG}/all"; os.makedirs(big, exist_ok=True); k = 0
for d in dirs:
    for fn in sorted(os.listdir(d)):
        os.link(os.path.join(d, fn), os.path.join(big, f"{k:06d}.jpg")); k += 1
print("frames", k, flush=True)
subprocess.run([FF, "-y", "-framerate", str(FPS), "-i", f"{big}/%06d.jpg",
                "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "21", "-preset", "medium",
                "-threads", "2", f"{BG}/video.mp4"], check=True, capture_output=True)

alst = f"{BG}/audio.txt"
with open(alst, "w") as fh:
    for i in range(1, 13):
        fh.write(f"file '{os.path.abspath(f'audio/narration_{i:02d}.mp3')}'\n")
subprocess.run([FF, "-y", "-f", "concat", "-safe", "0", "-i", alst, "-c", "copy", f"{BG}/voice.mp3"],
               check=True, capture_output=True)

probe = subprocess.run([FF, "-i", f"{BG}/voice.mp3"], capture_output=True, text=True).stderr
m = re.search(r'Duration: (\d+):(\d+):(\d+\.\d+)', probe)
h, mi, se = m.groups(); DUR = int(h) * 3600 + int(mi) * 60 + float(se) + 7.5
print("total dur", DUR, flush=True)
sr = 44100; n = int(DUR * sr); t = np.arange(n) / sr
rng = np.random.default_rng(11)
def tone(f, a, ph=0): return a * np.sin(2 * np.pi * f * t + ph)
lfo = 0.62 + 0.38 * np.sin(2 * np.pi * 0.045 * t)
drone = (tone(73.42, 0.22) + tone(110.0, 0.14) + tone(146.83, 0.09) + tone(220.0, 0.05)) * lfo
drum = np.zeros(n)
for k in range(0, n, int(2.0 * sr)):
    L = min(int(0.5 * sr), n - k); tt = np.arange(L) / sr
    drum[k:k+L] += 0.5 * np.sin(2 * np.pi * 55 * tt) * np.exp(-tt * 9.0)
bed = drone + drum + 0.03 * np.sin(2 * np.pi * 523.25 * t) * lfo

def boom(at, amp=0.9, dur=1.6):
    global bed
    s = int(at * sr); L = min(int(dur * sr), n - s); tt = np.arange(L) / sr
    bed[s:s+L] += amp * (np.sin(2 * np.pi * 48 * tt) * 0.7 + rng.normal(0, 0.25, L) * np.exp(-tt * 12)) * np.exp(-tt * 3.2)

def drum_roll(at, dur=2.5):
    global bed
    s = int(at * sr); L = min(int(dur * sr), n - s); tt = np.arange(L) / sr
    hits = np.zeros(L); step = 0.14
    for j in range(int(dur / step)):
        st = int(j * step * sr); hl = min(int(0.25 * sr), L - st); htt = np.arange(hl) / sr
        hits[st:st+hl] += 0.4 * np.sin(2 * np.pi * 60 * htt) * np.exp(-htt * 14)
    bed[s:s+L] += hits * (0.4 + 0.6 * tt / dur)

offs = []; acc = 0.0
for s in SEG:
    offs.append(acc); acc += s[1]
boom(offs[0] + 0.4, 1.0)
for i, s in enumerate(SEG):
    if s[0] == "card" and i > 1:
        boom(offs[i] + 0.15, 0.5, 1.0)
drum_roll(offs[13] + 0.1, 2.5)

fi = int(3 * sr); fo = int(4 * sr)
bed[:fi] *= np.linspace(0, 1, fi); bed[-fo:] *= np.linspace(1, 0, fo)
bed = bed / np.max(np.abs(bed)) * 0.34
bed += rng.normal(0, 0.0035, n)
pcm = np.clip(bed * 32767, -32768, 32767).astype('<i2')
with wave.open(f"{BG}/score.wav", "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(pcm.tobytes())

subprocess.run([FF, "-y", "-i", f"{BG}/voice.mp3", "-i", f"{BG}/score.wav",
                "-filter_complex", "[1:a]volume=0.34,lowpass=f=900[a];[0:a][a]amix=inputs=2:duration=longest:dropout_transition=0[out]",
                "-map", "[out]", "-c:a", "aac", "-b:a", "192k", f"{BG}/audio.m4a"], check=True, capture_output=True)
subprocess.run([FF, "-y", "-i", f"{BG}/video.mp4", "-i", f"{BG}/audio.m4a",
                "-c:v", "copy", "-c:a", "copy", "video_master.mp4"], check=True, capture_output=True)
print("MASTER", os.path.getsize("video_master.mp4") // 1024, "KB", flush=True)
