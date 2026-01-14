#!/usr/bin/python
from __future__ import print_function
__author__ = "Dr. Dinga Wonanke"
__status__ = "production"
import re
from types import SimpleNamespace


def get_times_toks(sentence_toks):
    """
    Extract time/duration expressions from tokenized sentence.

    Returns list of dicts with keys:
      - value : str   (surface quantity: "2", "two", "several", "half", "overnight")
      - units : str   (normalized unit: h, min, d, week, month, year, N/A)
      - text  : str   (surface phrase)
    """

    times = []

    def norm(tok: str) -> str:
        t = tok.lower().strip()
        t = t.replace("–", "-").replace("—", "-")
        return t.strip("()[]{};:,.")

    UNIT_MAP = {
        "s": "s", "sec": "s", "secs": "s", "second": "s", "seconds": "s",
        "m": "min", "min": "min", "mins": "min", "minute": "min", "minutes": "min",
        "h": "h", "hr": "h", "hrs": "h", "hour": "h", "hours": "h",
        "d": "d", "day": "d", "days": "d",
        "w": "week", "wk": "week", "wks": "week", "week": "week", "weeks": "week",
        "mo": "month", "mos": "month", "month": "month", "months": "month",
        "y": "year", "yr": "year", "yrs": "year", "year": "year", "years": "year",
    }

    WORD_NUM = {
        "a", "an",
        "one", "two", "three", "four", "five",
        "six", "seven", "eight", "nine", "ten",
        "half", "quarter"
    }

    AMBIGUOUS = {
        "few", "several", "some", "many",
        "next", "following", "after", "over", "within",
        "for", "different", "successive",
        "additional", "in"
    }

    def parse_number(tok):
        return bool(re.fullmatch(r"[0-9]+(\.[0-9]+)?", tok))

    def in_nmr_context(i: int, window: int = 10) -> bool:
        """
        Returns True if surrounding tokens suggest NMR/chemical-shift assignment text,
        where e.g. '12H' means 12 hydrogens (NOT hours).
        """
        lo = max(0, i - window)
        hi = min(len(sentence_toks), i + window + 1)
        ctx = " ".join(sentence_toks[lo:hi]).lower()

        if "nmr" in ctx or "δ" in ctx or "ppm" in ctx:
            return True

        if re.search(r"\bj\s*=\s*\d", ctx) or "hz" in ctx:
            return True

        if any(s in ctx for s in ["cdcl3", "cd3od", "dmso", "d6", "acetone-d6", "d2o"]):
            return True

        if re.search(r"\b(br|s|d|t|q|m|dd|dt|td|tt)\b", ctx):
            return True

        return False

    def parse_compact(token_raw: str, i: int):
        """
        Returns (num_str, unit_str) or (None, None)
        Adds guard to avoid misclassifying NMR integrals like '12H'.
        """
        t = token_raw.replace(",", "")
        m = re.match(r"^([0-9]+(?:\.[0-9]+)?(?:-[0-9]+)?)\s*([a-zA-Z]+)$", t)
        if not m:
            return None, None

        num = m.group(1)
        unit_raw = m.group(2)

        if unit_raw == "H" and in_nmr_context(i):
            return None, None

        return num, norm(unit_raw)

    i = 0
    N = len(sentence_toks)

    while i < N:
        tok_raw = sentence_toks[i]
        tok = norm(tok_raw)

        nxt_raw = sentence_toks[i+1] if i+1 < N else ""
        nxt = norm(nxt_raw)

        nxt2_raw = sentence_toks[i+2] if i+2 < N else ""
        nxt2 = norm(nxt2_raw)

        if tok in {"overnight", "o/n"}:
            times.append({"value": tok, "units": "N/A", "text": tok_raw})
            i += 1
            continue

        if tok in {"half", "quarter"}:
            if nxt in {"a", "an"} and nxt2 in UNIT_MAP:
                times.append({"value": tok, "units": UNIT_MAP[nxt2], "text": f"{tok_raw} {nxt_raw} {nxt2_raw}"})
                i += 3
                continue
            if nxt in UNIT_MAP:
                times.append({"value": tok, "units": UNIT_MAP[nxt], "text": f"{tok_raw} {nxt_raw}"})
                i += 2
                continue

        if tok in {"a", "an"} and nxt in UNIT_MAP:
            times.append({"value": tok, "units": UNIT_MAP[nxt], "text": f"{tok_raw} {nxt_raw}"})
            i += 2
            continue

        val, unit = parse_compact(tok_raw, i)
        if val and unit in UNIT_MAP:
            times.append({"value": val, "units": UNIT_MAP[unit], "text": tok_raw})
            i += 1
            continue

        if parse_number(tok) and nxt in UNIT_MAP:
            if nxt_raw == "H" and in_nmr_context(i):
                i += 1
                continue

            times.append({"value": tok, "units": UNIT_MAP[nxt], "text": f"{tok_raw} {nxt_raw}"})
            i += 2
            continue

        # --- word numbers: two weeks ---
        if tok in WORD_NUM and nxt in UNIT_MAP:
            times.append({"value": tok, "units": UNIT_MAP[nxt], "text": f"{tok_raw} {nxt_raw}"})
            i += 2
            continue

        # --- ambiguous quantities: several days ---
        if tok in AMBIGUOUS and nxt in UNIT_MAP:
            times.append({"value": tok, "units": UNIT_MAP[nxt], "text": f"{tok_raw} {nxt_raw}"})
            i += 2
            continue

        i += 1

    return times


# def get_times_toks(sentence_toks):
#     """
#     Finds tokens corresponding to temperature values
#     Returns IDs
#     """
#     times = []
#     time_units = ["h", "hr", "hrs", "min", "hour", "hours", "minutes", "d",
#                   "day", "days", 'weeks', 'week', 'month', 'month', 'year', 'years']

#     for num, (tok, next_tok) in enumerate(zip(sentence_toks, sentence_toks[1:])):
#         text = tok + ' ' + next_tok
#         pattern_not_to_match = r'\d-\s*[dhsm]|formed|take'
#         reject_pattern = re.search(pattern_not_to_match, text)
#         if reject_pattern:
#             print('Text checker', text)
#             continue
#         if tok == "overnight":
#             times.append({"tok_id": num, "value": "overnight", "units": "N/A"})
#         elif next_tok == "days":
#             times.append({"tok_id": num, "value": tok, "units": "day"})
#         else:
#             tok_num = re.findall(
#                 "(^[0-9\-\.\,]*)\s*[hrsmind]*", tok)[0].replace(",", "")
#             tok_unit = re.findall("[0-9\-\.\,]*\s*([hrsmind]*$)", tok)[0]
#             tok_unit = next_tok if tok_unit == "" else tok_unit

#             if tok_num != "" and all(t in "0987654321-,." for t in tok_num) and tok_unit in time_units:
#                 times.append(
#                     {"tok_id": num, "value": tok_num, "units": tok_unit})
#     return times

def get_temperatures_toks(sentence_toks):
    """
    Docstring for get_temperatures_toks

    :param sentence_toks: Description
    """

    out = []

    RATE_HINTS = {"/", "min-1", "h-1", "per", "min⁻1", "h⁻1"}

    def norm(tok: str) -> str:
        t = (tok or "").strip().lower()
        t = t.replace("–", "-").replace("—", "-").replace("−", "-")
        return t.strip("()[]{};:,.")

    def join_text(toks):
        return " ".join(toks).replace(" - ", "-").replace(" °", "°").strip()

    def is_rate_context(i: int) -> bool:
        window = " ".join(sentence_toks[i:min(i + 5, len(sentence_toks))]).lower()
        return any(h in window for h in RATE_HINTS)

    def norm_unit(u: str) -> str:
        u = (u or "").strip().replace(" ", "")
        u = u.replace("°c", "°C")
        # preserve explicit ° where present
        if u in {"°C", "K", "°F"}:
            return u
        if u == "C":
            return "°C"
        if u == "°":
            return "°C"
        if u == "k":
            return "K"
        if u in {"f", "F"}:
            return "°F"
        if u == "°F":
            return "°F"
        return u

    ISOTOPE_TOKEN = re.compile(r"^\s*\d{1,3}\s*(C|H|P|F|N)\s*[\]}),;:.]*\s*$", re.I)
    NMR_TOKEN = re.compile(r"^(nmr|n\.m\.r\.?)$", re.I)

    def is_isotope_nmr_context(i: int) -> bool:
        """
        True if token looks like isotope label AND nearby tokens indicate NMR context.
        We DO NOT block tokens containing a degree sign (e.g., 13°C is real).
        """
        if i >= len(sentence_toks):
            return False

        tok = sentence_toks[i] or ""
        if "°" in tok:
            return False

        if not ISOTOPE_TOKEN.match(tok):
            return False


        for j in range(max(0, i - 3), min(len(sentence_toks), i + 5)):
            if NMR_TOKEN.match(norm(sentence_toks[j])):
                return True

        if i + 1 < len(sentence_toks) and NMR_TOKEN.match(norm(sentence_toks[i + 1])):
            return True

        return False

    def parse_numeric_temp_at(i: int):
        if i >= len(sentence_toks):
            return None, None, 0, None
        if is_rate_context(i):
            return None, None, 0, None

        if is_isotope_nmr_context(i):
            return None, None, 0, None

        t0_raw = sentence_toks[i]
        t0 = (t0_raw or "").replace(",", "")
        t0n = norm(t0_raw)

        t1_raw = sentence_toks[i + 1] if i + 1 < len(sentence_toks) else ""
        t1n = norm(t1_raw)

        t2_raw = sentence_toks[i + 2] if i + 2 < len(sentence_toks) else ""
        t2n = norm(t2_raw)

        t3_raw = sentence_toks[i + 3] if i + 3 < len(sentence_toks) else ""
        # t3n = norm(t3_raw)

        t0_clean = re.sub(
            r"^[~∼≈≃≅≒≓≍≌≉≊≋≔≕≖≗≘≙≚≛≜≝≞≟≠≡≢≣≦≧≨≩≪≫≤≥<>]+",
            "",
            t0
        ).strip()

        m = re.match(
            r"^([+-]?\d+(?:\.\d+)?(?:-\d+(?:\.\d+)?)?)\s*(°?\s*[CKF]|°c|°C|K|C|F|°F)?$",
            t0_clean
        )
        if m:
            val = m.group(1)
            unit = norm_unit((m.group(2) or "").replace(" ", ""))

            if unit in {"°C", "K", "°F"}:
                return val, unit, 1, t0_raw

            # unit in next token: "235 °C" or "235 C"
            if unit == "":
                if re.fullmatch(r"(°c|°C|C|K|F|°F)", (t1_raw or "").strip()):
                    unit2 = norm_unit((t1_raw or "").strip())
                    return val, unit2, 2, join_text([t0_raw, t1_raw])

                # split degree: "235" "°" "C"
                if (t1_raw or "").strip() == "°" and re.fullmatch(r"(c|C|k|K|f|F)", (t2_raw or "").strip()):
                    unit2 = norm_unit("°" + (t2_raw or "").strip().upper())
                    return val, unit2, 3, join_text([t0_raw, t1_raw, t2_raw])

        # B) split range: "80 - 100 °C" or "80 to 100 °C"
        if re.fullmatch(r"[+-]?\d+(\.\d+)?", t0n):
            if t1n in {"-", "to"} and re.fullmatch(r"[+-]?\d+(\.\d+)?", t2n):

                # unit as token i+3
                if re.fullmatch(r"(°c|°C|C|K|F|°F)", (t3_raw or "").strip()):
                    val = f"{t0n}-{t2n}"
                    unit = norm_unit((t3_raw or "").strip())
                    return val, unit, 4, join_text(sentence_toks[i:i + 4])

                # unit split: "... 100 ° C"
                if (t3_raw or "").strip() == "°" and i + 4 < len(sentence_toks):
                    t4_raw = sentence_toks[i + 4]
                    if re.fullmatch(r"(c|C|k|K|f|F)", (t4_raw or "").strip()):
                        val = f"{t0n}-{t2n}"
                        unit = norm_unit("°" + (t4_raw or "").strip().upper())
                        return val, unit, 5, join_text(sentence_toks[i:i + 5])

        # C) plain split: "235 °C" / "235 C"
        if re.fullmatch(r"[+-]?\d+(\.\d+)?", t0n):
            if re.fullmatch(r"(°c|°C|C|K|F|°F)", (t1_raw or "").strip()):
                unit = norm_unit((t1_raw or "").strip())
                return t0n, unit, 2, join_text([t0_raw, t1_raw])

            # "235 ° C"
            if (t1_raw or "").strip() == "°" and re.fullmatch(r"(c|C|k|K|f|F)", (t2_raw or "").strip()):
                unit = norm_unit("°" + (t2_raw or "").strip().upper())
                return t0n, unit, 3, join_text([t0_raw, t1_raw, t2_raw])

        return None, None, 0, None

    # -----------------------------
    # Textual phrases ("room temp", etc.)
    # -----------------------------
    TEXT_PHRASES = [
        (("room", "temperature"), ("RT", "N/A", "temperature")),
        (("room", "temp"),        ("RT", "N/A", "temperature")),
        (("room", "temp."),       ("RT", "N/A", "temperature")),
        (("at", "room", "temperature"), ("RT", "N/A", "temperature")),
        (("at", "room", "temp"),        ("RT", "N/A", "temperature")),
        (("rt",),                 ("RT", "N/A", "temperature")),
        (("r.t",),                ("RT", "N/A", "temperature")),
        (("r.t.",),               ("RT", "N/A", "temperature")),

        (("ambient", "temperature"), ("AT", "N/A", "temperature")),
        (("ambient", "temp"),        ("AT", "N/A", "temperature")),
        (("ambient", "temp."),       ("AT", "N/A", "temperature")),
        (("at", "ambient"),          ("AT", "N/A", "temperature")),
        (("at", "ambient", "temperature"), ("AT", "N/A", "temperature")),

        (("ice", "bath"),  ("ice bath", "N/A", "temperature")),
        (("ice-bath",),    ("ice bath", "N/A", "temperature")),
        (("on", "ice"),    ("ice", "N/A", "temperature")),
        (("in", "ice"),    ("ice", "N/A", "temperature")),
        (("cold", "room"), ("cold room", "N/A", "temperature")),
        (("refrigerator",),("refrigerator", "N/A", "temperature")),
        (("fridge",),      ("fridge", "N/A", "temperature")),
        (("freezer",),     ("freezer", "N/A", "temperature")),
    ]


    RT_REGEX = re.compile(r"^(rt|r\.t\.?)$", re.I)

    # ambient single-token variants only (NO "at")
    AT_REGEX = re.compile(r"^(ambient([-_\s]?temp(erature)?)?|amb\.?)$", re.I)

    KIND_MARKERS = [
        ("melting_point", re.compile(r"^(mp|m\.p\.?|mpt|m\.pt\.?)$", re.I)),
        ("boiling_point", re.compile(r"^(bp|b\.p\.?)$", re.I)),
        ("glass_transition", re.compile(r"^(tg|t_g)$", re.I)),
        ("melting_temperature", re.compile(r"^(tm|t_m)$", re.I)),
        ("freezing_point", re.compile(r"^(fp|f\.p\.?)$", re.I)),
    ]

    MULTI_MARKERS = [
        ("melting_point", ("melting", "point")),
        ("boiling_point", ("boiling", "point")),
        ("decomposition_temperature", ("decomposition", "temperature")),
        ("decomposition_temperature", ("decomposition", "temp")),
        ("decomposition_temperature", ("decomp", "temp")),
        ("decomposition_temperature", ("decomp", "temperature")),
        ("freezing_point", ("freezing", "point")),
        ("glass_transition", ("glass", "transition")),
        ("melting_temperature", ("melting", "temperature")),
    ]

    DECOMP_QUAL = re.compile(r"\b(dec\.?|decomp|decomposition)\b", re.I)

    phrases_by_len = {}
    for toks, info in TEXT_PHRASES:
        phrases_by_len.setdefault(len(toks), []).append((tuple(toks), info))

    def add(value, units, text, kind):
        out.append({"value": value, "units": units, "text": text, "kind": kind})

    i = 0
    N = len(sentence_toks)

    while i < N:
        t0 = norm(sentence_toks[i])
        if is_isotope_nmr_context(i):
            i += 1
            continue

        matched_property = False
        for kind, marker_tokens in MULTI_MARKERS:
            L = len(marker_tokens)
            if i + L <= N:
                window = tuple(norm(x) for x in sentence_toks[i:i + L])
                if window == marker_tokens:
                    num, unit, consumed, text_num = parse_numeric_temp_at(i + L)
                    if num is not None:
                        qual_window = " ".join(
                            norm(sentence_toks[j]) for j in range(i, min(i + L + consumed + 6, N))
                        )
                        kind2 = "decomposition_temperature" if DECOMP_QUAL.search(qual_window) else kind
                        add(
                            num,
                            unit,
                            join_text(sentence_toks[i:i + L] + ([text_num] if text_num else [])),
                            kind2,
                        )
                        i = i + L + consumed
                    else:
                        add(" ".join(marker_tokens), "N/A", join_text(sentence_toks[i:i + L]), kind)
                        i += L
                    matched_property = True
                    break
        if matched_property:
            continue

        marker_kind = None
        for kind, rgx in KIND_MARKERS:
            if rgx.match(t0):
                marker_kind = kind
                break

        if marker_kind is not None:
            num, unit, consumed, text_num = parse_numeric_temp_at(i + 1)
            if num is not None:
                qual_window = " ".join(
                    norm(sentence_toks[j]) for j in range(i, min(i + 1 + consumed + 6, N))
                )
                kind2 = "decomposition_temperature" if DECOMP_QUAL.search(qual_window) else marker_kind
                add(
                    num,
                    unit,
                    join_text([sentence_toks[i]] + ([text_num] if text_num else sentence_toks[i + 1:i + 1 + consumed])),
                    kind2,
                )
                i = i + 1 + consumed
            else:
                add(sentence_toks[i], "N/A", sentence_toks[i], marker_kind)
                i += 1
            continue

        matched = False
        for L in (4, 3, 2, 1):
            if i + L > N:
                continue
            window = tuple(norm(x) for x in sentence_toks[i:i + L])
            for phrase, (value, units, kind) in phrases_by_len.get(L, []):
                if window == phrase:
                    add(value, units, join_text(sentence_toks[i:i + L]), kind)
                    i += L
                    matched = True
                    break
            if matched:
                break
        if matched:
            continue

        if RT_REGEX.match(t0):
            add("RT", "N/A", sentence_toks[i], "temperature")
            i += 1
            continue

        if AT_REGEX.match(t0):
            add("AT", "N/A", sentence_toks[i], "temperature")
            i += 1
            continue

        num, unit, consumed, text_num = parse_numeric_temp_at(i)
        if num is not None and unit is not None:
            qual_window = " ".join(
                norm(sentence_toks[j]) for j in range(max(0, i - 3), min(i + consumed + 5, N))
            )
            kind = "decomposition_temperature" if DECOMP_QUAL.search(qual_window) else "temperature"
            add(num, unit, text_num or join_text(sentence_toks[i:i + consumed]), kind)
            i += consumed
            continue

        i += 1

    return out




# def get_temperatures_toks(sentence_toks):
#     """
#     Finds tokens corresponding to temperature values
#     Returns IDs
#     """
#     temperatures = []
#     rate_units = ["/", "min-1", "h-1", "per"]

#     for num, (tok, next_tok) in enumerate(zip(sentence_toks, sentence_toks[1:])):
#         if tok == "room" and sentence_toks[num - 1] != "from":
#             temperatures.append({"tok_id": num, "value": "RT", "units": "N/A"})
#         else:
#             tok_num = re.findall(
#                 "(^[0-9\-\.\,]*)\s*[°KC]*", tok)[0].replace(",", "")
#             tok_unit = re.findall("[0-9\-\.\,]*\s*([°KC]*$)", tok)[0]
#             tok_unit = next_tok if tok_unit == "" else tok_unit
#             tok_unit = '°C' if tok_unit == '°' else tok_unit
#             next_toks = "".join([sentence_toks[i] for i in range(
#                 num + 1, num + 4) if i < len(sentence_toks)])

#             # temperature token contains allowed symbols
#             # units of temperature
#             # units are not temperature rate
#             if tok_num != "" \
#                     and all(t in "0987654321-." for t in tok_num) \
#                     and all(t in "°KC" for t in tok_unit) \
#                     and all(r not in next_toks for r in rate_units):
#                 temperatures.append(
#                     {"tok_id": num, "value": tok_num, "units": tok_unit})

#     return temperatures


def get_environment(sentence, materials_):
    """
    Docstring for get_environment

    :param sentence: Description
    :param materials_: Description
    """

    with_ids = [t.i for t in sentence if t.text in ["with", "into"]]
    in_ids = [t.i for t in sentence if t.text in ["in", "under"]]
    atmospheres = ["inert", "reducing", "oxidizing"]
    env_materials = [m for m in materials_]
    env_materials.extend({"text": t.text, "tok_ids": [
                         t.i]} for t in sentence if t.text in atmospheres)

    def get_token_ids(media_ids, materials):
        m_id = 0
        media_tok = ""
        media_tok_id = []
        while m_id < len(materials) and not media_tok:
            mat_text = materials[m_id]['text']
            mat_toks = materials[m_id]['tok_ids']
            mat_tok = mat_toks[0]
            if any(mat_tok > i for i in media_ids):
                media_tok = mat_text
                media_tok_id = mat_toks
            m_id = m_id + 1
        return media_tok_id, media_tok

    in_media_id, in_media = get_token_ids(in_ids, env_materials)
    with_media_id, with_media = get_token_ids(with_ids, env_materials)

    return [in_media_id, with_media_id], [in_media, with_media]


def tok2nums(tokens, sentence):
    values = []
    for t_tok in reversed(tokens):
        t_id = t_tok["tok_id"]
        if all(sentence[t_id].i not in t["tok_ids"] for t in values):
            try:
                t_value = __get_tok_values([t.text for t in sentence], t_tok)
                t_value["tok_ids"] = [sentence[t].i for t in t_value["tok_ids"]]
                t_value["flag"] = t_tok.get("flag", "")
                values.append(t_value)
            except Exception:
                pass
    return values

# def tok2nums(tokens, sentence):
#     values = []
#     for t_tok in reversed(tokens):
#         t_id = t_tok["tok_id"]
#         if all(sentence[t_id].i not in t["tok_ids"] for t in values):
#             try:
#                 t_value = __get_tok_values([t.text for t in sentence], t_tok)
#                 t_value["tok_ids"] = [
#                     sentence[t].i for t in t_value["tok_ids"]]
#                 values.append(t_value)
#             except:
#                 pass
#     return values


def __is_valid_temp_token(token, units):
    if token in ["and", ",", "to", "-", "or"]:
        return True
    token_str = token.replace(units, "")
    if all(c in "0987654321,." for c in token_str):
        return True

    return False


def __get_temperatures_list(sentence_tokens, token):
    temp_list = []
    current_id = token["tok_id"]
    current_tok = sentence_tokens[current_id]
    units = token["units"]

    # print("->", current_id, current_tok, sentence["tokens"][temp_id-1])

    while current_id > 0 and __is_valid_temp_token(current_tok, units):
        tok_num = re.sub("([0-9\.\,]*)\s*[°A-Za-z]*",
                         "\\1", current_tok).replace(",", "")
        if tok_num != "":
            temp_list.append((tok_num, current_id))

        # print("-->", tok_num, sentence["tokens"][current_id-1])

        current_id = current_id - 1
        current_tok = sentence_tokens[current_id]

    return temp_list, current_id


def __break_temperature_range(temp_list, first_token):
    # range: "... - ..."
    if len(temp_list) == 3 and any(t[0] == '-' for t in temp_list):
        return {"min": float(temp_list[0][0]),
                "max": float(temp_list[2][0]),
                "values": [],
                "tok_ids": [temp_list[0][1], temp_list[2][1]]}

    # range: "between ... and ...", "from ... to ..."
    if first_token in ["between", "from"] and len(temp_list) == 2:
        return {"min": float(temp_list[0][0]),
                "max": float(temp_list[1][0]),
                "values": [],
                "tok_ids": [temp_list[0][1], temp_list[1][1]]}

    # range "up to ..."
    if first_token == "up" and len(temp_list) == 1:
        return {"min": None,
                "max": float(temp_list[0][0]),
                "values": [float(temp_list[0][0])],
                "tok_ids": [temp_list[0][1]]}

    # list of values
    values = [float(t[0]) for t in temp_list]
    return {"max": max(values) if values else None,
            "min": min(values) if values else None,
            "values": values,
            "tok_ids": [t[1] for t in temp_list]}


def __get_tok_values(sentence_tokens, token):
    # overnight
    if token["value"] in ['overnight']:
        return {"max": float(12),
                "min": float(12),
                "values": [float(12)],
                "tok_ids": [token["tok_id"]],
                "units": 'h'}

    # room temperature / ambient / lab (default 25 °C)
    if token["value"] in ['RT', 'room temperature', 'AT']:
        return {"max": float(25),
                "min": float(25),
                "values": [float(25)],
                "tok_ids": [token["tok_id"]],
                "units": '°C'}

    # ice bath (~0 °C)
    if token["value"] in ['ICE']:
        return {"max": float(0),
                "min": float(0),
                "values": [float(0)],
                "tok_ids": [token["tok_id"]],
                "units": '°C'}

    # fridge / cold room (typical ~4 °C)
    if token["value"] in ['FRIDGE']:
        return {"max": float(4),
                "min": float(4),
                "values": [float(4)],
                "tok_ids": [token["tok_id"]],
                "units": '°C'}

    # freezer (typical ~-20 °C)
    if token["value"] in ['FREEZER']:
        return {"max": float(-20),
                "min": float(-20),
                "values": [float(-20)],
                "tok_ids": [token["tok_id"]],
                "units": '°C'}

    # multiple values or range
    temp_id = token["tok_id"]
    if sentence_tokens[temp_id - 1] in [",", "and", "to", "or"] and "-" not in sentence_tokens[temp_id]:
        temp_list, first_tok_id = __get_temperatures_list(
            sentence_tokens, token)
        temp_data = __break_temperature_range(
            temp_list, sentence_tokens[first_tok_id])
        temp_data["units"] = token["units"]
        return temp_data

    token_num = re.sub("([0-9\.\,\-]*)\s*[°A-Za-z]*", "\\1",
                       sentence_tokens[temp_id]).replace(",", "")
    range_values = re.split("-", token_num)

    # single value
    if len(range_values) == 1:
        value = float(range_values[0])
        return {"max": value,
                "min": value,
                "values": [value],
                "tok_ids": [temp_id],
                "units": token["units"]}

    value_1 = range_values[0]
    value_2 = range_values[1]

    # "...-..."
    if value_1 != "" and value_2 != "":
        values = [float(value_1), float(value_2)]
        return {"max": max(values),
                "min": min(values),
                "values": [],
                "tok_ids": [temp_id],
                "units": token["units"]}

    # "... ° -... °"
    if sentence_tokens[temp_id - 1] == "°" and value_1 == "":
        value = re.sub("([0-9\.\,\-]*)\s*[°A-Za-z]*", "\\1",
                       sentence_tokens[temp_id - 2]).replace(", ", "")
        return {"max": float(value_2),
                "min": float(value),
                "values": [],
                "tok_ids": [temp_id, temp_id - 2],
                "units": token["units"]}

    # negative temperature
    return {"max": float(token_num),
            "min": float(token_num),
            "values": [float(token_num)],
            "tok_ids": [temp_id],
            "units": token["units"]}


def get_ph_toks(sentence_toks):
    """
    Finds tokens corresponding to pH values.
    Returns list of dicts: tok_id, value, units, flag

    Handles:
      - pH 7, pH=7.4, pH ~ 2, pH: 3
      - compact: pH7, pH7.4
      - ranges: pH 2-3, pH 2 – 3, pH 2 to 3
    """
    phs = []

    def norm(tok: str) -> str:
        t = tok.lower().strip()
        t = t.replace("–", "-").replace("—", "-")
        t = t.strip("()[]{};:,.")
        return t

    def parse_number(token: str):
        t = token.replace(",", "")
        if re.match(r"^[0-9]+(\.[0-9]+)?$", t):
            return t
        return None

    def parse_range_triplet(a, b, c):
        # "2 - 3" or "2 to 3"
        n1 = parse_number(a)
        n2 = parse_number(c)
        if n1 and n2 and b in {"-", "to"}:
            return f"{n1}-{n2}"
        return None

    i = 0
    N = len(sentence_toks)

    while i < N:
        tok = norm(sentence_toks[i])

        # compact: "ph7" / "ph7.4" / "ph=7.4"
        m = re.match(r"^ph\s*[:=~]?\s*([0-9]+(?:\.[0-9]+)?)$", tok)
        if m:
            phs.append({"tok_id": i, "value": m.group(1), "units": "N/A", "flag": ""})
            i += 1
            continue

        # split: "pH" followed by number (possibly after '=' ':' '~')
        if tok == "ph":
            # skip optional punctuation token like "=", ":", "~"
            j = i + 1
            if j < N and norm(sentence_toks[j]) in {"=", ":", "~", "≈"}:
                j += 1

            # range: pH 2 - 3 / pH 2 to 3
            if j + 2 < N:
                a = norm(sentence_toks[j])
                b = norm(sentence_toks[j+1])
                c = norm(sentence_toks[j+2])
                rng = parse_range_triplet(a, b, c)
                if rng:
                    phs.append({"tok_id": i, "value": rng, "units": "N/A", "flag": ""})
                    i = j + 3
                    continue

            # single value
            if j < N:
                n = parse_number(norm(sentence_toks[j]))
                if n:
                    phs.append({"tok_id": i, "value": n, "units": "N/A", "flag": ""})
                    i = j + 1
                    continue

        i += 1

    return phs

def get_atmosphere_toks(sentence):
    """
    Extract operating conditions from a sentence and return STRUCTURED buckets:

    param sentence: List of tokens (with .text and .i attributes)

    Returns:
      {
        "atmosphere": [ {value, text, mode, composition?, pressure?, pressure_units?} ... ],
        "pressure":   [ {value, units, text, kind} ... ],
        "vessel":     [ {value, text, qualifiers?} ... ],
        "humidity":   [ {value, units, text} ... ],
      }
    """


    # ---------- helpers ----------
    def _wrap_tokens(x):
        if len(x) > 0 and hasattr(x[0], "text") and hasattr(x[0], "i"):
            return list(x)
        return [SimpleNamespace(text=str(t), i=i) for i, t in enumerate(list(x))]

    toks = _wrap_tokens(sentence)

    def norm(x: str) -> str:
        s = (x or "").strip()
        s = s.replace("–", "-").replace("—", "-").replace("−", "-")
        return s.lower().strip("()[]{};:,.")

    def raw(i: int) -> str:
        return toks[i].text if 0 <= i < len(toks) else ""

    def span_text(i, j):
        return " ".join(t.text for t in toks[i:j]).replace(" - ", "-").strip()

    # ---------- canonical maps ----------
    # NOTE: removed "co": "CO" to avoid Co -> CO mistakes.
    GAS_MAP = {
        "n2": "N2", "nitrogen": "N2", "dinitrogen": "N2",
        "ar": "Ar", "argon": "Ar",
        "he": "He", "helium": "He",
        "h2": "H2", "hydrogen": "H2",
        "o2": "O2", "oxygen": "O2",
        "co2": "CO2", "carbon dioxide": "CO2",
        "nh3": "NH3", "ammonia": "NH3",
        "air": "air",
        "ch4": "CH4", "methane": "CH4",
        # qualitative
        "inert": "inert",
        "reducing": "reducing",
        "oxidizing": "oxidizing",
        "vacuum": "vacuum", "vacuo": "vacuum",
    }

    PRESS_UNITS = {
        "pa": "Pa", "kpa": "kPa", "mpa": "MPa", "gpa": "GPa",
        "bar": "bar", "mbar": "mbar",
        "atm": "atm", "atmosphere": "atm", "atmospheres": "atm",
        "torr": "Torr", "mmhg": "mmHg",
        "psi": "psi",
    }

    # Vessels/apparatus
    VESSELS = {
        "autoclave": "autoclave",
        "bomb": "bomb",
        "ampoule": "ampoule",
        "tube": "tube",
        "vessel": "vessel",
        "reactor": "reactor",
        "schlenk": "schlenk",
        "glovebox": "glovebox",
        "glove-box": "glovebox",
    }

    MODES = {
        "flowing", "flow", "purged", "purge", "sparged", "sparge",
        "blanket", "blanketed", "sealed", "seal", "sealed-off",
        "pressurized", "pressurised", "pressurize", "pressurise",
        "degassed", "bubbled", "bubbling", "backfilled", "backfill",
        "evacuated", "evacuation",
    }

    TRIGGERS = {"under", "in", "with", "into", "on", "at", "within"}

    # Words that indicate the gas token is part of an atmosphere phrase
    ATMOS_CONTEXT_WORDS = {
        "atmosphere", "atmospheric", "conditions", "environment",
        "purged", "purge", "sparged", "sparge", "flowing", "blanketed", "backfilled",
        "under", "in", "with", "into",
    }

    # Common metal symbols we do NOT want to treat as gases
    # (this is intentionally broad; it only matters when a token is standing alone)
    METAL_SYMBOLS = {
        "co", "ni", "zn", "cu", "fe", "mn", "cr", "mg", "ca", "ba", "sr", "pb", "ag", "au",
        "al", "ga", "in", "sn", "ti", "zr", "hf", "v", "mo", "w", "ru", "rh", "pd", "pt",
    }

    # ---------- parsers ----------
    def canon_unit(token_text: str):
        return PRESS_UNITS.get(norm(token_text), None)

    def parse_number(tok_text: str):
        t = (tok_text or "").replace(",", "")
        return t if re.match(r"^[0-9]+(\.[0-9]+)?$", t) else None

    def parse_range(tok_text: str):
        t = (tok_text or "").replace(",", "")
        return t if re.match(r"^[0-9]+(\.[0-9]+)?-[0-9]+(\.[0-9]+)?$", t) else None

    def parse_number_or_range(tok_text: str):
        return parse_range(tok_text) or parse_number(tok_text)

    # humidity
    RH_UNIT = re.compile(r"^(rh|r\.h\.|%rh|%r\.h\.)$", re.I)
    REL_HUMID = re.compile(r"^(relative)$", re.I)
    HUMIDITY_WORD = re.compile(r"^(humidity|humid)$", re.I)

    def try_humidity(i):
        N = len(toks)

        # "60% RH"
        m = re.match(r"^([0-9]+(\.[0-9]+)?)%$", (raw(i) or "").strip())
        if m and i + 1 < N and RH_UNIT.match((raw(i + 1) or "").strip()):
            return i + 2, {"value": m.group(1), "units": "%RH", "text": span_text(i, i + 2)}

        # "60 % RH"
        if i + 2 < N and parse_number(norm(raw(i))) and norm(raw(i + 1)) == "%" and RH_UNIT.match((raw(i + 2) or "").strip()):
            return i + 3, {"value": parse_number(norm(raw(i))), "units": "%RH", "text": span_text(i, i + 3)}

        # "40% relative humidity"
        m = re.match(r"^([0-9]+(\.[0-9]+)?)%$", (raw(i) or "").strip())
        if m and i + 2 < N and REL_HUMID.match(norm(raw(i + 1))) and HUMIDITY_WORD.match(norm(raw(i + 2))):
            return i + 3, {"value": m.group(1), "units": "%RH", "text": span_text(i, i + 3)}

        # "relative humidity 40%"
        if i + 2 < N and REL_HUMID.match(norm(raw(i))) and HUMIDITY_WORD.match(norm(raw(i + 1))):
            m = re.match(r"^([0-9]+(\.[0-9]+)?)%$", (raw(i + 2) or "").strip())
            if m:
                return i + 3, {"value": m.group(1), "units": "%RH", "text": span_text(i, i + 3)}

        # "humid air"
        if norm(raw(i)) == "humid" and i + 1 < N and norm(raw(i + 1)) == "air":
            return i + 2, {"value": "humid air", "units": "N/A", "text": span_text(i, i + 2)}

        return None

    def try_pressure_at(i):
        N = len(toks)
        if i + 1 >= N:
            return None
        n = parse_number_or_range(norm(raw(i)))
        if not n:
            return None
        u = canon_unit(raw(i + 1))
        if not u:
            return None
        return i + 2, {"value": n, "units": u, "text": span_text(i, i + 2), "kind": "pressure"}

    def try_pressure_parenthetical(i):
        N = len(toks)
        if i + 3 >= N:
            return None
        if raw(i) not in {"(", "["}:
            return None
        n = parse_number_or_range(norm(raw(i + 1)))
        u = canon_unit(raw(i + 2))
        close_ok = raw(i + 3) in {")", "]"}
        if n and u and close_ok:
            return i + 4, {"value": n, "units": u, "text": span_text(i, i + 4), "kind": "pressure"}
        return None

    def canon_gas_at(i: int):
        """
        Return (gas_value, consumed_tokens) or (None, 0)
        """
        N = len(toks)
        t0_raw = raw(i)
        t0 = norm(t0_raw)

        # phrase: carbon monoxide / carbon dioxide
        if i + 1 < N and t0 == "carbon":
            t1 = norm(raw(i + 1))
            if t1 == "monoxide":
                return "CO", 2
            if t1 == "dioxide":
                return "CO2", 2

        # CO must be written as "CO" (exact) to count as gas
        if t0_raw == "CO":
            return "CO", 1

        # Regular gases from map (case-insensitive key)
        if t0 in GAS_MAP:
            # guard: metal symbols like "Co" appear as "co" after norm()
            # If original token is exactly a metal symbol casing (Co/Ni/Zn etc.), do NOT treat as gas
            # unless it's in atmosphere context (handled outside).
            return GAS_MAP[t0], 1

        return None, 0

    def is_atmosphere_context(i_start: int, i_end: int):
        """
        Require context so we don't treat bare tokens like "Co" in "(M=Co, Ni, Zn)" as atmosphere.
        Checks a small window around the span for triggers/modes/words like 'atmosphere'.
        """
        N = len(toks)
        w0 = max(0, i_start - 3)
        w1 = min(N, i_end + 4)
        window_norm = [norm(raw(k)) for k in range(w0, w1)]
        window_raw = [raw(k) for k in range(w0, w1)]

        # any obvious context word?
        if any(w in ATMOS_CONTEXT_WORDS for w in window_norm):
            return True

        # specific patterns: "<gas> atmosphere"
        if i_end < N and norm(raw(i_end)) in {"atmosphere", "conditions", "environment"}:
            return True

        # avoid formula lists: contains "m" "=" nearby, like "(M=Co, Ni, Zn)"
        if "m" in window_norm and "=" in window_raw:
            return False

        return False

    def try_mixture(i):
        """
        Detect mixtures:
          - 5% H2 in N2
          - H2/N2 (5/95) or H2 / N2
        """
        N = len(toks)

        # A) "<pct>% <gas1> in <gas2>"
        if i + 3 < N:
            t0 = norm(raw(i))
            t1 = norm(raw(i + 1))

            pct = None
            g1_idx = None

            if re.match(r"^[0-9]+(\.[0-9]+)?%$", t0):
                pct = t0
                g1_idx = i + 1
            elif parse_number(t0) and t1 == "%":
                pct = f"{t0}%"
                g1_idx = i + 2

            if g1_idx is not None and g1_idx + 2 < N:
                g1, c1 = canon_gas_at(g1_idx)
                mid = norm(raw(g1_idx + 1))
                g2, c2 = canon_gas_at(g1_idx + 2)
                if g1 and c1 == 1 and g2 and c2 == 1 and mid in {"in", "into"}:
                    comp = f"{pct} {g1} in {g2}"
                    return g1_idx + 3, {"value": f"{g1}/{g2}", "text": span_text(i, g1_idx + 3), "composition": comp, "mode": ""}

        # B) single token like "H2/N2"
        m = re.match(r"^([A-Za-z0-9]+)\/([A-Za-z0-9]+)$", (raw(i) or "").strip())
        if m:
            g1 = GAS_MAP.get(m.group(1).lower())
            g2 = GAS_MAP.get(m.group(2).lower())
            # allow CO only if written CO
            if m.group(1) == "CO":
                g1 = "CO"
            if m.group(2) == "CO":
                g2 = "CO"
            if g1 and g2:
                j = i + 1
                comp_txt = raw(i)
                if j < N and re.match(r"^\(?\d+(\.\d+)?[\/:]\d+(\.\d+)?\)?$", norm(raw(j))):
                    comp_txt = span_text(i, j + 1)
                    j += 1
                return j, {"value": f"{g1}/{g2}", "text": comp_txt, "composition": comp_txt, "mode": ""}

        # C) split tokens: "H2" "/" "N2"
        if i + 2 < N and norm(raw(i + 1)) == "/":
            g1, c1 = canon_gas_at(i)
            g2, c2 = canon_gas_at(i + 2)
            if g1 and c1 == 1 and g2 and c2 == 1:
                j = i + 3
                comp_txt = span_text(i, j)
                if j < N and re.match(r"^\(?\d+(\.\d+)?[\/:]\d+(\.\d+)?\)?$", norm(raw(j))):
                    comp_txt = span_text(i, j + 1)
                    j += 1
                return j, {"value": f"{g1}/{g2}", "text": comp_txt, "composition": comp_txt, "mode": ""}

        return None

    # ---------- output ----------
    out_struct = {"atmosphere": [], "pressure": [], "vessel": [], "humidity": []}

    def add_atmos(value, text, mode="", pressure=None, pressure_units=None, composition=None):
        item = {"value": value, "text": text, "mode": mode}
        if composition:
            item["composition"] = composition
        if pressure is not None and pressure_units is not None:
            item["pressure"] = pressure
            item["pressure_units"] = pressure_units
        out_struct["atmosphere"].append(item)

    def add_pressure(value, units, text, kind="pressure"):
        out_struct["pressure"].append({"value": value, "units": units, "text": text, "kind": kind})

    def add_vessel(value, text, qualifiers=None):
        item = {"value": value, "text": text}
        if qualifiers:
            item["qualifiers"] = qualifiers
        out_struct["vessel"].append(item)

    def add_humidity(value, units, text):
        out_struct["humidity"].append({"value": value, "units": units, "text": text})

    # ---------- scan ----------
    i = 0
    N = len(toks)

    def match_phrase(i, phrase_tokens):
        L = len(phrase_tokens)
        if i + L > N:
            return False
        return [norm(raw(i + k)) for k in range(L)] == list(phrase_tokens)

    while i < N:
        # humidity
        h = try_humidity(i)
        if h:
            j, item = h
            add_humidity(item["value"], item["units"], item["text"])
            i = j
            continue

        # pressure (parenthetical)
        pp = try_pressure_parenthetical(i)
        if pp:
            j, item = pp
            add_pressure(item["value"], item["units"], item["text"], kind=item.get("kind", "pressure"))
            i = j
            continue

        # pressure (plain)
        p = try_pressure_at(i)
        if p:
            j, item = p
            add_pressure(item["value"], item["units"], item["text"], kind=item.get("kind", "pressure"))
            i = j
            continue

        # vessels
        if match_phrase(i, ["pressure", "vessel"]):
            add_vessel("pressure vessel", span_text(i, i + 2))
            i += 2
            continue

        if match_phrase(i, ["sealed", "tube"]):
            add_vessel("sealed tube", span_text(i, i + 2), qualifiers=["sealed"])
            i += 2
            continue

        if i + 2 < N and norm(raw(i)) in {"teflon", "ptfe"} and norm(raw(i + 1)) in {"lined", "lining"} and norm(raw(i + 2)) == "autoclave":
            add_vessel("autoclave", span_text(i, i + 3), qualifiers=["teflon-lined"])
            i += 3
            continue

        if norm(raw(i)) in VESSELS:
            add_vessel(VESSELS[norm(raw(i))], raw(i))
            i += 1
            continue

        # mixtures
        mix = try_mixture(i)
        if mix:
            j, item = mix
            # mixtures almost always imply atmosphere context; still ok to accept
            add_atmos(item["value"], item["text"], mode=item.get("mode", ""), composition=item.get("composition"))
            i = j
            continue

        # vacuum + reduced pressure phrases
        if norm(raw(i)) == "vacuum":
            add_atmos("vacuum", raw(i), mode="vacuum")
            i += 1
            continue
        if norm(raw(i)) == "vacuo" and i > 0 and norm(raw(i - 1)) == "in":
            add_atmos("vacuum", span_text(i - 1, i + 1), mode="vacuum")
            i += 1
            continue
        if norm(raw(i)) == "reduced" and i + 1 < N and norm(raw(i + 1)) == "pressure":
            add_atmos("vacuum", span_text(i, i + 2), mode="reduced_pressure")
            i += 2
            continue

        # trigger-based: "under nitrogen", "in air", "under 10 bar N2"
        if norm(raw(i)) in TRIGGERS:
            trig_i = i
            j = i + 1

            # optional mode right after trigger
            mode = ""
            if j < N and norm(raw(j)) in MODES:
                mode = norm(raw(j))
                j += 1

            # optional pressure after trigger
            pressure = None
            punits = None
            pp2 = try_pressure_parenthetical(j)
            if pp2:
                j2, item = pp2
                pressure, punits = item["value"], item["units"]
                add_pressure(item["value"], item["units"], item["text"])
                j = j2
            else:
                p2 = try_pressure_at(j)
                if p2:
                    j2, item = p2
                    pressure, punits = item["value"], item["units"]
                    add_pressure(item["value"], item["units"], item["text"])
                    j = j2

            # gas after
            if j < N:
                gas_val, consumed = canon_gas_at(j)
                if gas_val:
                    text = span_text(trig_i, j + consumed)
                    add_atmos(gas_val, text, mode=mode, pressure=pressure, pressure_units=punits)
                    i = j + consumed
                    continue

                # inert atmosphere
                if norm(raw(j)) == "inert":
                    end = j + 1
                    if end < N and norm(raw(end)) in {"atmosphere", "conditions", "environment"}:
                        end += 1
                    add_atmos("inert", span_text(trig_i, end), mode=mode)
                    i = end
                    continue

            # pressure-only condition (no gas)
            if pressure is not None and punits is not None:
                add_atmos("pressurized", span_text(trig_i, j), mode=(mode or "pressurized"),
                          pressure=pressure, pressure_units=punits)
                i = j
                continue

        # direct gas tokens — ONLY if context indicates atmosphere
        gas_val, consumed = canon_gas_at(i)
        if gas_val:
            # reject bare metal symbols like "Co" unless context indicates atmosphere
            # (gas_val might be "air"/"N2"/etc. from GAS_MAP)
            token_norm = norm(raw(i))
            token_raw = raw(i)

            # If token looks like a metal symbol casing (Co/Ni/Zn etc.), never accept as gas here
            # (you still get N2 etc because they aren't metal symbols)
            if token_raw in {"Co", "Ni", "Zn", "Fe", "Cu", "Mn", "Cr"}:
                i += 1
                continue

            # If the normalized token matches a metal symbol and the raw token is title-case (Co),
            # skip unless clearly in atmosphere context
            if token_norm in METAL_SYMBOLS and token_raw[:1].isupper() and token_raw[1:2].islower():
                if not is_atmosphere_context(i, i + consumed):
                    i += 1
                    continue

            if is_atmosphere_context(i, i + consumed):
                # optional mode before
                mode = ""
                if i > 0 and norm(raw(i - 1)) in MODES:
                    mode = norm(raw(i - 1))
                add_atmos(gas_val, span_text(i, i + consumed), mode=mode)
            i += consumed
            continue

        i += 1

    # ---------- de-dup ----------
    def dedup_list(items, key_fields):
        seen = set()
        out = []
        for it in items:
            k = tuple(it.get(f) for f in key_fields)
            if k in seen:
                continue
            seen.add(k)
            out.append(it)
        return out

    out_struct["atmosphere"] = dedup_list(out_struct["atmosphere"],
                                          ["value",
                                           "text",
                                           "mode",
                                           "composition",
                                           "pressure",
                                           "pressure_unit"]
                                          )
    out_struct["pressure"] = dedup_list(out_struct["pressure"],
                                        ["value", "unit", "text", "kind"])
    out_struct["vessel"] = dedup_list(out_struct["vessel"],
                                      ["value",
                                       "text"]
                                      )
    out_struct["humidity"] = dedup_list(out_struct["humidity"],
                                        ["value",
                                         "unit", "text"])

    return out_struct
