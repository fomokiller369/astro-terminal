import streamlit as st
import datetime
import pytz
import swisseph as swe
import pandas as pd
from astral import LocationInfo
from astral.sun import sun

# ================= 1. ALLOWED GMAIL IDs & PASSWORDS =================
ALLOWED_GMAIL_USERS = [
    ("spiritualteam43@gmail.com", "admin999"),
    ("4tradingviews@gmail.com", "pass123"),
    ("spiritualteam27@gmail.com", "gold786"),
    ("ravijaiswal1838@gmail.com", "xau2026")
]

# ================= 2. ASTROLOGY SETUP & CONSTANTS =================
TZ = pytz.timezone("Asia/Kolkata")
LAT, LON = 19.0760, 72.8777
city = LocationInfo("Mumbai", "India", "Asia/Kolkata", LAT, LON)
swe.set_sid_mode(swe.SIDM_LAHIRI)

CHALDEAN_ORDER = ["Sun", "Venus", "Mercury", "Moon", "Saturn", "Jupiter", "Mars"]
WEEKDAY_LORDS = {0: "Moon", 1: "Mars", 2: "Mercury", 3: "Jupiter", 4: "Venus", 5: "Saturn", 6: "Sun"}

FRIENDS = {
    "Sun": {"Sun", "Moon", "Mars", "Jupiter"}, "Moon": {"Moon", "Sun", "Mercury"}, 
    "Mars": {"Mars", "Sun", "Moon", "Jupiter"}, "Mercury": {"Mercury", "Sun", "Venus"}, 
    "Jupiter": {"Jupiter", "Sun", "Moon", "Mars"}, "Venus": {"Venus", "Mercury", "Saturn"}, 
    "Saturn": {"Saturn", "Mercury", "Venus"}
}
ENEMIES = {
    "Sun": {"Venus", "Saturn"}, "Moon": {"Saturn", "Venus"}, "Mars": {"Mercury", "Saturn"}, 
    "Mercury": {"Moon", "Mars"}, "Jupiter": {"Mercury", "Venus"}, "Venus": {"Sun", "Moon"}, 
    "Saturn": {"Sun", "Moon", "Mars"}
}

UCHHA_RASI = {"Sun": 0, "Moon": 1, "Mars": 9, "Mercury": 5, "Jupiter": 3, "Venus": 11, "Saturn": 6}
NEECHA_RASI = {"Sun": 6, "Moon": 7, "Mars": 3, "Mercury": 11, "Jupiter": 9, "Venus": 5, "Saturn": 0}
SWARASHI = {"Sun": {4}, "Moon": {3}, "Mars": {0, 7}, "Mercury": {2, 5}, "Jupiter": {8, 11}, "Venus": {1, 6}, "Saturn": {9, 10}}
PLANET_MAP = {"Sun": swe.SUN, "Moon": swe.MOON, "Mars": swe.MARS, "Mercury": swe.MERCURY, "Jupiter": swe.JUPITER, "Venus": swe.VENUS, "Saturn": swe.SATURN}

DAY_STRONG = ["Sun", "Jupiter", "Venus", "Mercury"]
NIGHT_STRONG = ["Moon", "Mars", "Saturn", "Mercury"]

# ================= 3. ASTROLOGY FUNCTIONS =================
def get_julian_day(dt_ist):
    dt_utc = dt_ist.astimezone(pytz.utc)
    hour_dec = dt_utc.hour + dt_utc.minute / 60.0 + dt_utc.second / 3600.0
    return swe.julday(dt_utc.year, dt_utc.month, dt_utc.day, hour_dec)

def get_planet_details(dt_ist, planet_name):
    jd = get_julian_day(dt_ist)
    flags = swe.FLG_SIDEREAL | swe.FLG_SWIEPH | swe.FLG_SPEED
    pid = PLANET_MAP[planet_name]
    res, _ = swe.calc_ut(jd, pid, flags)
    lon = res[0] % 360.0
    
    rasi_idx = int(lon // 30)
    is_vakri = res[3] < 0
    
    dignity = "Normal"
    if rasi_idx == NEECHA_RASI[planet_name]: dignity = "Neecha (Weak)"
    elif rasi_idx == UCHHA_RASI[planet_name]: dignity = "Uchha (Strong)"
    elif rasi_idx in SWARASHI[planet_name]: dignity = "Swarashi (Own)"
        
    return {
        "degree": round(lon % 30.0, 2),
        "is_vakri": is_vakri,
        "motion_str": "Vakri (R)" if is_vakri else "Margi (D)",
        "dignity": dignity,
        "rasi_idx": rasi_idx
    }

def calculate_score(planet_name, p_details, day_lord, is_day):
    score = 0
    if p_details["is_vakri"]: score -= 3
    if p_details["rasi_idx"] == NEECHA_RASI[planet_name]: score -= 3
    if p_details["rasi_idx"] == UCHHA_RASI[planet_name] or p_details["rasi_idx"] in SWARASHI[planet_name]: score += 3
    
    if planet_name != day_lord:
        if planet_name in ENEMIES[day_lord]: score -= 4
        elif planet_name in FRIENDS[day_lord]: score += 3
    else:
        score += 4  
        
    if is_day:
        if planet_name in DAY_STRONG: score += 3
        else: score -= 3
    else:
        if planet_name in NIGHT_STRONG: score += 3
        else: score -= 3
        
    direction = "🟢 BULLISH" if score < 0 else "🔴 BEARISH"
    return score, direction

def generate_power_report(start_dt, end_dt):
    delta = datetime.timedelta(days=1)
    current_dt = start_dt
    master_table = []
    
    while current_dt <= end_dt:
        if current_dt.weekday() >= 5:  # Skip Weekends
            current_dt += delta
            continue
            
        s = sun(city.observer, date=current_dt, tzinfo=TZ)
        sunrise = s["sunrise"]
        sunset = s["sunset"]
        
        next_day = current_dt + datetime.timedelta(days=1)
        s_next = sun(city.observer, date=next_day, tzinfo=TZ)
        next_sunrise = s_next["sunrise"]
        
        day_hora_sec = (sunset - sunrise).total_seconds() / 12.0
        night_hora_sec = (next_sunrise - sunset).total_seconds() / 12.0
        
        day_lord = WEEKDAY_LORDS[current_dt.weekday()]
        start_idx = CHALDEAN_ORDER.index(day_lord)
        
        formatted_date = current_dt.strftime("%d %b %Y (%a)")
        day_summary = f"{formatted_date} | Lord: {day_lord}"
        
        daily_horas = []
        max_impact = -1
        
        # Calculate ALL 24 Horas (12 Day + 12 Night)
        for h in range(24):
            is_day = h < 12
            hora_sec = day_hora_sec if is_day else night_hora_sec
            
            if is_day:
                h_start = sunrise + datetime.timedelta(seconds=(h % 12) * hora_sec)
                hora_label = f"Day Hora {(h % 12) + 1}"
            else:
                h_start = sunset + datetime.timedelta(seconds=(h % 12) * hora_sec)
                hora_label = f"Night Hora {(h % 12) + 1}"
                
            h_mid = h_start + datetime.timedelta(seconds=hora_sec / 2.0)
            h_planet = CHALDEAN_ORDER[(start_idx + h) % 7]
            
            p_details = get_planet_details(h_mid, h_planet)
            raw_score, direction = calculate_score(h_planet, p_details, day_lord, is_day)
            
            impact = abs(raw_score)
            if impact > max_impact:
                max_impact = impact
            
            if h_planet == day_lord: relation = "Self (Mitra)"
            elif h_planet in ENEMIES[day_lord]: relation = f"Shatru of {day_lord}"
            elif h_planet in FRIENDS[day_lord]: relation = f"Mitra of {day_lord}"
            else: relation = "Neutral"
                
            daily_horas.append({
                "hora_label": hora_label,
                "start": h_start,
                "planet": h_planet, "details": p_details,
                "relation": relation, "direction": direction,
                "impact": impact
            })
            
        for i, h_data in enumerate(daily_horas):
            is_powerful = "🔥 MOST POWERFUL" if h_data["impact"] == max_impact else ""
            dir_display = f"{h_data['direction']}  {is_powerful}"
            
            master_table.append({
                "Date & Lord": day_summary if i == 0 else "",
                "Hora Type & Time (IST)": f"{h_data['hora_label']}: {h_data['start'].strftime('%I:%M %p')}",
                "Planet & Degree": f"{h_data['planet']} ({h_data['details']['degree']}°)",
                "Motion & Dignity": f"{h_data['details']['motion_str']} | {h_data['details']['dignity']}",
                "Relation w/ Lord": h_data['relation'],
                "Direction & Power": dir_display
            })
            
        current_dt += delta

    if not master_table:
        return None, "⚠️ Di gayi dates me sirf chhuttiyan (Weekends) hain!"
        
    df = pd.DataFrame(master_table)
    return df, None

# ================= 4. STREAMLIT APP =================
def main():
    st.set_page_config(page_title="Power Astro", page_icon="⚡", layout="wide")
    st.title("⚡ XAUUSD Power Astrology (24-Hour)")

    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    # Login System
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

    # Security Blocker
    current_user = st.session_state.get('username', '')
    allowed_emails = [user[0].strip().lower() for user in ALLOWED_GMAIL_USERS]
    
    if current_user not in allowed_emails:
        st.error(f"🚫 Access Denied: '{current_user}' ko yeh page dekhne ki permission nahi hai.")
        if st.button("Logout", key="logout_blocked"):
            st.session_state['logged_in'] = False
            st.session_state['username'] = ""
            st.rerun()
        st.stop()

    # Main App UI
    col1, col2 = st.columns([8, 1])
    with col2:
        if st.button("Logout"):
            st.session_state['logged_in'] = False
            st.session_state['username'] = ""
            st.rerun()
            
    # Calculate Date Restrictions dynamically based on Current Date
    ist = pytz.timezone('Asia/Kolkata')
    today = datetime.datetime.now(ist).date()
    
    # 1. Past Limit: 1st of the Previous Month
    first_day_this_month = today.replace(day=1)
    last_day_prev_month = first_day_this_month - datetime.timedelta(days=1)
    min_date = last_day_prev_month.replace(day=1)
    
    # 2. Future Limit: Next Week Friday
    days_to_next_monday = 7 - today.weekday()
    next_monday = today + datetime.timedelta(days=days_to_next_monday)
    max_date = next_monday + datetime.timedelta(days=4)
            
    with st.form("power_form"):
        col_start, col_end = st.columns(2)
        with col_start:
            start_date = st.text_input("Start Date (YYYY-MM-DD)", value=today.strftime("%Y-%m-%d"))
        with col_end:
            end_date = st.text_input("End Date (YYYY-MM-DD)", value=(today + datetime.timedelta(days=1)).strftime("%Y-%m-%d"))
            
        generate = st.form_submit_button("Generate Power Report")
        
    if generate:
        try:
            s_date = datetime.datetime.strptime(start_date.strip(), "%Y-%m-%d").date()
            e_date = datetime.datetime.strptime(end_date.strip(), "%Y-%m-%d").date()
            
            # --- DATE RESTRICTION LOGIC ---
            if s_date < min_date:
                st.warning(f"⚠️ Warning: Aap sirf {min_date.strftime('%d %b %Y')} se Till Date ka hi data nikal sakte hain!")
            elif e_date > max_date:
                st.warning(f"⚠️ Warning: Aap future mein sirf {max_date.strftime('%d %b %Y')} (Next Week) tak ka hi data nikal sakte hain!")
            elif s_date > e_date:
                st.warning("⚠️ Start Date, End Date se pehle ki honi chahiye!")
            else:
                with st.spinner("Calculating Planetary Dignities and Powers (Day & Night)..."):
                    df, error = generate_power_report(s_date, e_date)
                    
                    if error:
                        st.error(error)
                    else:
                        st.markdown("### 📊 Power Astro Report (24-Hour)")
                        st.table(df)
                        
        except Exception:
            st.error("⚠️ Kripya Date YYYY-MM-DD format me dalein.")

if __name__ == "__main__":
    main()
