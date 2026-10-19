"""Bande-son du film, synthétisée en code et calée sur out/cues.json (exporté par render.mjs).

120 BPM : 1 temps = 15 images. Les sections et les bruitages viennent des cues de index.html,
donc un son ne peut pas décrocher de son action. Sortie : out/audio.wav (44,1 kHz stéréo),
normalisée ensuite à -14 LUFS par build.sh.
"""
import json
import os

import numpy as np
from scipy.signal import butter, fftconvolve, sosfilt
from scipy.io import wavfile

HERE = os.path.dirname(os.path.abspath(__file__))
SR, FPS, BPM = 44100, 30, 120
data = json.load(open(os.path.join(HERE, 'out', 'cues.json')))
TOTAL = data['total']
CUES = data['cues']
N = int(TOTAL / FPS * SR)
BEAT = 15  # images
rng = np.random.default_rng(7)
PAD = 0.035  # niveau des nappes (3 dents de scie × 4 notes s'additionnent vite)


def at(f):
    return int(round(f / FPS * SR))


def hz(n):
    return 440.0 * 2 ** ((n - 69) / 12)


def sec(f):
    return f / FPS


def first(kind, default):
    for c in CUES:
        if c['k'] == kind:
            return c['f']
    return default


SEC = {k: first(k, d) for k, d in
       [('drop', 300), ('break', 510), ('ship', 630), ('drop2', 690), ('logo', 855), ('final', 960)]}
FLY = SEC['logo'] - 15            # les écrans s'envolent : la batterie s'arrête
BOOM = first('boom', SEC['logo'] + 16)
CTA = SEC['logo'] + 60            # début de la pill de fin

# ---------------------------------------------------------------- outils
def bp(x, lo, hi, order=2):
    return sosfilt(butter(order, [lo, hi], 'band', fs=SR, output='sos'), x)


def lp(x, fc, order=2):
    return sosfilt(butter(order, fc, 'low', fs=SR, output='sos'), x)


def hp(x, fc, order=2):
    return sosfilt(butter(order, fc, 'high', fs=SR, output='sos'), x)


def noise(n):
    return rng.standard_normal(n)


def tt(dur):
    return np.arange(int(dur * SR)) / SR


class Bus:
    def __init__(self):
        self.x = np.zeros((N + SR * 3, 2))

    def add(self, sig, f=None, i=None, gain=1.0, pan=0.0):
        i = at(f) if i is None else i
        if i >= N or len(sig) == 0:
            return
        sig = sig[: len(self.x) - i]
        l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
        self.x[i:i + len(sig), 0] += sig * gain * l * 1.414
        self.x[i:i + len(sig), 1] += sig * gain * r * 1.414


dry, verb, drums = Bus(), Bus(), Bus()

# ---------------------------------------------------------------- instruments
def kick(v=1.0):
    t = tt(0.45)
    f = 46 + 120 * np.exp(-t * 30)
    ph = 2 * np.pi * np.cumsum(f) / SR
    s = np.sin(ph) * np.exp(-t * 6.5)
    s[:200] += hp(noise(200), 3000) * 0.4 * np.linspace(1, 0, 200)
    return np.tanh(s * 1.6) * v


def clap(v=1.0):
    t = tt(0.3)
    n = bp(noise(len(t)), 900, 2600)
    env = np.zeros(len(t))
    for d in (0.0, 0.009, 0.018):
        k = int(d * SR)
        env[k:] += np.exp(-(t[: len(t) - k]) * 90)
    env += np.exp(-t * 14) * 0.6
    return n * env * v * 0.6


def hat(v=1.0, open_=False):
    t = tt(0.25 if open_ else 0.06)
    return hp(noise(len(t)), 7500) * np.exp(-t * (14 if open_ else 70)) * v * 0.5


def fm_pluck(n, dur=1.4, v=1.0, ratio=2.0, index=2.4, decay=3.2):
    t = tt(dur)
    f = hz(n)
    mod = np.sin(2 * np.pi * f * ratio * t) * index * np.exp(-t * 9)
    s = np.sin(2 * np.pi * f * t + mod) * np.exp(-t * decay)
    s[:80] *= np.linspace(0, 1, 80)
    return s * v


def bell(n, dur=2.2, v=1.0):
    return fm_pluck(n, dur, v, ratio=3.5, index=1.6, decay=2.0)


def saw(f, t, detune=0.0):
    ph = (f * (1 + detune) * t + rng.random()) % 1.0
    return 2 * ph - 1


def pad_note(n, dur, v=1.0, cutoff=1400, attack=0.25, release=0.7):
    t = tt(dur + release)
    f = hz(n)
    sl = saw(f, t, -0.004) + saw(f, t, 0.0) * 0.6 + saw(f, t, 0.0045)
    sr = saw(f, t, 0.003) + saw(f, t, 0.0) * 0.6 + saw(f, t, -0.005)
    env = np.minimum(1, t / attack) * np.where(t < dur, 1, np.exp(-(t - dur) / release * 3))
    return lp(sl, cutoff) * env * v * PAD, lp(sr, cutoff) * env * v * PAD


def bass_note(n, dur, v=1.0):
    t = tt(dur)
    f = hz(n)
    s = np.sin(2 * np.pi * f * t) + 0.25 * np.sin(4 * np.pi * f * t) + 0.08 * saw(f, t)
    env = np.minimum(1, t / 0.006) * np.exp(-t * 2.2)
    env[-200:] *= np.linspace(1, 0, 200)
    return np.tanh(s * env * 1.4) * v * 0.5


def square_note(n, dur, v=1.0):
    t = tt(dur)
    s = np.sign(np.sin(2 * np.pi * hz(n) * t))
    env = np.minimum(1, t / 0.005) * np.where(t < dur - 0.02, 1, np.linspace(1, 0, len(t)))
    return bp(s * env, 450, 2400) * v * 0.18


# ---------------------------------------------------------------- bruitages
def sfx_tick(v):
    t = tt(0.03)
    return (np.sin(2 * np.pi * 3100 * t) * np.exp(-t * 260) + hp(noise(len(t)), 4000) * np.exp(-t * 400) * 0.3) * v * 0.5


def sfx_click(v):
    t = tt(0.06)
    a = hp(noise(len(t)), 2500) * np.exp(-t * 500)
    b = np.sin(2 * np.pi * 1800 * t) * np.exp(-t * 180) * 0.5
    up = np.zeros(int(0.07 * SR))
    up[: len(t)] = (a + b) * 0.55
    return np.concatenate([(a + b), up]) * v * 0.7


def sfx_thud(v):
    t = tt(0.5)
    f = 42 + 50 * np.exp(-t * 18)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 7)
    s += lp(noise(len(t)), 300) * np.exp(-t * 20) * 0.6
    return np.tanh(s * 1.5) * v * 0.8


def sfx_clock(v, alt):
    t = tt(0.05)
    fc = 1500 if not alt else 1050
    return bp(noise(len(t)), fc * 0.8, fc * 1.25) * np.exp(-t * 160) * v * 1.4


def sfx_pen(v):
    t = tt(0.14)
    am = 0.5 + 0.5 * np.sin(2 * np.pi * 38 * t) ** 2
    return bp(noise(len(t)), 2200, 6500) * am * np.sin(np.pi * t / t[-1]) * v * 0.35


def sfx_pop(v, n=76):
    t = tt(0.07)
    f = hz(n) * (0.7 + 0.5 * (1 - np.exp(-t * 60)))
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 50) * v * 0.5


def sfx_noise_swell(dur, peak_at, v, lo=300, hi=6000):
    """Bruit dont l'enveloppe et la brillance culminent à peak_at (s) : whoosh."""
    t = tt(dur)
    env = np.exp(-((t - peak_at) / (dur * 0.22)) ** 2)
    nz = noise(len(t))
    low = bp(nz, lo, lo * 3.5)
    high = bp(nz, hi * 0.35, min(hi, SR / 2 - 100))
    bright = np.exp(-((t - peak_at) / (dur * 0.12)) ** 2)
    return (low * (1 - 0.6 * bright) + high * bright * 1.3) * env * v * 0.6


def sfx_riser(dur, v):
    t = tt(dur)
    p = t / dur
    f = 220 * 2 ** (p * 2.3)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.3 + hp(noise(len(t)), 2000) * 0.5
    return s * p ** 2.2 * v * 0.5


def sfx_shake(v):
    t = tt(0.08)
    grains = (rng.random(len(t)) < 0.05).astype(float) * rng.standard_normal(len(t))
    return bp(grains + noise(len(t)) * 0.15, 3000, 9000) * np.sin(np.pi * t / t[-1]) * v * 1.2


def sfx_stretch(dur, v):
    t = tt(dur)
    p = t / dur
    f = 150 * 2 ** (p * 1.4) * (1 + 0.03 * np.sin(2 * np.pi * 9 * t))
    ph = np.cumsum(f) / SR
    s = (2 * (ph % 1) - 1)
    return lp(s, 1400) * (0.3 + 0.7 * p) * v * 0.25


def sfx_snap(v):
    t = tt(0.6)
    f = 120 + 900 * np.exp(-t * 40)
    zap = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 18)
    boing_f = 150 * (1 + 0.25 * np.sin(2 * np.pi * 11 * t) * np.exp(-t * 4))
    boing = np.sin(2 * np.pi * np.cumsum(boing_f) / SR) * np.exp(-t * 5) * 0.6
    crack = hp(noise(len(t)), 3000) * np.exp(-t * 300)
    return (zap + boing + crack) * v * 0.6


def sfx_key(v, seed):
    r = np.random.default_rng(seed)
    t = tt(0.04)
    body = np.sin(2 * np.pi * (180 + r.random() * 60) * t) * np.exp(-t * 120)
    clk = bp(r.standard_normal(len(t)), 1800, 4800) * np.exp(-t * 260)
    return (clk + body * 0.6) * v * 0.55


def sfx_impact(v, size=1.0):
    t = tt(1.6 * size)
    f = 38 + 80 * np.exp(-t * 14)
    boom = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * (3.2 / size))
    crash = hp(noise(len(t)), 1500) * np.exp(-t * (7 / size)) * 0.45
    return np.tanh((boom + crash) * 1.3) * v * 0.85


def sfx_reverse(dur, v):
    return sfx_noise_swell(dur, dur * 0.98, v, lo=200, hi=9000) * np.linspace(0.2, 1, int(dur * SR))


# ---------------------------------------------------------------- musique
PROG = [[53, 57, 60, 64], [57, 60, 64, 67], [50, 53, 57, 60], [53, 57, 58, 62]]   # Fmaj7 Am7 Dm7 B♭maj7
ROOT = [41, 45, 38, 34]


def chord_at(f):
    return (int(f) // 60) % 4


def play_pads(f0, f1, v=1.0, cutoff=1400):
    f = f0
    while f < f1:
        nb = min(f1, (f // 60 + 1) * 60)
        ci = chord_at(f)
        for k, n in enumerate(PROG[ci]):
            l, r = pad_note(n, sec(nb - f), v, cutoff)
            verb.x[at(f):at(f) + len(l), 0] += l[: len(verb.x) - at(f)] * 0.6
            verb.x[at(f):at(f) + len(r), 1] += r[: len(verb.x) - at(f)] * 0.6
            dry.x[at(f):at(f) + len(l), 0] += l[: len(dry.x) - at(f)]
            dry.x[at(f):at(f) + len(r), 1] += r[: len(dry.x) - at(f)]
        f = nb


def play_groove(f0, f1, full=True):
    for f in range(f0, f1, BEAT):
        drums.add(kick(1.0), f, gain=0.95)
        if full:
            drums.add(hat(0.9), f + 7.5, gain=0.5, pan=0.3)
            if ((f - f0) // BEAT) % 2 == 1:
                drums.add(clap(1.0), f, gain=0.5)
                verb.add(clap(1.0), f, gain=0.15)
            drums.add(bass_note(ROOT[chord_at(f)] + 12, 0.22, 1.0), f + 7.5, gain=0.7)
            if ((f - f0) // BEAT) % 4 == 3:
                drums.add(hat(0.7, True), f + 7.5, gain=0.35, pan=-0.3)


def play_roll(f0, f1):
    n = 0
    f = float(f0)
    while f < f1:
        p = (f - f0) / (f1 - f0)
        drums.add(clap(0.4 + 0.6 * p), f, gain=0.25 + 0.25 * p)
        f += 3.75 if p < 0.5 else 1.875
        n += 1


def sidechain(x, f0, f1):
    """Pompe les nappes sur la grosse caisse."""
    for f in range(f0, f1, BEAT):
        i = at(f)
        k = int(0.3 * SR)
        seg = x[i:i + k]
        g = 1 - 0.65 * np.exp(-np.arange(len(seg)) / SR * 9)
        seg *= g[:, None]


# intro : nappe discrète
play_pads(0, 60, 0.45, 900)
# audit : musique d'attente téléphonique, carrée et sans relief
hold = [72, 76, 79, 76, 74, 77, 81, 77]
for i, f in enumerate(range(90, 210, 8)):
    dry.add(square_note(hold[i % len(hold)], 0.22, 1.0), f, gain=0.35)
# montée
play_pads(210, 300, 0.6, 1100)
for i, f in enumerate(range(210, 300, 8)):
    n = PROG[chord_at(f)][i % 4] + 12
    verb.add(fm_pluck(n, 0.6, 0.35), f, gain=0.6, pan=0.25 * (-1) ** i)
play_roll(270, 300)
# drop
play_pads(SEC['drop'], 510, 0.9, 1600)
play_groove(SEC['drop'], 450)
play_groove(480, 510)
# break
play_pads(SEC['break'], 630, 0.75, 900)
for f in range(SEC['break'], 630, 60):
    dry.add(bass_note(ROOT[chord_at(f)], 1.9, 0.9), f, gain=0.55)
# ship it
play_pads(SEC['ship'], 690, 0.8, 1300)
play_groove(SEC['ship'], 675, full=False)
play_roll(675, 690)
# drop 2
play_pads(SEC['drop2'], FLY, 0.95, 1800)
play_groove(SEC['drop2'], FLY)
# logo + fin
for n in [41, 53, 57, 60, 64, 67]:
    l, r = pad_note(n, sec(CTA - 1 - BOOM), 0.7, 1500, attack=0.05, release=1.2)
    for b, w in ((dry, 1.0), (verb, 0.7)):
        b.x[at(BOOM):at(BOOM) + len(l), 0] += l * w
        b.x[at(BOOM):at(BOOM) + len(r), 1] += r * w
play_pads(CTA, SEC['final'], 0.55, 1000)
for n in [53, 57, 60, 64, 67, 72]:
    l, r = pad_note(n, sec(TOTAL - SEC['final']), 0.6, 1300, attack=0.4, release=1.5)
    verb.x[at(SEC['final']):at(SEC['final']) + len(l), 0] += l * 0.8
    verb.x[at(SEC['final']):at(SEC['final']) + len(r), 1] += r * 0.8
    dry.x[at(SEC['final']):at(SEC['final']) + len(l), 0] += l * 0.6
    dry.x[at(SEC['final']):at(SEC['final']) + len(r), 1] += r * 0.6
for i, n in enumerate([65, 69, 72, 76, 79]):
    verb.add(bell(n, 2.5, 0.5), SEC['final'] + i * 2, gain=0.5, pan=-0.4 + i * 0.2)

sidechain(dry.x, SEC['drop'], 450)
sidechain(dry.x, 480, 510)
sidechain(dry.x, SEC['drop2'], FLY)
sidechain(verb.x, SEC['drop'], 450)
sidechain(verb.x, SEC['drop2'], FLY)

# ---------------------------------------------------------------- placement des bruitages
for c in CUES:
    f, k, v = c['f'], c['k'], c.get('v', 0.5)
    if k == 'tick':
        dry.add(sfx_tick(v), f, pan=0.1)
    elif k == 'pluck':
        p = fm_pluck(c['n'], 1.3, v)
        dry.add(p, f, gain=0.55, pan=0.15)
        verb.add(p, f, gain=0.45)
    elif k == 'thud':
        dry.add(sfx_thud(v), f)
    elif k == 'clock':
        dry.add(sfx_clock(v, c.get('alt', 0)), f, gain=0.8, pan=0.2 if c.get('alt') else -0.2)
    elif k == 'pen':
        dry.add(sfx_pen(v), f, pan=0.2)
    elif k in ('tag', 'pop'):
        dry.add(sfx_pop(v, c.get('n', 76)), f)
        verb.add(sfx_pop(v, c.get('n', 76)), f, gain=0.3)
    elif k == 'swish':
        d = sec(c.get('dur', 8))
        s = sfx_noise_swell(d, sec(c['peak'] - f), v)
        dry.add(s, f, gain=0.8)
    elif k == 'whoosh':
        d = sec(c.get('dur', 16))
        s = sfx_noise_swell(d, sec(c['peak'] - f), v)
        dry.add(s, f, gain=1.0)
        verb.add(s, f, gain=0.3)
    elif k == 'riser':
        s = sfx_riser(sec(c['end'] - f), v)
        dry.add(s, f, gain=0.8)
        verb.add(s, f, gain=0.3)
    elif k == 'click':
        dry.add(sfx_click(v), f, gain=0.9)
    elif k == 'shake':
        dry.add(sfx_shake(v), f, gain=0.9, pan=0.25)
    elif k in ('shimmer', 'sparkle'):
        end = c.get('end', f + 8)
        r2 = np.random.default_rng(f)
        nn = [84, 88, 91, 96, 100]
        for j, ff in enumerate(np.arange(f, end, 2.0)):
            verb.add(bell(nn[(j * 3 + int(r2.integers(5))) % 5], 1.2, v * 0.25), ff, gain=0.6, pan=float(r2.uniform(-.6, .6)))
    elif k == 'stretch':
        s = sfx_stretch(sec(c['end'] - f), v)
        dry.add(s, f, gain=0.9)
    elif k == 'hit':
        dry.add(sfx_impact(v, 0.8), f, gain=0.7)
        verb.add(sfx_impact(v, 0.8), f, gain=0.3)
    elif k == 'snap':
        dry.add(sfx_snap(v), f, gain=0.9)
    elif k == 'key':
        dry.add(sfx_key(v, f), f, gain=0.9, pan=0.1)
    elif k == 'enter':
        dry.add(sfx_key(1.0, f) * 1.4, f)
        dry.add(sfx_thud(0.25), f)
    elif k == 'impact':
        dry.add(sfx_impact(v), f, gain=0.8)
        verb.add(sfx_impact(v), f, gain=0.25)
    elif k == 'reverse':
        dry.add(sfx_reverse(sec(c['end'] - f), v), f, gain=0.8)
    elif k == 'boom':
        dry.add(sfx_impact(min(1.0, v), 1.6), f, gain=1.0)
        verb.add(sfx_impact(min(1.0, v), 1.6), f, gain=0.45)

# « ok, too much. » : la musique passe sous l'eau jusqu'au retour à 100 %
music = drums.x * 0.5
i0, i1 = at(450), at(476)
for ch in range(2):
    music[i0:i1, ch] = lp(music[i0:i1, ch], 500, 4) * 0.8

# ---------------------------------------------------------------- réverbe + master
ir_t = tt(2.2)
ir = np.stack([lp(noise(len(ir_t)), 6000) * np.exp(-ir_t * 3.0) for _ in range(2)], 1)
ir /= np.sqrt((ir ** 2).sum(0))  # énergie unité : la réverbe n'ajoute pas de gain
wet = np.stack([fftconvolve(verb.x[:, c], ir[:, c])[: len(verb.x)] for c in range(2)], 1) * 0.5
mix = dry.x + music + wet
if os.environ.get('STEMS'):
    def lvl(x):
        m = x.mean(1)
        return ' '.join(f"{20*np.log10(np.sqrt((m[i*SR:(i+1)*SR]**2).mean())+1e-9):5.0f}" for i in range(int(N / SR)))
    print('dry  ', lvl(dry.x)); print('drums', lvl(music)); print('wet  ', lvl(wet)); print('mix  ', lvl(mix))
mix = hp(mix.T, 28).T
mix = mix[: N + int(0.2 * SR)]
fade = int(0.6 * SR)
mix[-fade:] *= np.linspace(1, 0, fade)[:, None]
mix = np.tanh(mix * 0.9) / 0.9
mix /= max(1e-6, np.abs(mix).max()) / 0.89
mix = mix[:N]
wavfile.write(os.path.join(HERE, 'out', 'audio.wav'), SR, (mix * 32767).astype(np.int16))
print('out/audio.wav', f'{len(mix) / SR:.2f} s')
