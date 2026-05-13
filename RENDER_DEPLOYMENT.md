# Render Deployment Guide — Tatle Tale Flask Website

This package is ready to deploy as a Render **Web Service**.

## What is included

- Flask backend for all pages.
- `/booking` POST form handling with a persistent booking counter and booking records.
- `/survey` POST form handling.
- `/api/feedback` JSON form handling.
- `/api/contact` form endpoint.
- `gunicorn` production server dependency.
- `/health` endpoint for Render health checks.
- `render.yaml` Blueprint with a persistent disk mounted at `/var/data`.

## Important security note

Do **not** upload a real `.env` file to GitHub. Add your email credentials only in the Render dashboard under Environment Variables.

## Deploy with Render Blueprint

1. Push this `flask_project` folder to a GitHub repository.
2. In Render, choose **New +** → **Blueprint**.
3. Select the GitHub repository.
4. Render will read `render.yaml`.
5. Add the secret values when Render asks for environment variables marked `sync: false`:
   - `MAIL_USERNAME`
   - `MAIL_PASSWORD`
   - `MAIL_DEFAULT_SENDER`
   - `MAIL_TO`
6. Deploy.

## Manual Render setup

If you do not use the Blueprint:

- Service type: **Web Service**
- Runtime: **Python**
- Build command: `pip install -r requirements.txt`
- Start command: `gunicorn app:app --workers 1 --threads 8 --timeout 120`
- Health check path: `/health`

Set these environment variables:

```text
SECRET_KEY=<generate a long random value>
BOOKING_LIMIT=20
BOOKING_DATA_PATH=/var/data/bookings.json
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=<your Gmail address>
MAIL_PASSWORD=<your Gmail app password>
MAIL_DEFAULT_SENDER=<your Gmail address>
MAIL_TO=<receiver email address>
```

Add a persistent disk:

```text
Name: booking-data
Mount path: /var/data
Size: 1 GB
```

## Gmail setup

For Gmail SMTP, use a Gmail **App Password**, not your normal Gmail password. The Google account usually needs 2-Step Verification enabled before an App Password can be created.

## Test after deployment

Open these pages on your Render URL:

- `/`
- `/booking`
- `/survey`
- `/event-booking`
- `/faq`
- `/privacy-policy`
- `/health`

Submit one test booking and one survey. Confirm that:

- the success page appears,
- the admin email arrives,
- the booking count persists after redeploy/restart because it writes to `/var/data/bookings.json`.

## Notes

Render's normal service filesystem is ephemeral. Only files under the persistent disk mount path are preserved across deploys and restarts. That is why this project uses `BOOKING_DATA_PATH=/var/data/bookings.json`.
