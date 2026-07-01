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

The site currently uses local image slots in `static/images/`, including SVG placeholders, a JPEG portrait, and normalized PNG service artwork. Replace these with real, permission-cleared client photography before launch. Keep filenames the same or update `data/content.py`.

- `hero-atelier.jpg`: currently the homepage hero image with tailoring shears, measuring tape, chalk, thread, and pins. Replace only if the client provides a newer approved hero image.
- `tailor-portrait-genaro.jpeg`: currently the lead tailor portrait slot. Replace only if the client provides a newer permission-cleared portrait of Genaro at work.
- `fitting-detail-1.png`: currently normalized general alterations and repairs artwork. Replace only if the client provides approved real alterations photography.
- `suit-rack.png`: currently normalized custom suits and sports jackets artwork. Replace only if the client provides approved real suit or jacket photography.
- `bridal-alteration.png`: currently normalized bridal and formal alterations artwork. Replace only if the client provides approved bridal or formalwear photography.
- `fabric-swatches.png`: currently normalized custom dress shirts artwork. Replace only if the client provides approved shirtmaking or fabric photography.
- `tuxedo-fitting.png`: currently normalized tuxedo rentals artwork. Replace only if the client provides approved tuxedo or formalwear photography.
- `embroidery-detail.png`: currently normalized embroidery artwork. Replace only if the client provides approved embroidery photography.
- `custom-draperies.png`: currently normalized custom draperies artwork. Replace only if the client provides approved drapery photography.
- `editorial-break.svg`: currently a full-width editorial image placeholder. Replace with a full-width atelier, fitting, or finished garment photograph.

Do not scrape Yelp, Instagram, or Facebook for images at build time or runtime. Mustafa should obtain usage permission from the shop owner before using photos from Instagram, Yelp, Facebook, or any client gallery.

## Pricing Note

Pricing is intentionally omitted because no public price list exists for the business, which is normal for bespoke tailoring and alteration work. The current templates use consultation-based language from `data/content.py`.

If the client later chooses to publish pricing, add the approved numbers to `PRICING_NOTE` or to each service object in `data/content.py`, then update `templates/services.html` to render those fields.

## Contact Form Note

The contact form currently validates submissions and appends them to `data/inquiries.json`. It does not send email.

Before going live, wire the TODO in `app.py` to Flask-Mail, SMTP, or a transactional email service once the client provides hosting email credentials.
