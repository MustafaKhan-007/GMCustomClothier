# G&M Custom Clothier Prototype

Full-stack Flask prototype website for G&M Custom Clothier, a bespoke tailoring and bridal alterations shop in Sugar Land, TX. The site uses server-rendered Flask/Jinja templates, local structured content, vanilla JavaScript, and a restrained dark editorial visual system.

## Tech Stack

- Flask + Jinja2
- Vanilla CSS and JavaScript
- Local JSON inquiry logging
- Gunicorn for Render deployment

## Local Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:FLASK_APP="app.py"
$env:FLASK_ENV="development"
flask run
```

Then open `http://127.0.0.1:5000`.

You can also run:

```powershell
python app.py
```

## Render Deployment

1. Push this folder to a Git repository.
2. In Render, create a new Web Service and connect the repo.
3. Confirm the build command is `pip install -r requirements.txt`.
4. Confirm the start command is `gunicorn app:app`.
5. Add a production `SECRET_KEY` environment variable if not using `render.yaml`.
6. Deploy.

The included `Procfile` and `render.yaml` are ready for a simple Python web service.

## Images To Replace

The site currently uses local SVG placeholder image slots in `static/images/`. Replace these with real, permission-cleared client photography before launch. Keep filenames the same or update `data/content.py`.

- `hero-atelier.svg`: currently a dark atelier hero placeholder. Replace with a real wide photo of the G&M fitting room, storefront interior, or tailoring table.
- `tailor-portrait-genaro.svg`: currently a portrait placeholder. Replace with a permission-cleared portrait of Genaro at work.
- `fitting-detail-1.svg`: currently a fitting detail placeholder. Replace with a real sleeve, hem, jacket, or gown fitting detail.
- `suit-rack.svg`: currently a custom suit rack placeholder. Replace with actual finished suits, jackets, or formalwear from G&M.
- `bridal-alteration.svg`: currently a bridal alteration placeholder. Replace with a permission-cleared bridal gown alteration or lacework photo.
- `fabric-swatches.svg`: currently a fabric and measurement placeholder. Replace with actual fabric books, shirting swatches, or tailor tools from the shop.
- `tuxedo-fitting.svg`: currently a formal tuxedo placeholder. Replace with a real tuxedo rental or wedding party fitting photo.
- `embroidery-detail.svg`: currently an embroidery detail placeholder. Replace with a real custom embroidery sample from G&M.
- `custom-draperies.svg`: currently a drapery placeholder. Replace with a finished drapery installation or fabric work photo.
- `editorial-break.svg`: currently a full-width editorial image placeholder. Replace with a full-width atelier, fitting, or finished garment photograph.

Do not scrape Yelp, Instagram, or Facebook for images at build time or runtime. Mustafa should obtain usage permission from the shop owner before using photos from Instagram, Yelp, Facebook, or any client gallery.

## Pricing Note

Pricing is intentionally omitted because no public price list exists for the business, which is normal for bespoke tailoring and alteration work. The current templates use consultation-based language from `data/content.py`.

If the client later chooses to publish pricing, add the approved numbers to `PRICING_NOTE` or to each service object in `data/content.py`, then update `templates/services.html` to render those fields.

## Contact Form Note

The contact form currently validates submissions and appends them to `data/inquiries.json`. It does not send email.

Before going live, wire the TODO in `app.py` to Flask-Mail, SMTP, or a transactional email service once the client provides hosting email credentials.
