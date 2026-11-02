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
    ("annjaldubai2025@gmail.com", "gold786"),
    ("ravijaiswal1838@gmail.com", "xau2026"),
    ("sanmanjhi84@gmail.com", "ash9283f"),
    ("rajkumarraobgs@gmail.com", "rk7392rd"),
    ("Adityabane.trade17@gmail.com", "adi8261t"),
    ("vinod.gb88@gmail.com", "vin5382gb"),
    ("shobitha.naidu@gmail.com", "shob2749n"),
    ("rinanishad243@gmail.com", "rina8193r"),
    ("ameshram318@gmail.com", "am7382sh"),
    ("sarthakwaghmode5558@gmail.com", "sarthak558"),
    ("pkmahalik1982@gmail.com", "pk8273mh"),
    ("milindwankhede7@gmail.com", "milind773"),
    ("ramjitnaga5f@gmail.com", "ram5392ng"),
    ("dhananjaykatalkar@gmail.com", "dhan9182dk"),
    ("manoj12693@gmail.com", "manoj693m"),
    ("goursundar.jena02@gmail.com", "gour0283gs"),
    ("suryabhannandagawali49@gmail.com", "surya4982sb"),
    ("sanjaymaraviofficial@gmail.com", "sanjay827m"),
    ("suresh.ronak39@gmail.com", "suresh39sr"),
    ("maravis985@gmail.com", "maravi985m"),
    ("onkar.lov@gmail.com", "onkar5382ov"),
    ("furkantabrez786@gmail.com", "furkan786ft"),
    ("akanksha.hp20@gmail.com", "akanksha20a"),
    ("sangramtawar@gmail.com", "sangram827st"),
    ("manvya24@gmail.com", "manvya24m"),
    ("bg786323@gmail.com", "bg786323b"),
    ("anantkumbhakarn6@gmail.com", "anant6738ak"),
    ("pankajchaudhari666@gmail.com", "pankaj666pc"),
    ("dilipkasera753@gmail.com", "dilip753dk"),
    ("viratdrkr@gmail.com", "virat8273vk"),
    ("hausiladubey07@gmail.com", "hausila07hd"),
    ("raajeshsingparihar@gmail.com", "raajesh827rp"),
    ("feelalone79@gmail.com", "feel79fa"),
    ("drgmmct.1@gmail.com", "drgmmct1dt"),
    ("jayujadhav99@gmail.com", "jaju999jj"),
    ("8817vikas.k@gmail.com", "vikas8817vk"),
    ("niraj.gautam1210@gmail.com", "niraj1210ng"),
    ("pranay30waghmare@gmail.com", "pranay30pw"),
    ("patelravi071982@gmail.com", "patel1982pr"),
    ("dhiraj.sai567@gmail.com", "dhiraj567ds"),
    ("neerajkumarranjan1@gmail.com", "neeraj1nr"),
    ("nagarajuunk@gmail.com", "nagaraju538nu"),
    ("rajendradewangan140@gmail.com", "rajendra140rd"),
    ("paharu393@gmail.com", "paharu393p"),
    ("lekhrajraut124@gmail.com", "lekhraj124lr"),
    ("munakumar1979@gmail.com", "muna1979mk"),
    ("kvchavan555@gmail.com", "chavan555kc"),
    ("havalvishal@gmail.com", "haval8273hv"),
    ("Sagardahiya7415@gmail.com", "sagar7415sd"),
    ("Allonewin155@gmail.com", "allone155aw"),
    ("niteshkumar12g@gmail.com", "nitesh12gn"),
    ("kpandit0289@gmail.com", "pandit0289kp"),
    ("Ks593615@gmail.com", "ks8274ks"),
    ("satyabanparida8@gmail.com", "saty3847da"),
    ("tarendrab109@gmail.com", "tare9274ab"),
    ("jasvindersingh56584@gmail.com", "jasv2947gh"),
    ("shubhamarmy155@gmail.com", "shub1038my"),
    ("rasmitachakrabarty30604@gmail.com", "rasm8372ty"),
    ("mit2025gold@gmail.com", "mitg7382ld"),
    ("rajeshjangle75180@gmail.com", "raje5938le"),
    ("dpkant05@gmail.com", "dpka3829nt"),
    ("sainimayur43@gmail.com", "sain3849ur"),
    ("pirsabmulla.pm@gmail.com", "pirs8273pm"),
    ("manishdhabekar2007@gmail.com", "mani9382ar"),
    ("dharmesandeep@gmail.com", "dhar1928ep"),
    ("madhumeshram10@gmail.com", "madh9283am"),
    ("uzmapaintco@gmail.com", "uzma3847co"),
    ("kishorrdas23@gmail.com", "kish8273as"),
    ("Binaryfrx@gmail.com", "bina9283rx"),
    ("Mujeshlove@gmail.com", "muje3829ve"),
    ("santoshlohar1859@gmail.com", "sant9382ar"),
    ("Swapnilgaikwad463@gmail.com", "swap3928ad"),
    ("pratiktrader999@gmail.com", "prat9283er"),
    ("annjaldubai2025@gmail.com", "annj2938ai"),
    ("chaitansinghsidar@gmail.com", "chai9382ar"),
    ("jiteshkapuriya7012@gmail.com", "jite9283ya"),
    ("anishsahu210@gmail.com", "anis3847hu"),
    ("patankarrp@gmail.com", "pata9382rp"),
    ("keshabkumarpatra744@gmail.com", "kesh2938ra"),
    ("ashishyadav201299@gmail.com", "ashi9283av"),
    ("bhupendra9885@gmail.com", "bhup3928ra"),
    ("pragyastarslok1@gmail.com", "prag9382ok"),
    ("sahmed083@gmail.com", "sahm9283ed"),
    ("hmmuniya@gmail.com", "hmmu2938ya"),
    ("parmar1010@gmail.com", "parm9382ar"),
    ("skyadav3245@gmail.com", "skya3847av"),
    ("munakumar1979@gmail.com", "muna9283ar"),
    ("kumariranikumari49@gmail.com", "kuma9382ri"),
    ("prabhatn862@gmail.com", "prab3928tn"),
    ("rahideshitrader100cr@gmail.com", "rahi9283cr"),
    ("havalvishal@gmail.com", "hava2938al"),
    ("vijetamanoj37@gmail.com", "vije9382oj"),
    ("niteshkumar12g@gmail.com", "nite3847rg"),
    ("dilipchavan535@gmail.com", "dili9283an"),
    ("aniljadhav665020@gmail.com", "anil9382av"),
    ("binyantopno90555@gmail.com", "biny3928no"),
    ("diptiranjanguru@gmail.com", "dipt9283ru"),
    ("Gauravpurbiya@gmail.com", "gaur2938ya"),
    ("gaytriindurkar1980@gmail.com", "gayt9382ar"),
    ("uditbisen96@gmail.com", "udit3847en"),
    ("ranithakur86022@gmail.com", "rani9283ur"),
    ("priyanka30582@gmail.com", "priy9382ka"),
    ("moin281268@gmail.com", "moin3928in"),
    ("poonamsinghdayal@gmail.com", "poon9283al"),
    ("shaileshg740@gmail.com", "shai2938hg"),
    ("adityagadhave2@gmail.com", "adit9382ve"),
    ("ganeshkalke78@gmail.com", "gane3847ke"),
    ("shivnathpatankar1@gmail.com", "shiv9283ar"),
    ("vickymotharkar10x@gmail.com", "vick9382rx"),
    ("viiishald24@gmail.com", "viii3928ld"),
    ("manjeetmalik446@gmail.com", "manj9283ik"),
    ("rajivranjanmuz77@gmail.com", "raji2938uz"),
    ("walejayashika@gmail.com", "wale9382ka"),
    ("subhsandesh36@gmail.com", "subh3847sh"),
    ("jetaramparihar25@gmail.com", "jeta9283ar"),
    ("anjalisarkarslg100@gmail.com", "anja9382lg"),
    ("kushalkumarub@gmail.com", "kush3928ub"),
    ("dayavlog4467@gmail.com", "daya9283og"),
    ("harshsanchetiix@gmail.com", "hars2938ix"),
    ("kchand9@gmail.com", "kcha9382nd"),
    ("rahulkumar8434706641@gmail.com", "rahu3847ar"),
    ("rahulpujari7686@gmail.com", "rahu9283ri"),
    ("ravindragirhepunje1978@gmail.com", "ravi9382je"),
    ("swapnanagilwar@gmail.com", "swap3928ar"),
    ("deepakkumarthakur1313@gmail.com", "deep9283ur"),
    ("royaltrader3690@gmail.com", "roya9382er")
]

# ================= 2. ASTROLOGY SETUP & CONSTANTS =================
TZ = pytz.timezone("Asia/Kolkata")
LAT, LON = 19.0760, 72.8777
city = LocationInfo("Mumbai", "India", "Asia/Kolkata", LAT, LON)
swe.set_sid_mode(swe.SIDM_LAHIRI)

CHALDEAN_ORDER = ["Sun", "Venus", "Mercury", "Moon", "Saturn", "Jupiter", "Mars"]
WEEKDAY_LORDS = {0: "Moon", 1: "Mars", 2: "Mercury", 3: "Jupiter", 4: "Venus", 5: "Saturn", 6: "Sun"}
PLANET_MAP = {"Sun": swe.SUN, "Moon": swe.MOON, "Mars": swe.MARS, "Mercury": swe.MERCURY, "Jupiter": swe.JUPITER, "Venus": swe.VENUS, "Saturn": swe.SATURN}

CUSTOM_ENEMIES = {
    "Sun": "Moon",
    "Moon": "Sun",
    "Mercury": "Venus",
    "Venus": "Mercury",
    "Mars": "Saturn",
    "Saturn": "Mars",
    "Jupiter": "Jupiter"
}

def get_julian_day(dt_ist):
    dt_utc = dt_ist.astimezone(pytz.utc)
    hour_dec = dt_utc.hour + dt_utc.minute / 60.0 + dt_utc.second / 3600.0
    return swe.julday(dt_utc.year, dt_utc.month, dt_utc.day, hour_dec)

def get_2nd_rank_planet(dt_ist):
    jd = get_julian_day(dt_ist)
    flags = swe.FLG_SIDEREAL | swe.FLG_SWIEPH
    
    planet_list = []
    for pname, pid in PLANET_MAP.items():
        res, _ = swe.calc_ut(jd, pid, flags)
        deg_in_rasi = round(res[0] % 30.0, 2)
        planet_list.append({"planet": pname, "degree": deg_in_rasi})
        
    unique_degrees = sorted(list(set([p["degree"] for p in planet_list])), reverse=True)
    target_degree = unique_degrees[1] if len(unique_degrees) > 1 else unique_degrees[0]
    
    second_rank_planets = [p["planet"] for p in planet_list if p["degree"] == target_degree]
    return second_rank_planets[0], target_degree

def get_horas_info(current_dt, target_planet):
    s = sun(city.observer, date=current_dt, tzinfo=TZ)
    sunrise, sunset = s["sunrise"], s["sunset"]
    
    next_day = current_dt + datetime.timedelta(days=1)
    next_sunrise = sun(city.observer, date=next_day, tzinfo=TZ)["sunrise"]
    
    day_hora_sec = (sunset - sunrise).total_seconds() / 12.0
    night_hora_sec = (next_sunrise - sunset).total_seconds() / 12.0
    
    day_lord = WEEKDAY_LORDS[current_dt.weekday()]
    start_idx = CHALDEAN_ORDER.index(day_lord)
    
    primary_enemy = CUSTOM_ENEMIES.get(target_planet, target_planet)
    fallback_enemy = CUSTOM_ENEMIES.get(day_lord, day_lord)  
    
    target_1st_idx = -1
    target_1st_time = None
    primary_enemy_last_idx = -1
    primary_enemy_last_time = None
    fallback_enemy_last_idx = -1
    fallback_enemy_last_time = None
    
    # 1. DAY HORAS SCAN (12 Hours)
    for h in range(12):
        h_start = sunrise + datetime.timedelta(seconds=h * day_hora_sec)
        h_planet = CHALDEAN_ORDER[(start_idx + h) % 7]
        time_str = f"{h_start.strftime('%I:%M %p')}"
        
        if h_planet == target_planet and target_1st_idx == -1:
            target_1st_idx = h
            target_1st_time = time_str
            
        if h_planet == primary_enemy:
            primary_enemy_last_idx = h
            primary_enemy_last_time = time_str
            
        if h_planet == fallback_enemy:
            fallback_enemy_last_idx = h
            fallback_enemy_last_time = time_str

    is_special = False
    
    # ==========================================
    # SPECIAL RULE: TUESDAY & JUPITER
    # ==========================================
    if current_dt.weekday() == 1 and target_planet == "Jupiter":
        jupiter_1st_night_time = None
        for h in range(12):
            h_start = sunset + datetime.timedelta(seconds=h * night_hora_sec)
            h_planet = CHALDEAN_ORDER[(start_idx + 12 + h) % 7]
            if h_planet == "Jupiter" and jupiter_1st_night_time is None:
                # Sirf simple time nikalenge, Bold karne ka logic aage hai
                jupiter_1st_night_time = f"{h_start.strftime('%I:%M %p')}"
                break
        
        is_special = True
        return target_1st_time, jupiter_1st_night_time, is_special

    # ==========================================
    # NORMAL LOGIC (With Fallback)
    # ==========================================
    if primary_enemy_last_idx > target_1st_idx:
        final_enemy_time = primary_enemy_last_time
    else:
        final_enemy_time = fallback_enemy_last_time
                
    return target_1st_time, final_enemy_time, is_special

def run_smart_time_report(start_dt, end_dt):
    delta = datetime.timedelta(days=1)
    current_dt = start_dt
    master_table = []
    
    while current_dt <= end_dt:
        if current_dt.weekday() >= 5: # Skip Sat/Sun
            current_dt += delta
            continue
            
        calc_time_ist = TZ.localize(datetime.datetime.combine(current_dt, datetime.time(3, 30, 0)))
        target_planet, p_deg = get_2nd_rank_planet(calc_time_ist)
        
        target_1st_day, enemy_last_time, is_special = get_horas_info(current_dt, target_planet)
        
        date_str = current_dt.strftime("%d %b %Y (%a)")
        t1_str = target_1st_day if target_1st_day else "-"
        t2_str = enemy_last_time if enemy_last_time else "-"
        
        # Yahan HTML <b> tag lagaya gaya hai bold karne ke liye
        if is_special:
            date_str = f"<b>{date_str}</b>"
            t1_str = f"<b>{t1_str}</b>"
            t2_str = f"<b>{t2_str}</b>"
        
        master_table.append({
            "Date & Day": date_str,
            "TIME-1": t1_str,
            "TIME-2": t2_str
        })
        current_dt += delta

    if not master_table:
        return None, "⚠️ Di gayi dates me sirf chhuttiyan (Weekends) hain!"
        
    df = pd.DataFrame(master_table)
    return df, None

def main():
    st.set_page_config(page_title="Smart Time", page_icon="🚀", layout="wide")
    st.title("🚀 XAUUSD SMART TIMING: TIME-1 & TIME-2")

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

    current_user = st.session_state.get('username', '')
    allowed_emails = [user[0].strip().lower() for user in ALLOWED_GMAIL_USERS]
    
    if current_user not in allowed_emails:
        st.error(f"🚫 Access Denied: '{current_user}' ko yeh page dekhne ki permission nahi hai.")
        if st.button("Logout", key="logout_blocked"):
            st.session_state['logged_in'] = False
            st.session_state['username'] = ""
            st.rerun()
        st.stop()

    col1, col2 = st.columns([8, 1])
    with col2:
        if st.button("Logout"):
            st.session_state['logged_in'] = False
            st.session_state['username'] = ""
            st.rerun()
            
    today = datetime.datetime.now(TZ).date()
    
    first_day_this_month = today.replace(day=1)
    last_day_prev_month = first_day_this_month - datetime.timedelta(days=1)
    min_date = last_day_prev_month.replace(day=1)
    
    days_to_next_monday = 7 - today.weekday()
    next_monday = today + datetime.timedelta(days=days_to_next_monday)
    max_date = next_monday + datetime.timedelta(days=4)
            
    with st.form("smart_form"):
        col_start, col_end = st.columns(2)
        with col_start:
            start_date = st.text_input("Start Date (YYYY-MM-DD)", value=today.strftime("%Y-%m-%d"))
        with col_end:
            end_date = st.text_input("End Date (YYYY-MM-DD)", value=(today + datetime.timedelta(days=1)).strftime("%Y-%m-%d"))
            
        generate = st.form_submit_button("Generate Smart Time Report")
        
    if generate:
        try:
            s_date = datetime.datetime.strptime(start_date.strip(), "%Y-%m-%d").date()
            e_date = datetime.datetime.strptime(end_date.strip(), "%Y-%m-%d").date()
            
            if s_date < min_date:
                st.warning(f"⚠️ Warning: Aap sirf {min_date.strftime('%d %b %Y')} se Till Date ka hi data nikal sakte hain!")
            elif e_date > max_date:
                st.warning(f"⚠️ Warning: Aap future mein sirf {max_date.strftime('%d %b %Y')} (Next Week) tak ka hi data nikal sakte hain!")
            elif s_date > e_date:
                st.warning("⚠️ Start Date, End Date se pehle ki honi chahiye!")
            else:
                with st.spinner("Calculating Smart Times..."):
                    df, error = run_smart_time_report(s_date, e_date)
                    
                    if error:
                        st.error(error)
                    else:
                        st.markdown("### 📊 XAUUSD Smart Swing Timing Report")
                        
                        # --- Custom CSS for Clean, Compact & Centered Table ---
                        st.markdown("""
                        <style>
                        .smart-table {
                            width: 100% !important;
                            max-width: 800px !important;
                            border-collapse: collapse;
                            margin: 15px 0;
                        }
                        .smart-table th, .smart-table td {
                            padding: 12px 30px !important;
                            text-align: center !important;
                            border-bottom: 1px solid rgba(128, 128, 128, 0.2);
                        }
                        .smart-table th {
                            font-size: 16px;
                            color: #888;
                        }
                        </style>
                        """, unsafe_allow_html=True)
                        
                        # Render DataFrame using HTML (No CSV Button, Parses Bold <b> tags)
                        html_table = df.to_html(escape=False, index=False, classes="smart-table")
                        st.markdown(html_table, unsafe_allow_html=True)
                        
        except Exception:
            st.error("⚠️ Kripya Date YYYY-MM-DD format me dalein.")

if __name__ == "__main__":
    main()
