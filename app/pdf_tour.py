import base64, io, requests, qrcode
from datetime import date
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

# ----------------------------------------------------------------------
# Paths & Jinja environment
# ----------------------------------------------------------------------
BASE_DIR      = Path(__file__).parent
TEMPLATE_DIR  = BASE_DIR / "templates"
STATIC_DIR    = BASE_DIR / "static"
env           = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

# ----------------------------------------------------------------------
# Logo for watermark (base64)
# ----------------------------------------------------------------------
LOGO_PATH = STATIC_DIR / "WRA Modern Logo.png"   # adjust if needed
logo_b64  = base64.b64encode(LOGO_PATH.read_bytes()).decode()

# ----------------------------------------------------------------------
# QR helper
# ----------------------------------------------------------------------
def qr_b64_for_stop(lat: float, lon: float) -> str:
    """
    Returns base64‑encoded PNG QR that opens Google Maps at the stop.
    """
    url = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"
    qr = qrcode.QRCode(border=1, box_size=3)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode()

# ----------------------------------------------------------------------
# Static map (Mapbox) helper
# ----------------------------------------------------------------------
def build_map_image(stops, width=600, height=500) -> str:
    """
    Returns base64 PNG of a static map with auto‑zoomed markers.
    """
    token = "YOUR_MAPBOX_TOKEN"  # <-- replace with env var / secret
    markers = [f"pin-s+555555({s['lon']},{s['lat']})" for s in stops]
    url = (
        "https://api.mapbox.com/styles/v1/mapbox/streets-v11/static/"
        f"{','.join(markers)}/auto/{width}x{height}@2x"
        f"?access_token={token}"
    )
    img_bytes = requests.get(url).content
    return base64.b64encode(img_bytes).decode()

# ----------------------------------------------------------------------
# Main PDF builder
# ----------------------------------------------------------------------
def build_tour_pdf(tour: dict, outfile: str) -> None:
    """
    tour = {
        'client_name': str,
        'date': 'YYYY-MM-DD',
        'start_time': 'HH:MM AM',
        'hero_image': 'https://...',
        'logo':       'https://...',
        'stops': [
            {
              'time': '11:30 AM',
              'address': '...',
              'floor': '3rd Floor',
              'lat': 42.37,
              'lon': -71.23,
              'image_url': 'https://...',
              'floorplan_url': 'https://...'
            },
            ...
        ]
    }
    """
    # Add QR codes to each stop
    for stop in tour["stops"]:
        stop["qr_b64"] = qr_b64_for_stop(stop["lat"], stop["lon"])

    # Build static map
    map_b64 = build_map_image(tour["stops"])

    # Render HTML
    template = env.get_template("tour_schedule.html")
    html_str = template.render(
        tour=tour,
        map_b64=map_b64,
        logo_b64=logo_b64,
        today=date.today().strftime("%B %d, %Y"),
    )

    # Output PDF
    HTML(string=html_str, base_url=".").write_pdf(outfile)

# ----------------------------------------------------------------------
# CLI / quick test
# ----------------------------------------------------------------------
if __name__ == "__main__":
    sample_tour = {
        "client_name": "Elpis Biopharmaceuticals",
        "date": "March 24, 2025",
        "start_time": "11:30 AM",
        "hero_image": "https://example.com/hero.jpg",
        "logo": "https://example.com/logo.png",
        "stops": [
            {
                "time": "11:30 AM",
                "address": "10 Beaver St, Waltham, MA",
                "floor": "3rd Floor",
                "lat": 42.3763,
                "lon": -71.2351,
                "image_url": "https://example.com/prop1.jpg",
                "floorplan_url": "https://example.com/prop1_fp.jpg",
            },
            # ... more stops ...
        ],
    }
    build_tour_pdf(sample_tour, "tour_schedule.pdf")import base64, io, requests, qrcode
from datetime import date
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

# ----------------------------------------------------------------------
# Paths & Jinja environment
# ----------------------------------------------------------------------
BASE_DIR      = Path(__file__).parent
TEMPLATE_DIR  = BASE_DIR / "templates"
STATIC_DIR    = BASE_DIR / "static"
env           = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

# ----------------------------------------------------------------------
# Logo for watermark (base64)
# ----------------------------------------------------------------------
LOGO_PATH = STATIC_DIR / "WRA Modern Logo.png"   # adjust if needed
logo_b64  = base64.b64encode(LOGO_PATH.read_bytes()).decode()

# ----------------------------------------------------------------------
# QR helper
# ----------------------------------------------------------------------
def qr_b64_for_stop(lat: float, lon: float) -> str:
    """
    Returns base64‑encoded PNG QR that opens Google Maps at the stop.
    """
    url = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"
    qr = qrcode.QRCode(border=1, box_size=3)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode()

# ----------------------------------------------------------------------
# Static map (Mapbox) helper
# ----------------------------------------------------------------------
def build_map_image(stops, width=600, height=500) -> str:
    """
    Returns base64 PNG of a static map with auto‑zoomed markers.
    """
    token = "YOUR_MAPBOX_TOKEN"  # <-- replace with env var / secret
    markers = [f"pin-s+555555({s['lon']},{s['lat']})" for s in stops]
    url = (
        "https://api.mapbox.com/styles/v1/mapbox/streets-v11/static/"
        f"{','.join(markers)}/auto/{width}x{height}@2x"
        f"?access_token={token}"
    )
    img_bytes = requests.get(url).content
    return base64.b64encode(img_bytes).decode()

# ----------------------------------------------------------------------
# Main PDF builder
# ----------------------------------------------------------------------
def build_tour_pdf(tour: dict, outfile: str) -> None:
    """
    tour = {
        'client_name': str,
        'date': 'YYYY-MM-DD',
        'start_time': 'HH:MM AM',
        'hero_image': 'https://...',
        'logo':       'https://...',
        'stops': [
            {
              'time': '11:30 AM',
              'address': '...',
              'floor': '3rd Floor',
              'lat': 42.37,
              'lon': -71.23,
              'image_url': 'https://...',
              'floorplan_url': 'https://...'
            },
            ...
        ]
    }
    """
    # Add QR codes to each stop
    for stop in tour["stops"]:
        stop["qr_b64"] = qr_b64_for_stop(stop["lat"], stop["lon"])

    # Build static map
    map_b64 = build_map_image(tour["stops"])

    # Render HTML
    template = env.get_template("tour_schedule.html")
    html_str = template.render(
        tour=tour,
        map_b64=map_b64,  
        logo_b64=logo_b64,
        today=date.today().strftime("%B %d, %Y"),
    )

    # Output PDF
    HTML(string=html_str, base_url=".").write_pdf(outfile)

# ----------------------------------------------------------------------
# CLI / quick test
# ----------------------------------------------------------------------
if __name__ == "__main__":
    sample_tour = {
        "client_name": "Elpis Biopharmaceuticals",
        "date": "March 24, 2025",
        "start_time": "11:30 AM",
        "hero_image": "https://example.com/hero.jpg",
        "logo": "https://example.com/logo.png",
        "stops": [
            {
                "time": "11:30 AM",
                "address": "10 Beaver St, Waltham, MA",
                "floor": "3rd Floor",
                "lat": 42.3763,
                "lon": -71.2351,
                "image_url": "https://example.com/prop1.jpg",
                "floorplan_url": "https://example.com/prop1_fp.jpg",
            },
            # ... more stops ...
        ],
    }
    build_tour_pdf(sample_tour, "tour_schedule.pdf")
  Add PDF tour generator
