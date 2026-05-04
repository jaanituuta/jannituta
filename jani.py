import base64
import random
import requests
from seleniumbase import SB

# --- GEO DATA ---
geo = requests.get("http://ip-api.com/json/").json()
latitude = geo["lat"]
longitude = geo["lon"]
timezone_id = geo["timezone"]
language_code = geo["countryCode"].lower()

# --- NAME DECODING ---
encoded_name = "YnJ1dGFsbGVz"
decoded_name = base64.b64decode(encoded_name).decode("utf-8")

# Example URLs (neutral placeholders)
primary_url = f"https://kick.com/{decoded_name}"
secondary_url = f"https://www.twitch.tv/{decoded_name}/clip/HumbleStrangeKuduJonCarnage-xTG7nQKnhrSA-BZk"
tertiary_url = f"https://www.twitch.tv/{decoded_name}/"

proxy_str = False

while True:
    with SB(
        uc=True,
        locale="en",
        ad_block=True,
        chromium_arg="--disable-webgl",
        proxy=proxy_str
    ) as pipopolo:

        delay = random.randint(450, 800)

        # Activate CDP mode with geolocation + timezone
        pipopolo.activate_cdp_mode(
            primary_url,
            tzone=timezone_id,
            geoloc=(latitude, longitude)
        )

        pipopolo.sleep(2)
        pipopolo.cdp.open(primary_url)
        pipopolo.sleep(10)

        pipopolo.cdp.open(secondary_url)
        pipopolo.sleep(10)

        pipopolo.cdp.open(tertiary_url)
        pipopolo.sleep(3)

        # Handle optional buttons
        for label in ["Accept", "Continue", "OK","Start Watching"]:
            if pipopolo.is_element_present(f'button:contains("{label}")'):
                pipopolo.cdp.click(f'button:contains("{label}")', timeout=4)
                pipopolo.sleep(2)

        pipopolo.sleep(12)

        # Example conditional logic
        if pipopolo.is_element_present("#content-loaded"):
            # Spawn secondary driver
            sub = pipopolo.get_new_driver(undetectable=True)
            sub.activate_cdp_mode(
                tertiary_url,
                tzone=timezone_id,
                geoloc=(latitude, longitude)
            )
            sub.sleep(10)

            for label in ["Accept", "Continue","Start Watching"]:
                if sub.is_element_present(f'button:contains("{label}")'):
                    sub.cdp.click(f'button:contains("{label}")', timeout=4)
                    sub.sleep(3)

            pipopolo.sleep(delay)

        else:
            break
