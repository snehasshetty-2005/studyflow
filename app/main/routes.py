"""Dashboard and data-backed student task summaries."""
from datetime import date, timedelta

from flask import render_template
from flask_login import current_user, login_required
from ..extensions import db
from ..models import Task
from . import main_bp


@main_bp.get("/")
def index():
    if current_user.is_authenticated:
        from flask import redirect, url_for
        return redirect(url_for("main.dashboard"))
    from flask import redirect, url_for
    return redirect(url_for("auth.login"))


@main_bp.get("/dashboard")
@login_required
def dashboard():
    query = db.select(Task).where(Task.user_id == current_user.id)
    all_tasks = db.session.scalars(query).all()
    counts = {status: sum(t.status == status for t in all_tasks) for status in Task.STATUSES}
    overdue = sum(t.is_overdue for t in all_tasks)
    total = len(all_tasks)
    upcoming = sorted((t for t in all_tasks if t.status != "Completed" and t.due_date), key=lambda t: t.due_date)[:5]
    recent = sorted(all_tasks, key=lambda t: t.updated_at or t.created_at, reverse=True)[:5]
    today = date.today()
    week_start = today - timedelta(days=today.weekday())
    week_counts = []
    for offset in range(7):
        day = week_start + timedelta(days=offset)
        amount = sum(bool(t.completed_at and t.completed_at.date() == day) for t in all_tasks)
        week_counts.append({"label": day.strftime("%a"), "date": day, "count": amount})
    return render_template(
        "main/dashboard.html", total=total, counts=counts, overdue=overdue,
        completion_rate=round(counts["Completed"] / total * 100) if total else 0,
        upcoming=upcoming, recent=recent, week_counts=week_counts,
        week_max=max((d["count"] for d in week_counts), default=0), today=today,
    )
