import streamlit as st
import datetime
import pytz
import swisseph as swe
import ephem
import warnings

warnings.filterwarnings('ignore')

# ================= 1. ALLOWED GMAIL IDs & PASSWORDS =================
ALLOWED_GMAIL_USERS = [
    ("spiritualteam43@gmail.com", "admin999"),
    ("4tradingviews@gmail.com", "pass123"),
    ("spiritualteam27@gmail.com", "gold786"),
    ("ravijaiswal1838@gmail.com", "xau2026")
]

# ================= 2. ASTROLOGICAL SETUP =================
LATITUDE, LONGITUDE = 19.0760, 72.8777 # Ahilyanagar / Mumbai
swe.set_sid_mode(swe.SIDM_KRISHNAMURTI)
ist = pytz.timezone('Asia/Kolkata')

PLANETS = {
    'Sun': swe.SUN, 'Moon': swe.MOON, 'Mars': swe.MARS,
    'Mercury': swe.MERCURY, 'Jupiter': swe.JUPITER,
    'Venus': swe.VENUS, 'Saturn': swe.SATURN
}

PLANET_HOUSES = {
    'Sun': [2, 10, 11], 'Moon': [5, 8, 12], 'Mars': [1, 6, 10],
    'Rahu': [3, 8, 12], 'Jupiter': [2, 5, 9, 11], 'Saturn': [4, 8, 12],
    'Mercury': [2, 3, 11], 'Ketu': [5, 8, 12], 'Venus': [2, 6, 11]
}
BULLISH_HOUSES = {2, 6, 10, 11}
BEARISH_HOUSES = {5, 8, 12}

HORA_ORDER = ['Saturn', 'Jupiter', 'Mars', 'Sun', 'Venus', 'Mercury', 'Moon']
WEEKDAY_LORDS = ['Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Sun']

def get_top_two_planets_live(jd):
    planet_degrees = []
    for p_name, p_id in PLANETS.items():
        pos, _ = swe.calc_ut(jd, p_id, swe.FLG_SWIEPH | swe.FLG_SIDEREAL)
        planet_degrees.append((p_name, pos[0] % 30.0))
    planet_degrees.sort(key=lambda x: x[1], reverse=True)
    return planet_degrees[0], planet_degrees[1]

def get_unequal_horas(date_obj):
    obs = ephem.Observer()
    obs.lat, obs.lon = str(LATITUDE), str(LONGITUDE)
    obs.date = date_obj.strftime('%Y/%m/%d 00:00:00')
    
    sun = ephem.Sun()
    sunrise = obs.next_rising(sun).datetime().replace(tzinfo=pytz.utc).astimezone(ist)
    sunset = obs.next_setting(sun).datetime().replace(tzinfo=pytz.utc).astimezone(ist)
    next_sunrise = obs.next_rising(sun, start=sunset).datetime().replace(tzinfo=pytz.utc).astimezone(ist)
    
    day_hora_len = (sunset - sunrise) / 12
    night_hora_len = (next_sunrise - sunset) / 12
    
    day_lord = WEEKDAY_LORDS[date_obj.weekday()]
    start_idx = HORA_ORDER.index(day_lord)
    
    horas = []
    curr = sunrise
    for hour in range(12):
        h_lord = HORA_ORDER[(start_idx + hour) % 7]
        horas.append({'lord': h_lord, 'start': curr, 'end': curr + day_hora_len})
        curr += day_hora_len
        
    for hour in range(12, 24):
        h_lord = HORA_ORDER[(start_idx + hour) % 7]
        horas.append({'lord': h_lord, 'start': curr, 'end': curr + night_hora_len})
        curr += night_hora_len
        
    return horas

def get_trend_prediction(sublord):
    houses = PLANET_HOUSES.get(sublord, [])
    bullish_count = len(set(houses).intersection(BULLISH_HOUSES))
    bearish_count = len(set(houses).intersection(BEARISH_HOUSES))
    if bullish_count > bearish_count: return "Bullish 🟢"
    elif bearish_count > bullish_count: return "Bearish 🔴"
    else: return "Sideways ⚪"

def generate_live_report(start_date_str, end_date_str):
    try:
        s_date = datetime.datetime.strptime(start_date_str.strip(), "%Y-%m-%d").date()
        e_date = datetime.datetime.strptime(end_date_str.strip(), "%Y-%m-%d").date()
    except Exception:
        return "⚠️ Kripya Date YYYY-MM-DD format me dalein (Jaise: 2026-10-26)"
    
    if s_date > e_date:
        return "⚠️ Start Date, End Date se pehle ki honi chahiye!"

    all_events = []
    pad_start = s_date - datetime.timedelta(days=2) 
    pad_end = e_date + datetime.timedelta(days=1)

    curr_d = pad_start
    while curr_d <= pad_end:
        day_horas = get_unequal_horas(curr_d)
        
        for hora in day_horas:
            h_start_utc = hora['start'].astimezone(pytz.utc)
            jd_hora = swe.julday(h_start_utc.year, h_start_utc.month, h_start_utc.day, h_start_utc.hour + h_start_utc.minute/60.0)
            
            king_info, vice_king_info = get_top_two_planets_live(jd_hora)
            k_planet, k_deg = king_info
            vk_planet, vk_deg = vice_king_info
            
            if hora['lord'] in [k_planet, vk_planet]:
                p_name = hora['lord']
                
                if p_name == k_planet:
                    p_deg = k_deg
                    rank_str = "NIFTY/SENSEX 👑"
                else:
                    p_deg = vk_deg
                    rank_str = "XAUUSD 🛡️"
                    
                prediction = get_trend_prediction(p_name)
                
                all_events.append({
                    'hora_start': hora['start'],
                    'planet': p_name,
                    'degree': p_deg,
                    'prediction': prediction,
                    'rank': rank_str
                })
                
        curr_d += datetime.timedelta(days=1)

    all_events.sort(key=lambda x: x['hora_start'])

    lines = []
    lines.append(f"=== 📅 SWING TIME FOR XAUUSD & NIFTY/SENSEX REPORT (00:00 AM to 23:59 PM) ===")
    lines.append(f"अवधि: {s_date.strftime('%d %b %Y')} से {e_date.strftime('%d %b %Y')}\n")

    curr_d = s_date
    while curr_d <= e_date:
        day_start = ist.localize(datetime.datetime(curr_d.year, curr_d.month, curr_d.day, 0, 0, 0))
        day_end = ist.localize(datetime.datetime(curr_d.year, curr_d.month, curr_d.day, 23, 59, 59))
        
        lines.append(f"=== Date: {curr_d.strftime('%a, %d %b %Y')} ===")
        daily_events = [e for e in all_events if day_start <= e['hora_start'] <= day_end]
        
        for event in daily_events:
            d_str = event['hora_start'].strftime('%a, %d %b %Y')
            h_start_str = event['hora_start'].strftime('%I:%M %p')
            
            line = f"Reversal Time : {d_str}, {h_start_str} IST | संकेत: {event['prediction']:<11} | {event['rank']} : {event['planet']} ({event['degree']:.2f}°)"
            lines.append(line)
            
        lines.append("-" * 115)
        curr_d += datetime.timedelta(days=1)

    return "\n".join(lines)

def main():
    st.set_page_config(page_title="Live Tracker", page_icon="⏱️", layout="wide")
    st.title("⏱️ True Live Tracker (NIFTY/SENSEX & XAUUSD)")

    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if not st.session_state['logged_in']:
        st.warning("🔒 Kripya apni Authorized Gmail ID aur Access Password dalein.")
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
                    st.session_state['username'] = clean_user
                    st.rerun()
                else:
                    st.error("Galat Username ya Password!")
        return

    # --- SECURITY CHECK BLOCKER (Optional) ---
    current_user = st.session_state.get('username', '')
    allowed_emails = [user[0].strip().lower() for user in ALLOWED_GMAIL_USERS]
    
    if current_user not in allowed_emails:
        st.error(f"🚫 Access Denied: '{current_user}' ko yeh page dekhne ki permission nahi hai.")
        if st.button("Logout", key="logout_blocked"):
            st.session_state['logged_in'] = False
            st.session_state['username'] = ""
            st.rerun()
        st.stop()
    # -----------------------------------------

    col1, col2 = st.columns([8, 1])
    with col2:
        if st.button("Logout"):
            st.session_state['logged_in'] = False
            st.session_state['username'] = ""
            st.rerun()
            
    with st.form("tracker_form"):
        col_start, col_end = st.columns(2)
        with col_start:
            start_date = st.text_input("Start Date (YYYY-MM-DD)", value="2026-10-19")
        with col_end:
            end_date = st.text_input("End Date (YYYY-MM-DD)", value="2026-10-23")
            
        generate = st.form_submit_button("Generate Swing Time Report")
        
    if generate:
        with st.spinner("Calculating Live Planet Degrees & Horas..."):
            result = generate_live_report(start_date, end_date)
            st.text_area("### Live Tracker Report", value=result, height=600)

if __name__ == "__main__":
    main()
