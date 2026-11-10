"""
श्री सद्गुरू यज्ञेश्वर शिवाचार्य (वेडे महाराज) मठ, परंडा
अधिकृत संकेतस्थळ - Streamlit (एकच फाईल)

चालवण्यासाठी:
    pip install -U streamlit
    streamlit run app.py
"""

import hmac
import html
import json
import os
import uuid
from datetime import date, datetime, time
from pathlib import Path

import streamlit as st

try:
    from zoneinfo import ZoneInfo
    IST = ZoneInfo("Asia/Kolkata")
except Exception:  # pragma: no cover
    IST = None

# ------------------------------------------------------------------
# कॉन्फिगरेशन
# ------------------------------------------------------------------
APP_DIR = Path(__file__).parent
UPLOAD_DIR = APP_DIR / "uploads"
DATA_FILE = APP_DIR / "data.json"
UPLOAD_DIR.mkdir(exist_ok=True)

# प्रशासक पासवर्ड फक्त environment variable मधून वाचला जातो (कोडमध्ये पासवर्ड नाही)
# उदा. export MATH_ADMIN_PASSWORD="your-password"
ADMIN_PASSWORD = os.environ.get("MATH_ADMIN_PASSWORD", "")

MATH_NAME = "श्री. सद्गुरू यज्ञेश्वर शिवाचार्य (वेडे महाराज) मठ"
MATH_PLACE = "परंडा, महाराष्ट्र"
CONTACT_NAME = "यश स्वामी (पकाले)"
CONTACT_EMAIL = "yashpakale56@gmail.com"
CONTACT_PHONE = "8208027577"
MAHARAJ_NAME = "श्री. ष. ब्र. १०८ राचलिंग शिवाचार्य परंडकर महाराज"
MAHARAJ_PHONES = ("9405428974", "9309170918")

PAGES = [
    "🏠 मुख्यपृष्ठ",
    "🛕 आमच्याविषयी",
    "🖼️ छायाचित्र दालन",
    "📅 कार्यक्रम वेळापत्रक",
    "📞 संपर्क",
    "🔐 प्रशासक",
]

MARATHI_WEEKDAYS = ["सोमवार", "मंगळवार", "बुधवार", "गुरुवार", "शुक्रवार", "शनिवार", "रविवार"]
MARATHI_MONTHS = [
    "जानेवारी", "फेब्रुवारी", "मार्च", "एप्रिल", "मे", "जून",
    "जुलै", "ऑगस्ट", "सप्टेंबर", "ऑक्टोबर", "नोव्हेंबर", "डिसेंबर",
]
DEV_DIGITS = str.maketrans("0123456789", "०१२३४५६७८९")

# ------------------------------------------------------------------
# CSS - तेजस्वी भगवा, लाल, सोनेरी आणि मरून रंगसंगती
# ------------------------------------------------------------------
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Devanagari:wght@400;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Noto Sans Devanagari', 'Nirmala UI', sans-serif;
}
.stApp {
    background: linear-gradient(180deg, #FFF6E0 0%, #FFE6BC 55%, #FFF6E0 100%);
}
.hero {
    background: linear-gradient(120deg, #FF9933 0%, #E53935 45%, #FFB300 100%);
    border-radius: 24px;
    padding: 2.4rem 1.5rem;
    text-align: center;
    color: #fff;
    box-shadow: 0 12px 32px rgba(229, 57, 53, .35);
    border: 3px solid #FFD54F;
    margin-bottom: 1.2rem;
}
.hero h1 {
    color: #fff;
    font-size: 2.1rem;
    font-weight: 800;
    margin: .2rem 0 0;
    text-shadow: 0 2px 8px rgba(0, 0, 0, .35);
}
.hero .sub { font-size: 1.08rem; margin-top: .6rem; letter-spacing: .5px; }
.om { font-size: 2.8rem; color: #FFEB3B; text-shadow: 0 0 12px #FF6F00; }
.card {
    background: #ffffff;
    border-left: 7px solid #E53935;
    border-radius: 18px;
    padding: 1.2rem 1.4rem;
    margin: .7rem 0;
    box-shadow: 0 6px 20px rgba(128, 0, 0, .12);
}
.card h3 { color: #800000; margin-top: 0; }
.card-gold { border-left-color: #FFB300; }
.card-green { border-left-color: #2E7D32; }
.card-blue  { border-left-color: #1565C0; }
.badge {
    display: inline-block;
    background: linear-gradient(90deg, #FFD54F, #FFB300);
    color: #4E0000;
    font-weight: 700;
    border-radius: 999px;
    padding: .2rem .9rem;
    font-size: .88rem;
}
.countdown {
    font-size: 1.6rem;
    font-weight: 800;
    color: #E53935;
}
.section-title {
    color: #800000;
    border-bottom: 4px solid #FF9933;
    padding-bottom: .35rem;
    margin-top: .8rem;
    font-weight: 800;
}
.about-title { color: #000 !important; }
.about-content,
.about-content * { color: #000 !important; }
.contact-title { color: #000 !important; }
.contact-content,
.contact-content * { color: #000 !important; }
.contact-row {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 1rem;
}
.contact-row .card { margin: .7rem 0; }
.contact-row .contact-line { overflow-wrap: anywhere; }
@media (max-width: 700px) {
    .contact-row { grid-template-columns: 1fr; }
}
.admin-title { color: #000 !important; }
.gallery-title,
.events-title,
.events-subtitle { color: #000 !important; }
.black-message { color: #000; }
.quote {
    background: linear-gradient(90deg, #FFF3CD, #FFE0B2);
    border-radius: 16px;
    padding: 1rem 1.2rem;
    border: 2px dashed #FF9933;
    color: #6D0000;
    font-weight: 600;
    text-align: center;
}
.contact-line { font-size: 1.08rem; margin: .4rem 0; }
.contact-line a { color: #1565C0; font-weight: 700; text-decoration: none; }
.footer {
    text-align: center;
    color: #800000;
    font-weight: 700;
    padding: 1rem;
    margin-top: 2rem;
    border-top: 3px solid #FF9933;
}
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #800000 0%, #B71C1C 50%, #E65100 100%);
}
section[data-testid="stSidebar"] * { color: #FFF8E1; }
section[data-testid="stSidebar"] h2 { color: #FFEB3B !important; }
.stButton > button {
    background: linear-gradient(90deg, #FF9933, #E53935);
    color: #fff;
    border: none;
    border-radius: 999px;
    font-weight: 700;
    padding: .5rem 1.4rem;
    box-shadow: 0 4px 12px rgba(229, 57, 53, .3);
}
.stButton > button:hover { filter: brightness(1.08); color: #fff; border: none; }
.stFormSubmitButton > button {
    background: linear-gradient(90deg, #FF9933, #E53935);
    color: #fff;
    border: none;
    border-radius: 999px;
    font-weight: 700;
}
</style>
"""


# ------------------------------------------------------------------
# डेटा व्यवस्थापन
# ------------------------------------------------------------------
def now_ist() -> datetime:
    return datetime.now(IST) if IST else datetime.now()


def load_data() -> dict:
    if DATA_FILE.exists():
        try:
            data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
            data.setdefault("images", [])
            data.setdefault("events", [])
            return data
        except json.JSONDecodeError:
            pass
    return {"images": [], "events": []}


def save_data(data: dict) -> None:
    DATA_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def mr_digits(text: str) -> str:
    return str(text).translate(DEV_DIGITS)


def fmt_date(d: date) -> str:
    return mr_digits(f"{d.day} {MARATHI_MONTHS[d.month - 1]} {d.year}, {MARATHI_WEEKDAYS[d.weekday()]}")


def parse_event_date(e: dict) -> date | None:
    try:
        return date.fromisoformat(e["date"])
    except (KeyError, ValueError, TypeError):
        return None


def split_events(events: list[dict]) -> tuple[list[dict], list[dict]]:
    today = now_ist().date()
    upcoming, past = [], []
    for e in events:
        d = parse_event_date(e)
        if d is None:
            continue
        (upcoming if d >= today else past).append((d, e))
    upcoming.sort(key=lambda x: (x[0], x[1].get("time", "")))
    past.sort(key=lambda x: x[0], reverse=True)
    return [e for _, e in upcoming], [e for _, e in past]


def countdown_text(d: date) -> str:
    delta = (d - now_ist().date()).days
    if delta == 0:
        return "🎉 आज कार्यक्रम आहे!"
    if delta == 1:
        return "⏳ उद्या कार्यक्रम आहे"
    return mr_digits(f"⏳ {delta} दिवस बाकी")


def image_path(img: dict) -> Path:
    return UPLOAD_DIR / img["file"]


# ------------------------------------------------------------------
# पृष्ठे
# ------------------------------------------------------------------
def render_home(data: dict) -> None:
    st.markdown(
        f"""
        <div class="hero">
            <div class="om">ॐ</div>
            <h1>{html.escape(MATH_NAME)}</h1>
            <div class="sub">श्रद्धा • भक्ती • अध्यात्म • गुरुपरंपरा</div>
            <div class="sub">📍 {MATH_PLACE}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    upcoming, _ = split_events(data["events"])
    st.markdown('<h2 class="section-title events-title">📅 पुढील कार्यक्रम</h2>', unsafe_allow_html=True)
    if upcoming:
        nxt = upcoming[0]
        d = parse_event_date(nxt)
        st.markdown(
            f"""
            <div class="card card-gold">
                <span class="badge">पुढील कार्यक्रम</span>
                <h3>{html.escape(nxt.get('title', ''))}</h3>
                <div>🗓️ {fmt_date(d)} {('• 🕒 ' + mr_digits(nxt['time'])) if nxt.get('time') else ''}</div>
                <div>📍 {html.escape(nxt.get('place', '') or MATH_PLACE)}</div>
                <div class="countdown">{countdown_text(d)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div class="black-message">सध्या कोणताही नियोजित कार्यक्रम नाही. '
            'लवकरच माहिती दिली जाईल.</div>',
            unsafe_allow_html=True,
        )

    st.markdown('<h2 class="section-title gallery-title">🖼️ ताजी छायाचित्रे</h2>', unsafe_allow_html=True)
    recent = list(reversed(data["images"]))[:3]
    if recent:
        cols = st.columns(3)
        for col, img in zip(cols, recent):
            with col:
                if image_path(img).exists():
                    st.image(str(image_path(img)), caption=img.get("caption") or None,
                             use_container_width=True)
    else:
        st.markdown('<div class="black-message">अद्याप छायाचित्रे उपलब्ध नाहीत.</div>',
                    unsafe_allow_html=True)

    st.markdown(
        '<div class="quote">॥ ॐ नमः शिवाय ॥<br>'
        "श्री सद्गुरू यज्ञेश्वर शिवाचार्य वेडे महाराज की जय</div>",
        unsafe_allow_html=True,
    )


def render_about() -> None:
    st.markdown('<h2 class="section-title about-title">🛕 आमच्याविषयी</h2>', unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="about-content">
        <div class="card">
            <h3>🕉️ {html.escape(MATH_NAME)}</h3>
            <p>महाराष्ट्राच्या पवित्र भूमीत वसलेला श्री सद्गुरू यज्ञेश्वर शिवाचार्य (वेडे महाराज)
            संजीवन समाधी मठ, परंडा हे श्रद्धा, भक्ती, अध्यात्म आणि गुरुपरंपरेचे एक पवित्र स्थान आहे.</p>
            <p>श्री सद्गुरू यज्ञेश्वर शिवाचार्य (वेडे महाराज) हे महान शिवयोगी, सद्गुरू आणि
            अध्यात्मिक परंपरेचे तेजस्वी प्रतीक होते. त्यांच्या पवित्र संजीवन समाधीला
            <b>{mr_digits('226')} वर्षांहून अधिक</b> प्राचीन इतिहास लाभलेला आहे. ही समाधी आजही
            असंख्य भाविकांसाठी श्रद्धेचे, भक्तीचे आणि आध्यात्मिक प्रेरणेचे केंद्र आहे.</p>
        </div>

        <div class="card card-green">
            <h3>🌿 अखंड गुरुपरंपरा</h3>
            <p>या मठाच्या गादीवर आजपर्यंत एकूण <b>{mr_digits('29')} महाराजांनी</b> विराजमान होऊन
            गुरुपरंपरेचा वारसा पुढे नेला आहे. ही गुरुपरंपरा आजही अखंडपणे जतन केली जात आहे.</p>
            <p>सध्या या पवित्र गादीवर विराजमान असलेले परमपूज्य गुरुवर्य
            <b>श्री. ष. ब्र. १०८ राचलिंग शिवाचार्य परंडकर महाराज</b> यांच्या मार्गदर्शनाखाली
            मठाची धार्मिक, आध्यात्मिक आणि सामाजिक परंपरा पुढे सुरू आहे.</p>
        </div>

        <div class="card card-blue">
            <h3>🔱 धार्मिक व आध्यात्मिक उपक्रम</h3>
            <ul>
                <li>अखंड शिवनाम सप्ताह</li>
                <li>परम रहस्य ग्रंथाचे पारायण</li>
                <li>संगीतमय शिवपाठ</li>
                <li>रुद्राभिषेक व बिल्वार्चन</li>
                <li>सामूहिक इष्टलिंग महापूजा</li>
                <li>गुरुपुण्यतिथी महोत्सव</li>
                <li>रथोत्सव व धर्मसभा</li>
                <li>महाप्रसाद व भक्तीमय धार्मिक सोहळे</li>
            </ul>
            <p>या कार्यक्रमांच्या माध्यमातून भाविकांना अध्यात्मिक शांती, गुरुभक्ती आणि
            धार्मिक संस्कारांचा अनुभव मिळतो.</p>
        </div>

        <div class="card">
            <h3>🪔 आमची श्रद्धा आणि परंपरा</h3>
            <p>शिवभक्ती, गुरुभक्ती, सेवा, समर्पण आणि मानवकल्याण ही या मठाची प्रमुख मूल्ये आहेत.
            सद्गुरूंच्या शिकवणीचा प्रसार करणे, धार्मिक परंपरांचे जतन करणे आणि भाविकांना
            अध्यात्मिक मार्गदर्शन उपलब्ध करून देणे हा मठाचा प्रमुख उद्देश आहे.</p>
            <p>श्री सद्गुरूंच्या पवित्र संजीवन समाधीचे दर्शन घेऊन गुरुकृपेचा अनुभव घेण्यासाठी
            सर्व शिवभक्तांचे आणि भाविकांचे <b>हार्दिक स्वागत!</b> 🙏</p>
        </div>

        <div class="quote">
            गुरुर्ब्रह्मा गुरुर्विष्णुः गुरुर्देवो महेश्वरः।<br>
            गुरुः साक्षात् परब्रह्म तस्मै श्री गुरवे नमः॥
        </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_gallery(data: dict) -> None:
    st.markdown('<h2 class="section-title gallery-title">🖼️ छायाचित्र दालन</h2>', unsafe_allow_html=True)
    images = list(reversed(data["images"]))
    if not images:
        st.markdown('<div class="black-message">अद्याप छायाचित्रे जोडलेली नाहीत.</div>', unsafe_allow_html=True)
        return
    cols = st.columns(3)
    shown = 0
    for img in images:
        if not image_path(img).exists():
            continue
        with cols[shown % 3]:
            st.image(str(image_path(img)), caption=img.get("caption") or None,
                     use_container_width=True)
        shown += 1


def render_events(data: dict) -> None:
    st.markdown('<h2 class="section-title events-title">📅 कार्यक्रम वेळापत्रक</h2>', unsafe_allow_html=True)
    upcoming, past = split_events(data["events"])

    st.markdown('<h4 class="events-subtitle">🔜 आगामी कार्यक्रम</h4>', unsafe_allow_html=True)
    if not upcoming:
        st.markdown('<div class="black-message">सध्या कोणताही आगामी कार्यक्रम नाही.</div>', unsafe_allow_html=True)
    for i, e in enumerate(upcoming):
        d = parse_event_date(e)
        badge = '<span class="badge">पुढील</span>' if i == 0 else ""
        st.markdown(
            f"""
            <div class="card {'card-gold' if i == 0 else ''}">
                {badge}
                <h3>{html.escape(e.get('title', ''))}</h3>
                <div>🗓️ <b>{fmt_date(d)}</b>{(' • 🕒 ' + mr_digits(e['time'])) if e.get('time') else ''}</div>
                <div>📍 {html.escape(e.get('place', '') or MATH_PLACE)}</div>
                <p>{html.escape(e.get('description', ''))}</p>
                <div class="countdown" style="font-size:1.1rem">{countdown_text(d)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    if past:
        with st.expander(f"🕰️ मागील कार्यक्रम ({mr_digits(len(past))})"):
            for e in past:
                d = parse_event_date(e)
                st.markdown(
                    f"- **{html.escape(e.get('title', ''))}** — {fmt_date(d)}"
                    f"{(' • ' + mr_digits(e['time'])) if e.get('time') else ''}"
                )


def render_contact() -> None:
    st.markdown('<h2 class="section-title contact-title">📞 संपर्क</h2>', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="contact-content">
        <div class="contact-row">
        <div class="card">
            <h3>🙏 {html.escape(MAHARAJ_NAME)}</h3>
            <div class="contact-line">📱 मोबाईल:
                <a href="tel:+91{MAHARAJ_PHONES[0]}">{mr_digits(MAHARAJ_PHONES[0])} ({MAHARAJ_PHONES[0]})</a>
                /
                <a href="tel:+91{MAHARAJ_PHONES[1]}">{mr_digits(MAHARAJ_PHONES[1])} ({MAHARAJ_PHONES[1]})</a>
            </div>
        </div>
        <div class="card">
            <h3>🙏 {html.escape(CONTACT_NAME)}</h3>
            <div class="contact-line">📱 मोबाईल: <a href="tel:+91{CONTACT_PHONE}">{mr_digits(CONTACT_PHONE)} ({CONTACT_PHONE})</a></div>
            <div class="contact-line">✉️ ईमेल: <a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a></div>
            <div class="contact-line">📍 पत्ता: {html.escape(MATH_NAME)}, {MATH_PLACE}</div>
        </div>
        </div>
        <div class="quote">भक्तांचे स्वागत आहे — दर्शन, माहिती किंवा मार्गदर्शनासाठी संपर्क साधा.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_admin(data: dict) -> None:
    st.markdown('<h2 class="section-title admin-title">🔐 प्रशासक विभाग</h2>', unsafe_allow_html=True)

    if not st.session_state.get("is_admin"):
        if not ADMIN_PASSWORD:
            st.error(
                "प्रशासक पासवर्ड सेट केलेला नाही. कृपया `MATH_ADMIN_PASSWORD` "
                "environment variable सेट करून अॅप पुन्हा सुरू करा."
            )
            return
        with st.form("login_form"):
            pw = st.text_input("प्रशासक पासवर्ड", type="password")
            ok = st.form_submit_button("प्रवेश करा")
        if ok:
            if hmac.compare_digest(pw.encode("utf-8"), ADMIN_PASSWORD.encode("utf-8")):
                st.session_state.is_admin = True
                st.rerun()
            else:
                st.error("पासवर्ड चुकीचा आहे.")
        return

    top = st.columns([4, 1])
    top[0].success("प्रशासक म्हणून प्रवेश केला आहे.")
    if top[1].button("बाहेर पडा"):
        st.session_state.is_admin = False
        st.rerun()

    tab_upload, tab_manage_img, tab_add_event, tab_manage_event = st.tabs(
        ["➕ छायाचित्रे जोडा", "🗂️ छायाचित्रे व्यवस्थापन",
         "🗓️ कार्यक्रम जोडा", "🧾 कार्यक्रम व्यवस्थापन"]
    )

    # --- छायाचित्रे जोडा ---
    with tab_upload:
        with st.form("upload_form", clear_on_submit=True):
            files = st.file_uploader(
                "छायाचित्रे निवडा (JPG / PNG / WEBP)",
                type=["jpg", "jpeg", "png", "webp"],
                accept_multiple_files=True,
            )
            caption = st.text_input("शीर्षक (ऐच्छिक)")
            submitted = st.form_submit_button("छायाचित्रे जतन करा")
        if submitted:
            if not files:
                st.warning("कृपया किमान एक छायाचित्र निवडा.")
            else:
                for f in files:
                    ext = Path(f.name).suffix.lower()
                    fname = f"{uuid.uuid4().hex}{ext}"
                    (UPLOAD_DIR / fname).write_bytes(f.getbuffer())
                    data["images"].append({
                        "id": uuid.uuid4().hex,
                        "file": fname,
                        "caption": caption.strip(),
                        "uploaded": now_ist().strftime("%Y-%m-%d"),
                    })
                save_data(data)
                st.success(mr_digits(f"{len(files)} छायाचित्रे यशस्वीरीत्या जोडली गेली."))

    # --- छायाचित्रे व्यवस्थापन ---
    with tab_manage_img:
        if not data["images"]:
            st.info("अद्याप छायाचित्रे नाहीत.")
        for img in list(reversed(data["images"])):
            c1, c2 = st.columns([1, 2])
            if image_path(img).exists():
                c1.image(str(image_path(img)), use_container_width=True)
            c2.markdown(f"**शीर्षक:** {img.get('caption') or '—'}")
            c2.caption(f"अपलोड: {mr_digits(img.get('uploaded', ''))}")
            if c2.button("हटवा", key=f"del_img_{img['id']}"):
                if image_path(img).exists():
                    image_path(img).unlink()
                data["images"] = [i for i in data["images"] if i["id"] != img["id"]]
                save_data(data)
                st.rerun()
            st.divider()

    # --- कार्यक्रम जोडा ---
    with tab_add_event:
        with st.form("event_form", clear_on_submit=True):
            title = st.text_input("कार्यक्रमाचे नाव *")
            c1, c2 = st.columns(2)
            ev_date = c1.date_input("तारीख", value=now_ist().date())
            ev_time = c2.time_input("वेळ", value=time(8, 0))
            place = st.text_input("ठिकाण", value=MATH_PLACE)
            desc = st.text_area("माहिती / विशेष सूचना")
            sub = st.form_submit_button("कार्यक्रम जोडा")
        if sub:
            if not title.strip():
                st.warning("कार्यक्रमाचे नाव आवश्यक आहे.")
            else:
                data["events"].append({
                    "id": uuid.uuid4().hex,
                    "title": title.strip(),
                    "date": ev_date.isoformat(),
                    "time": ev_time.strftime("%H:%M"),
                    "place": place.strip(),
                    "description": desc.strip(),
                })
                save_data(data)
                st.success("कार्यक्रम वेळापत्रकात जोडला गेला.")

    # --- कार्यक्रम व्यवस्थापन ---
    with tab_manage_event:
        if not data["events"]:
            st.info("अद्याप कोणताही कार्यक्रम नाही.")
        for e in sorted(data["events"], key=lambda x: x.get("date", ""), reverse=True):
            d = parse_event_date(e)
            label = f"{e.get('title', '')} — {fmt_date(d) if d else e.get('date', '')}"
            c1, c2 = st.columns([4, 1])
            c1.markdown(f"**{label}**")
            if c2.button("हटवा", key=f"del_ev_{e['id']}"):
                data["events"] = [x for x in data["events"] if x["id"] != e["id"]]
                save_data(data)
                st.rerun()


# ------------------------------------------------------------------
# मुख्य अॅप
# ------------------------------------------------------------------
def main() -> None:
    st.set_page_config(page_title=MATH_NAME, page_icon="🕉️", layout="wide")
    st.markdown(CSS, unsafe_allow_html=True)

    if "is_admin" not in st.session_state:
        st.session_state.is_admin = False

    with st.sidebar:
        st.markdown("## 🕉️ मठ मार्गदर्शक")
        st.markdown(f"**{MATH_NAME}**")
        page = st.radio("पृष्ठे", PAGES, label_visibility="collapsed")
        st.markdown("---")
        st.caption("॥ ॐ नमः शिवाय ॥")

    data = load_data()

    if page == PAGES[0]:
        render_home(data)
    elif page == PAGES[1]:
        render_about()
    elif page == PAGES[2]:
        render_gallery(data)
    elif page == PAGES[3]:
        render_events(data)
    elif page == PAGES[4]:
        render_contact()
    elif page == PAGES[5]:
        render_admin(data)

    st.markdown(
        f'<div class="footer">{html.escape(MATH_NAME)} • {MATH_PLACE}<br>'
        "॥ श्री सद्गुरू यज्ञेश्वर शिवाचार्य वेडे महाराज की जय ॥</div>",
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
