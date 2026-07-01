import json
import os
import threading
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote_plus

from flask import Flask, flash, redirect, render_template, request, url_for

from config import Config
from data.content import (
    ABOUT_COPY,
    AMENITIES,
    BUSINESS,
    GALLERY,
    HOURS,
    IMAGE_SLOTS,
    MAP_QUERY,
    PAYMENT_METHODS,
    PRICING_NOTE,
    PROCESS_STEPS,
    REVIEW_SNAPSHOT,
    SERVICES,
    SOCIAL,
    TESTIMONIALS,
)


app = Flask(__name__)
app.config.from_object(Config)

INQUIRY_FILE = Path(__file__).resolve().parent / "data" / "inquiries.json"
INQUIRY_LOCK = threading.Lock()


def image_path(filename):
    return url_for("static", filename=f"images/{filename}")


def map_embed_url():
    return f"https://www.google.com/maps?q={quote_plus(MAP_QUERY)}&output=embed"


@app.context_processor
def inject_globals():
    return {
        "business": BUSINESS,
        "hours": HOURS,
        "services": SERVICES,
        "social": SOCIAL,
        "payment_methods": PAYMENT_METHODS,
        "amenities": AMENITIES,
        "map_query": MAP_QUERY,
        "map_embed_url": map_embed_url(),
        "image_path": image_path,
    }


def page_meta(title, description):
    return {
        "title": f"{title} | {BUSINESS['name']}",
        "description": description,
    }


@app.route("/")
def index():
    return render_template(
        "index.html",
        active_page="home",
        meta=page_meta(
            "Bespoke Tailoring in Sugar Land",
            "G&M Custom Clothier offers custom suits, bridal alterations, tuxedo rentals, embroidery, and expert alterations in Sugar Land, TX.",
        ),
        about_copy=ABOUT_COPY,
        testimonials=TESTIMONIALS,
        review_snapshot=REVIEW_SNAPSHOT,
    )


@app.route("/services")
def services_page():
    return render_template(
        "services.html",
        active_page="services",
        meta=page_meta(
            "Services",
            "Explore custom suits, dress shirts, bridal alterations, tuxedo rentals, embroidery, repairs, and custom draperies from G&M Custom Clothier.",
        ),
        pricing_note=PRICING_NOTE,
    )


@app.route("/about")
def about():
    return render_template(
        "about.html",
        active_page="about",
        meta=page_meta(
            "About Genaro and the Shop",
            "Learn about G&M Custom Clothier, led by master tailor Genaro with 15+ years of tailoring experience in Sugar Land.",
        ),
        about_copy=ABOUT_COPY,
        process_steps=PROCESS_STEPS,
    )


@app.route("/gallery")
def gallery():
    return render_template(
        "gallery.html",
        active_page="gallery",
        meta=page_meta(
            "Gallery",
            "View placeholder tailoring, bridal, formalwear, fabric, and atelier photography slots for the G&M Custom Clothier prototype.",
        ),
        gallery=GALLERY,
    )


@app.route("/reviews")
def reviews():
    return render_template(
        "reviews.html",
        active_page="reviews",
        meta=page_meta(
            "Reviews",
            "Read paraphrased public review highlights for G&M Custom Clothier and find links to public review platforms.",
        ),
        testimonials=TESTIMONIALS,
        review_snapshot=REVIEW_SNAPSHOT,
    )


def validate_inquiry(form):
    required = ["name", "phone", "email", "service", "preferred_date", "message"]
    errors = {}
    for field in required:
        if not form.get(field, "").strip():
            errors[field] = "This field is required."
    if form.get("email") and "@" not in form.get("email", ""):
        errors["email"] = "Enter a valid email address."
    if form.get("service") and form.get("service") not in {service["name"] for service in SERVICES}:
        errors["service"] = "Choose a listed service."
    return errors


def append_inquiry(payload):
    INQUIRY_FILE.parent.mkdir(parents=True, exist_ok=True)
    with INQUIRY_LOCK:
        if INQUIRY_FILE.exists():
            try:
                existing = json.loads(INQUIRY_FILE.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                existing = []
        else:
            existing = []
        existing.append(payload)
        tmp_file = INQUIRY_FILE.with_suffix(".tmp")
        tmp_file.write_text(json.dumps(existing, indent=2), encoding="utf-8")
        tmp_file.replace(INQUIRY_FILE)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    errors = {}
    form_data = {}
    if request.method == "POST":
        form_data = {key: request.form.get(key, "").strip() for key in request.form}
        errors = validate_inquiry(form_data)
        if not errors:
            inquiry = {
                "submitted_at": datetime.now(timezone.utc).isoformat(),
                "name": form_data["name"],
                "phone": form_data["phone"],
                "email": form_data["email"],
                "service": form_data["service"],
                "preferred_date": form_data["preferred_date"],
                "message": form_data["message"],
            }
            append_inquiry(inquiry)
            # TODO: wire up Flask-Mail or SMTP once client provides hosting email creds.
            flash("Thank you. Your consultation request has been logged for the prototype.", "success")
            return redirect(url_for("contact", submitted="1"))

    return render_template(
        "contact.html",
        active_page="contact",
        meta=page_meta(
            "Contact & Booking",
            "Contact G&M Custom Clothier in Sugar Land, TX for custom tailoring, bridal alterations, tuxedo rentals, and consultation requests.",
        ),
        errors=errors,
        form_data=form_data,
    )


@app.route("/robots.txt")
def robots_txt():
    return app.response_class("User-agent: *\nAllow: /\nSitemap: /sitemap.xml\n", mimetype="text/plain")


@app.route("/sitemap.xml")
def sitemap_xml():
    pages = ["index", "services_page", "about", "gallery", "reviews", "contact"]
    base_url = request.url_root.rstrip("/")
    xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for endpoint in pages:
        xml.append(f"  <url><loc>{base_url}{url_for(endpoint)}</loc></url>")
    xml.append("</urlset>")
    return app.response_class("\n".join(xml), mimetype="application/xml")


@app.errorhandler(404)
def not_found(_error):
    return (
        render_template(
            "404.html",
            active_page=None,
            meta=page_meta(
                "Page Not Found",
                "The requested G&M Custom Clothier page could not be found.",
            ),
        ),
        404,
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=app.config["DEBUG"])
