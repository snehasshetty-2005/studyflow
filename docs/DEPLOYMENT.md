# Deployment checklist

## Suggested provider combination and status

Suggested for a **portfolio demo with fake data only**: Render Free for the Flask web process and Supabase Free for PostgreSQL. Current official pricing pages show $0 Free plans. This is not a production recommendation. No accounts, services, migrations, or live deployment have been created or verified.

Current plan checks dated 2026-10-19 (recheck before creating resources):

- Render offers free Python web services for hobby and testing projects, not production. They spin down after 15 minutes without inbound activity and take about a minute to wake. Their filesystem is ephemeral, so SQLite cannot persist hosted data. Render currently includes 750 free instance hours per workspace per month. Bandwidth and build pipeline minutes have included limits; exceeding them can suspend service/builds when no payment method is on file, while usage charges may apply if a payment method is added. Free services may be restarted, and Render can suspend services that initiate unusually high volumes of public internet traffic, including database traffic.
- Supabase Free currently lists a 500 MB database, 5 GB egress, 5 GB cached egress, 50,000 monthly active users, and a limit of two active projects. Low-activity Free projects may pause after seven days. Free projects do not include downloadable database backups. Supabase's current billing docs distinguish paid-plan card requirements from Free signup; check the signup flow before provisioning and do not select a paid plan or add paid add-ons.
- Render supports Python 3.13. Its default for a newly created service is now Python 3.14.8, so this project explicitly pins 3.13.16 in `.python-version` and in the Render blueprint. Package compatibility still needs a successful hosted build.

Official sources: [Render free plan](https://render.com/docs/free), [Render Flask deploy](https://render.com/docs/deploy-flask), [Render Python version](https://render.com/docs/python-version), [Supabase pricing](https://supabase.com/pricing), [Supabase project pausing](https://supabase.com/docs/guides/platform/free-project-pausing), [Supabase Postgres connections](https://supabase.com/docs/guides/database/connecting-to-postgres), and [Supabase production checklist](https://supabase.com/docs/guides/deployment/going-into-prod).

## Cost controls and caveats

- Recheck official provider documentation on the day of deployment for eligibility, quotas, runtime/build hours, bandwidth, database storage, backup, card, and overage terms.
- Do not add payment details if maintaining a strict zero-cost cap. Render may suspend services/builds at quota limits when there is no payment method; with a payment method, overage billing can apply.
- Supabase inactivity pause and Render cold starts make this arrangement unsuitable for reliable always-on production traffic. Render free service local files disappear after spin-down/redeploy, so use a remote Postgres database rather than SQLite.
- Prefer default subdomains. Delete the Render service and Supabase project when finished with the demo. Export any data needed before deleting; Supabase Free has no downloadable backups.

## Setup steps (not performed)

1. Create a GitHub repository and push this local Git repository. No GitHub remote is configured yet.
2. Create a Supabase Free project only after checking the signup/payment terms. From the project's **Connect** panel, select the session pooler suitable for a long-running application that needs IPv4, and use its SSL connection string. Adapt the scheme to `postgresql+psycopg://` for the installed driver and keep the credential private. Supabase documents `sslmode=require` for encrypted connections and CA certificate verification for the stronger `verify-full` mode.
3. The reviewed initial Alembic migration is already in `migrations/versions/`; commit the complete `migrations/` directory with the source.
4. In Render, choose **New > Blueprint** and connect the GitHub repository. Render reads `render.yaml`, which defines the free Python web service, health check, WSGI command, and build-time database migration. The first blueprint setup prompts for `DATABASE_URL`; provide the Supabase pooler URL with the scheme changed to `postgresql+psycopg://`. Keep it private. Render generates `SECRET_KEY` securely. Do not add a payment method or select paid resources if maintaining a strict zero-cost target.
5. The blueprint sets `COOKIE_SECURE=1` and `FLASK_DEBUG=0`. Confirm all variables in Render's private environment settings before the first build. Never paste credentials into chat or commit them.
6. Verify HTTPS, registration, sign-in/out, task create/edit/complete/delete, owner isolation, and persistence after a service restart. Test the cold-start path after the service sleeps. Use only fake demo data.
7. Monitor Render/Supabase quotas and pause status. Export data if needed, then delete both hosted resources when finished.

These steps have not been performed. A local Git repository is initialized, but no GitHub remote, provider account, cloud resource, or live deployment is configured. Exact runtime compatibility, account signup terms, live database connection, and quota behavior must be verified in the provider dashboards before claiming deployment.
