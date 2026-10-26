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

# ================= 2. ASTROLOGICAL CONSTANTS =================
DASHA_LORDS = ['Ketu', 'Venus', 'Sun', 'Moon', 'Mars', 'Rahu', 'Jupiter', 'Saturn', 'Mercury']
DASHA_YEARS = [7, 20, 6, 10, 7, 18, 16, 19, 17]

# STOCK (Equities) के लिए भाव सिग्निफिकेशन्स
PLANET_HOUSES = {
    'Sun': [2, 10, 11],
    'Moon': [5, 8, 12],
    'Mars': [1, 6, 10],
    'Rahu': [3, 8, 12],
    'Jupiter': [2, 5, 9, 11],
    'Saturn': [4, 8, 12],
    'Mercury': [2, 3, 11],
    'Ketu': [5, 8, 12],
    'Venus': [2, 6, 11]
}

# Stock Equity Rules: 2, 6, 10, 11 = Bullish | 5, 8, 12 = Bearish
BULLISH_HOUSES_STOCK = {2, 6, 10, 11}
BEARISH_HOUSES_STOCK = {5, 8, 12}

def get_stock_trend(sublord):
    houses = PLANET_HOUSES.get(sublord, [])
    bullish_count = len(set(houses).intersection(BULLISH_HOUSES_STOCK))
    bearish_count = len(set(houses).intersection(BEARISH_HOUSES_STOCK))
    
    if bullish_count > bearish_count:
        trend = "Bullish (UP) 🟢"
    elif bearish_count > bullish_count:
        trend = "Bearish (DOWN) 🔴"
    else:
        trend = "Neutral / Sideways ⚪"
        
    return houses, trend

def get_sublord(longitude):
    nakshatra_length = 13 + 1/3
    nakshatra_num = int(longitude / nakshatra_length)
    nakshatra_lord_index = nakshatra_num % 9
    
    rem_degrees = longitude - (nakshatra_num * nakshatra_length)
    
    current_span = 0
    for i in range(9):
        lord_index = (nakshatra_lord_index + i) % 9
        # Fixed syntax error here (added * operator)
        sub_lord_span = (DASHA_YEARS[lord_index] / 120.0) * nakshatra_length
        current_span += sub_lord_span
        
        if rem_degrees <= current_span:
            return DASHA_LORDS[lord_index]
    return None

def generate_report(start_date_str, end_date_str):
    try:
        s_date = datetime.datetime.strptime(start_date_str.strip(), "%Y-%m-%d").date()
        e_date = datetime.datetime.strptime(end_date_str.strip(), "%Y-%m-%d").date()
    except Exception:
        return "⚠️ Kripya Date YYYY-MM-DD format me dalein (Jaise: 2026-10-26)"
    
    if s_date > e_date:
        return "⚠️ Start Date, End Date se pehle ki honi chahiye!"

    swe.set_sid_mode(swe.SIDM_KRISHNAMURTI)
    ist = pytz.timezone('Asia/Kolkata')
    
    start_time = ist.localize(datetime.datetime(s_date.year, s_date.month, s_date.day, 9, 15, 0))
    end_time = ist.localize(datetime.datetime(e_date.year, e_date.month, e_date.day, 15, 30, 0))

    lines = []
    lines.append(f"=== NIFTY/SENSEX REVERSAL TIME TERMINAL REPORT (09:15 AM - 03:30 PM) ===")
    lines.append(f"अवधि: {start_time.strftime('%d %b %Y')} से {end_time.strftime('%d %b %Y')} (Per Day Trading Hours)\n")

    current_time = start_time
    previous_sublord = None

    while current_time <= end_time:
        time_only = current_time.time()
        # केवल 09:15 AM से 03:30 PM के बीच का फिल्टर
        is_market_hours = datetime.time(9, 15) <= time_only <= datetime.time(15, 30)

        utc_time = current_time.astimezone(pytz.utc)
        jd = swe.julday(utc_time.year, utc_time.month, utc_time.day, utc_time.hour + utc_time.minute / 60.0)
        
        moon_pos, _ = swe.calc_ut(jd, swe.MOON, swe.FLG_SWIEPH | swe.FLG_SIDEREAL)
        moon_longitude = moon_pos[0]
        
        current_sublord = get_sublord(moon_longitude)
        
        if current_sublord != previous_sublord and previous_sublord is not None:
            if is_market_hours:
                # --- TIME ADJUSTMENT LOGIC ---
                display_time = current_time
                if current_sublord == 'Venus':
                    display_time = current_time - datetime.timedelta(minutes=30)
                elif current_sublord == 'Ketu':
                    display_time = current_time + datetime.timedelta(minutes=15)
                    
                houses, trend = get_stock_trend(current_sublord)
                
                # Single line output layout
                line = (
                    f"रिवर्सल टाइम for NIFTY/SENSEX: {display_time.strftime('%d %b %Y, %I:%M %p')} | "
                    f"संकेत: {trend:<20} | "
                    f"सब-लॉर्ड: {current_sublord:<7} | "
                    f"भाव: {str(houses):<12} | "
                    f"(डिग्री: {moon_longitude:.2f})"
                )
                lines.append(line)
        
        previous_sublord = current_sublord
        current_time += datetime.timedelta(minutes=1)
        
        # Performance optimization: Jump to next day 09:15 AM if current time crosses 03:30 PM
        if current_time.time() > datetime.time(15, 30):
            current_time += datetime.timedelta(days=1)
            current_time = current_time.replace(hour=9, minute=15)
            previous_sublord = None # Reset for the new day
            
    return "\n".join(lines)

def main():
    st.set_page_config(page_title="NIFTY/SENSEX Terminal", page_icon="📈", layout="wide")
    st.title("📈 NIFTY & SENSEX Astro Reversal Terminal")

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
                    st.rerun()
                else:
                    st.error("Galat Username ya Password!")
        return

    col1, col2 = st.columns([8, 1])
    with col2:
        if st.button("Logout"):
            st.session_state['logged_in'] = False
            st.rerun()
            
    with st.form("astro_form"):
        col_start, col_end = st.columns(2)
        with col_start:
            start_date = st.text_input("Start Date (YYYY-MM-DD)", value="2026-10-26")
        with col_end:
            end_date = st.text_input("End Date (YYYY-MM-DD)", value="2026-10-31")
            
        generate = st.form_submit_button("Generate NIFTY/SENSEX Report")
        
    if generate:
        with st.spinner("Calculating Ephemeris Data..."):
            result = generate_report(start_date, end_date)
            st.text_area("### Reversal Report", value=result, height=500)

if __name__ == "__main__":
    main()
