import streamlit as st
import datetime
import pytz
import swisseph as swe

# ================= 1. ALLOWED GMAIL IDs & PASSWORDS LIST =================
ALLOWED_GMAIL_USERS = [
    ("spiritualteam43@gmail.com", "admin999"),
    ("4tradingviews@gmail.com", "pass123"),
    ("spiritualteam27@gmail.com", "gold786"),
    ("ravijaiswal1838@gmail.com", "xau2026")
]

# ================= 2. ASTROLOGICAL & SBC 9x9 CONSTANTS =================
DASHA_LORDS = ['Ketu', 'Venus', 'Sun', 'Moon', 'Mars', 'Rahu', 'Jupiter', 'Saturn', 'Mercury']
DASHA_YEARS = [7, 20, 6, 10, 7, 18, 16, 19, 17]
ALLOWED_SUBLORDS = {'Mercury', 'Mars', 'Jupiter', 'Sun'}

RASHI_LORDS = [
    'Mars', 'Venus', 'Mercury', 'Moon', 'Sun', 'Mercury',
    'Venus', 'Mars', 'Jupiter', 'Saturn', 'Saturn', 'Jupiter'
]

SBC_28_NAKSHATRAS = [
    ("Ashwini", 0.0, 13.333333, (0, 6)), ("Bharani", 13.333333, 26.666667, (0, 7)),
    ("Krittika", 26.666667, 40.0, (1, 8)), ("Rohini", 40.0, 53.333333, (2, 8)),
    ("Mrigashira", 53.333333, 66.666667, (3, 8)), ("Ardra", 66.666667, 80.0, (4, 8)),
    ("Punarvasu", 80.0, 93.333333, (5, 8)), ("Pushya", 93.333333, 106.666667, (6, 8)),
    ("Ashlesha", 106.666667, 120.0, (7, 8)), ("Magha", 120.0, 133.333333, (8, 7)),
    ("P.Phalguni", 133.333333, 146.666667, (8, 6)), ("U.Phalguni", 146.666667, 160.0, (8, 5)),
    ("Hasta", 160.0, 173.333333, (8, 4)), ("Chitra", 173.333333, 186.666667, (8, 3)),
    ("Swati", 186.666667, 200.0, (8, 2)), ("Vishakha", 200.0, 213.333333, (8, 1)),
    ("Anuradha", 213.333333, 226.666667, (7, 0)), ("Jyeshtha", 226.666667, 240.0, (6, 0)),
    ("Mula", 240.0, 253.333333, (5, 0)), ("P.Ashadha", 253.333333, 266.666667, (4, 0)),
    ("U.Ashadha", 266.666667, 276.666667, (3, 0)), ("Abhijit", 276.666667, 280.888889, (2, 0)),
    ("Shravana", 280.888889, 293.333333, (1, 0)), ("Dhanishtha", 293.333333, 306.666667, (0, 1)),
    ("Shatabhisha", 306.666667, 320.0, (0, 2)), ("P.Bhadrapada", 320.0, 333.333333, (0, 3)),
    ("U.Bhadrapada", 333.333333, 346.666667, (0, 4)), ("Revati", 346.666667, 360.0, (0, 5))
]

SWE_PLANETS = {
    'Sun': swe.SUN, 'Moon': swe.MOON, 'Mars': swe.MARS,
    'Mercury': swe.MERCURY, 'Jupiter': swe.JUPITER,
    'Venus': swe.VENUS, 'Saturn': swe.SATURN, 'Rahu': swe.TRUE_NODE
}

LATITUDE, LONGITUDE = 19.0760, 72.8777

def get_sbc_nakshatra(degree):
    deg = degree % 360.0
    for name, start, end, coord in SBC_28_NAKSHATRAS:
        if start <= deg < end:
            return name, coord
    return "Revati", (0, 5)

def get_tri_vedha_coords(coord):
    r, c = coord
    if c == 8: return [(r, 0), (0, 8 - r), (8, r)]
    if c == 0: return [(r, 8), (0, r), (8, 8 - r)]
    if r == 0: return [(8, c), (c, 0), (8 - c, 8)]
    if r == 8: return [(0, c), (8 - c, 0), (c, 8)]
    return []

def get_kp_lords(longitude):
    nak_len = 13 + 1/3
    deg = longitude % 360.0
    nak_num = int(deg / nak_len)
    star_lord_idx = nak_num % 9
    star_lord = DASHA_LORDS[star_lord_idx]
    rem_deg = deg - (nak_num * nak_len)
    current_span = 0.0
    for i in range(9):
        sub_idx = (star_lord_idx + i) % 9
        sub_span = (DASHA_YEARS[sub_idx] / 120.0) * nak_len
        if rem_deg <= current_span + sub_span:
            return star_lord, DASHA_LORDS[sub_idx], sub_span
        current_span += sub_span
    return star_lord, DASHA_LORDS[star_lord_idx], 0.5

def get_house_occupied(degree, cusps):
    deg = degree % 360.0
    for i in range(12):
        c_start, c_end = cusps[i], cusps[(i + 1) % 12]
        if c_start <= c_end:
            if c_start <= deg < c_end: return i + 1
        else:
            if deg >= c_start or deg < c_end: return i + 1
    return 1

def evaluate_signal(jd, dt_ist, moon_star, sublord, sub_span, last_trend, asset_mode):
    planet_info = {}
    for p_name, p_id in SWE_PLANETS.items():
        pos, _ = swe.calc_ut(jd, p_id, swe.FLG_SWIEPH | swe.FLG_SIDEREAL | swe.FLG_SPEED)
        deg, speed = pos[0] % 360.0, pos[3]
        is_retro = (speed < 0) if p_name not in {'Sun', 'Moon', 'Rahu'} else False
        nak_name, coord = get_sbc_nakshatra(deg)
        p_star, _, _ = get_kp_lords(deg)
        planet_info[p_name] = {
            'deg': deg, 'speed': speed, 'nak': nak_name, 'star_lord': p_star,
            'coord': coord, 'rashi': int(deg / 30.0),
            'vedha_targets': get_tri_vedha_coords(coord), 'retro': is_retro
        }
    ketu_deg = (planet_info['Rahu']['deg'] + 180.0) % 360.0
    ketu_nak, ketu_coord = get_sbc_nakshatra(ketu_deg)
    k_star, _, _ = get_kp_lords(ketu_deg)
    planet_info['Ketu'] = {
        'deg': ketu_deg, 'speed': planet_info['Rahu']['speed'], 'nak': ketu_nak,
        'star_lord': k_star, 'coord': ketu_coord, 'rashi': int(ketu_deg / 30.0),
        'vedha_targets': get_tri_vedha_coords(ketu_coord), 'retro': False
    }

    cusps_raw, _ = swe.houses_ex(jd, LATITUDE, LONGITUDE, b'P', swe.FLG_SIDEREAL)
    cusps = list(cusps_raw[1:13]) if len(cusps_raw) == 13 else list(cusps_raw[0:12])

    owned_houses = {p: [] for p in DASHA_LORDS}
    for h_idx, cusp_deg in enumerate(cusps):
        owned_houses[RASHI_LORDS[int((cusp_deg % 360.0) / 30.0)]].append(h_idx + 1)

    occupied_house = {p: get_house_occupied(info['deg'], cusps) for p, info in planet_info.items()}
    sub_star = planet_info[sublord]['star_lord']
    kp_houses = []
    for h in [occupied_house[sub_star], occupied_house[sublord]] + owned_houses[sub_star] + owned_houses[sublord]:
        if h not in kp_houses: kp_houses.append(h)

    sub_coord = planet_info[sublord]['coord']
    vedha_list, raw_vedha_names = [], set()
    for p_name, info in planet_info.items():
        if p_name != sublord and ((sub_coord in info['vedha_targets']) or (sub_coord == info['coord'])):
            vedha_list.append(f"{p_name}(R)" if info['retro'] else p_name)
            raw_vedha_names.add(p_name)

    core_bull_h = set(kp_houses).intersection({5, 8, 12})
    core_bear_h = set(kp_houses).intersection({2, 3, 6, 10})
    support_bull_h = set(kp_houses).intersection({1, 9})

    bull_score = len(core_bull_h) * 1.65 + (len(support_bull_h) * 0.55 if len(core_bull_h) > 0 else 0.0)
    bear_score = len(core_bear_h) * 1.35 + (2.20 if len(core_bull_h) == 0 else 0.0)

    has_malefic_vedha = len(raw_vedha_names.intersection({'Sun', 'Mars', 'Saturn', 'Rahu', 'Ketu'})) > 0
    if 'Saturn' in raw_vedha_names: bear_score += 1.60
    if len(raw_vedha_names.intersection({'Rahu', 'Ketu'})) > 0: bear_score += 1.10
    if len(raw_vedha_names.intersection({'Sun', 'Mars'})) > 0: bear_score += 1.25
    if len(raw_vedha_names.intersection({'Jupiter', 'Venus', 'Mercury'})) > 0: bull_score += 1.30

    moon_nak, moon_rashi = planet_info['Moon']['nak'], planet_info['Moon']['rashi']

    if sublord == 'Sun':
        if has_malefic_vedha or len(core_bull_h) == 0 or planet_info['Sun']['rashi'] in {5, 6}: bear_score += 2.10
        else: bull_score += 2.00
    elif sublord == 'Mars':
        if 'Sun' in raw_vedha_names or 'Saturn' in raw_vedha_names or len(core_bear_h) >= 2: bear_score += 2.40
        elif last_trend == "Bullish (UP) 🟢": bear_score += 2.00
        elif len(core_bull_h) >= 1 or moon_rashi == 7 or moon_nak in {"Anuradha", "Jyeshtha", "Mula", "Magha", "P.Phalguni", "U.Phalguni"}: bull_score += 2.50
        else: bear_score += 1.80
    elif sublord == 'Jupiter':
        if len(core_bull_h) == 0 and has_malefic_vedha and moon_star in {'Mars', 'Rahu'}: bear_score += 2.30
        elif moon_nak in {"Magha", "P.Phalguni"} and last_trend == "Bullish (UP) 🟢": bear_score += 2.10
        else: bull_score += 2.80
    elif sublord == 'Mercury':
        if moon_nak == "Swati": bear_score += 2.40
        elif len(core_bull_h) >= 2: bull_score += 2.80
        elif last_trend == "Bullish (UP) 🟢" and len(core_bull_h) <= 1: bear_score += 2.60
        else: bull_score += 2.70

    if asset_mode == 'STOCK':
        bull_score, bear_score = bear_score, bull_score

    trend = "Bullish (UP) 🟢" if bull_score >= bear_score else "Bearish (DOWN) 🔴"
    moon_speed = planet_info['Moon']['speed']
    wave_mins = int(round((sub_span / (moon_speed / 24.0)) * 60.0))
    wave_end = dt_ist + datetime.timedelta(minutes=wave_mins)

    base_map = {'Sun': 150, 'Mars': 210, 'Jupiter': 270, 'Mercury': 250}
    avg_max = base_map.get(sublord, 190)
    p_low, p_high = max(100, int(round((avg_max * 0.65) / 10.0) * 10)), max(160, int(round((avg_max * 1.15) / 10.0) * 10))
    pips_str = f"{p_low}-{p_high} Pips (\${p_low//10}-\${p_high//10}) | SL:50pips (Flip Tgt:150pips)"
    vedha_str = ", ".join(vedha_list) if vedha_list else "Clean"
    return moon_nak, kp_houses, vedha_str, trend, wave_end, pips_str

def run_astro_app(start_date_str, end_date_str, asset_mode):
    try:
        s_date = datetime.datetime.strptime(start_date_str.strip(), "%Y-%m-%d").date()
        e_date = datetime.datetime.strptime(end_date_str.strip(), "%Y-%m-%d").date()
    except Exception:
        return "⚠️ Kripya Date YYYY-MM-DD format me dalein (Jaise: 2026-10-26)"
    
    if s_date > e_date:
        return "⚠️ Start Date, End Date se pehle ki honi chahiye!"
    if (e_date - s_date).days > 15:
        return "⚠️ Ek baar me maximum 15 din ki range chunein taaki result turant aaye."

    swe.set_sid_mode(swe.SIDM_KRISHNAMURTI)
    ist = pytz.timezone('Asia/Kolkata')
    if asset_mode == 'XAUUSD':
        curr_t = ist.localize(datetime.datetime(s_date.year, s_date.month, s_date.day, 3, 30, 0))
        end_t = ist.localize(datetime.datetime(e_date.year, e_date.month, e_date.day, 2, 30, 0))
    else:
        curr_t = ist.localize(datetime.datetime(s_date.year, s_date.month, s_date.day, 9, 15, 0))
        end_t = ist.localize(datetime.datetime(e_date.year, e_date.month, e_date.day, 15, 30, 0))

    lines = [f"=== {asset_mode} ASTRO REVERSAL REPORT ({s_date.strftime('%d %b %Y')} to {e_date.strftime('%d %b %Y')}) ===\n"]
    prev_sub, last_tr = None, None
    
    while curr_t <= end_t:
        t_only = curr_t.time()
        is_stock_hr = datetime.time(9, 15) <= t_only <= datetime.time(15, 30)
        utc_t = curr_t.astimezone(pytz.utc)
        jd = swe.julday(utc_t.year, utc_t.month, utc_t.day, utc_t.hour + utc_t.minute / 60.0)
        m_pos, _ = swe.calc_ut(jd, swe.MOON, swe.FLG_SWIEPH | swe.FLG_SIDEREAL)
        star_l, curr_sub, sub_sp = get_kp_lords(m_pos[0])

        if curr_sub != prev_sub and prev_sub is not None and curr_sub in ALLOWED_SUBLORDS:
            if asset_mode == 'XAUUSD' or is_stock_hr:
                m_nak, kp_h, v_str, tr, w_end, p_str = evaluate_signal(jd, curr_t, star_l, curr_sub, sub_sp, last_tr, asset_mode)
                last_tr = tr
                lines.append(
                    f"रिवर्सल टाइम: **{curr_t.strftime('%d %b %Y, %I:%M %p')}** (वेव अंत: {w_end.strftime('%I:%M %p')}) |  \n"
                    f"संकेत: {tr} |  \n"
                    f"टारगेट: {p_str} |  \n"
                    f"सब-लॉर्ड: {curr_sub}\n\n"
                )
        prev_sub = curr_sub
        curr_t += datetime.timedelta(minutes=1)
        
    return "\n".join(lines)

# Streamlit App Execution
def main():
    st.set_page_config(page_title="Astro Terminal", page_icon="🔮")
    st.title("🔮 XAUUSD Astro Reversal Terminal")

    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    # Login Screen
    if not st.session_state['logged_in']:
        st.warning("🔒 FOMOKILLER Astro Terminal: Kripya apni Authorized Gmail ID aur Access Password dalein.")
        with st.form("login_form"):
            username = st.text_input("Username (Gmail ID)")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login")
            
            if submitted:
                clean_user = username.strip().lower()
                clean_pass = password.strip()
                valid = False
                for allowed_email, allowed_pin in ALLOWED_GMAIL_USERS:
                    if clean_user == allowed_email.strip().lower() and clean_pass == allowed_pin:
                        valid = True
                        break
                if valid:
                    st.session_state['logged_in'] = True
                    st.rerun()
                else:
                    st.error("Galat Username ya Password!")
        return

    # Main App Screen
    col1, col2 = st.columns([4, 1])
    with col2:
        if st.button("Logout"):
            st.session_state['logged_in'] = False
            st.rerun()
            
    with st.form("astro_form"):
        start_date = st.text_input("Start Date (YYYY-MM-DD)", value="2026-10-26")
        end_date = st.text_input("End Date (YYYY-MM-DD)", value="2026-10-31")
        market = "XAUUSD"
        generate = st.form_submit_button("Generate XAUUSD Report")
        
    if generate:
        with st.spinner("Calculating Ephemeris Data..."):
            result = run_astro_app(start_date, end_date, market)
            st.markdown("### Reversal Time & Direction Report")
            with st.container(height=450, border=True):
                st.markdown(result)

if __name__ == "__main__":
    main()
