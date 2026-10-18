import urllib.request
import hashlib
import os

NTFY_TOPIC = os.getenv("NTFY_TOPIC")
if not NTFY_TOPIC:
    raise RuntimeError("Missing required environment variable: NTFY_TOPIC")

# Live job boards covering TfL, Overground (Willesden/Richmond), and SWR (Richmond/Egham)
URLS = {
    "TfL Careers": "https://london-gov.jobs2web.com/tfl/search/?q=Customer+Service",
    "South Western Railway (Richmond/Egham)": "https://careers.southwesternrailway.com/jobs/search",
    "Arriva Overground (Willesden/Richmond)": "https://www.arrivaraillondon.co.uk/careers/",
    "Railway Careers UK (SWR Live Feed)": "https://railwaycareers.co.uk/operators/south-western-railway"
}

# Keywords tailored for a 19yo part-time student around your stations
ROLE_KEYWORDS = [
    "customer service assistant", "csa", "night tube", 
    "part time", "part-time", "rail operator", 
    "station assistant", "customer host", "gateline"
]

LOCATION_KEYWORDS = ["richmond", "willesden", "egham", "feltham", "twickenham", "staines"]

def send_ping(title, message, link):
    req = urllib.request.Request(
        f"https://ntfy.sh/{NTFY_TOPIC}",
        data=message.encode('utf-8'),
        headers={
            "Title": title,
            "Priority": "high",
            "Tags": "train,rotating_light",
            "Click": link
        }
    )
    urllib.request.urlopen(req, timeout=10)

for name, url in URLS.items():
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        html = urllib.request.urlopen(req, timeout=20).read().decode('utf-8', errors='ignore').lower()
        
        found_roles = [kw for kw in ROLE_KEYWORDS if kw in html]
        found_locs = [loc for loc in LOCATION_KEYWORDS if loc in html]
        
        # Create a fingerprint of the matched keywords + page content length
        fingerprint_source = f"{found_roles}_{found_locs}_{len(html) // 500}"
        current_hash = hashlib.md5(fingerprint_source.encode()).hexdigest()
        
        safe_name = "".join(c if c.isalnum() else "_" for c in name)
        state_file = f"state_{safe_name}.txt"
        
        old_hash = ""
        if os.path.exists(state_file):
            with open(state_file, "r") as f:
                old_hash = f.read().strip()
        
        # Trigger notification if roles are spotted and the page state is new
        if found_roles and current_hash != old_hash:
            loc_text = f" | Locations spotted: {', '.join(found_locs)}" if found_locs else ""
            msg = f"Roles spotted: {', '.join(found_roles)}{loc_text}. Tap to view and apply!"
            send_ping(f"New Rail Job Alert: {name}", msg, url)
            
            with open(state_file, "w") as f:
                f.write(current_hash)
            print(f"Alert sent for {name}!")
        else:
            print(f"Checked {name} - no new changes.")
            
    except Exception as e:
        print(f"Error checking {name}: {e}")
