"""Task CRUD, ownership checks, search, filtering, and sorting."""
from datetime import date

from flask import abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy import case, or_

from ..extensions import db
from ..models import Task, utcnow
from . import tasks_bp


def owned_task(task_id):
    task = db.session.scalar(db.select(Task).where(Task.id == task_id, Task.user_id == current_user.id))
    if task is None:
        abort(404)
    return task


def task_values(form):
    errors = {}
    title = form.get("title", "").strip()
    description = form.get("description", "").strip()
    subject = form.get("subject", "").strip()
    priority = form.get("priority", "Medium")
    status = form.get("status", "Pending")
    due_raw = form.get("due_date", "").strip()
    if not title or len(title) > 160:
        errors["title"] = "Enter a title between 1 and 160 characters."
    if len(description) > 2000:
        errors["description"] = "Description must be 2,000 characters or fewer."
    if len(subject) > 80:
        errors["subject"] = "Subject must be 80 characters or fewer."
    if priority not in Task.PRIORITIES:
        errors["priority"] = "Choose a valid priority."
    if status not in Task.STATUSES:
        errors["status"] = "Choose a valid status."
    due_date = None
    if due_raw:
        try:
            due_date = date.fromisoformat(due_raw)
        except ValueError:
            errors["due_date"] = "Enter a valid due date."
    return {"title": title, "description": description, "subject": subject,
            "priority": priority, "status": status, "due_date": due_date}, errors


@tasks_bp.get("/")
@login_required
def list_tasks():
    query = db.select(Task).where(Task.user_id == current_user.id)
    search = request.args.get("q", "").strip()[:100]
    status = request.args.get("status", "")
    priority = request.args.get("priority", "")
    subject = request.args.get("subject", "").strip()[:80]
    sort = request.args.get("sort", "due")
    if search:
        pattern = f"%{search}%"
        query = query.where(or_(Task.title.ilike(pattern), Task.description.ilike(pattern)))
    if status in Task.STATUSES:
        query = query.where(Task.status == status)
    else:
        status = ""
    if priority in Task.PRIORITIES:
        query = query.where(Task.priority == priority)
    else:
        priority = ""
    if subject:
        query = query.where(Task.subject.ilike(f"%{subject}%"))
    sort_columns = {
        "due": (Task.due_date.is_(None), Task.due_date.asc(), Task.updated_at.desc()),
        "priority": (case((Task.priority == "High", 3), (Task.priority == "Medium", 2), (Task.priority == "Low", 1), else_=0).desc(), Task.updated_at.desc()),
        "updated": (Task.updated_at.desc(),),
    }
    if sort not in sort_columns:
        sort = "due"
    tasks = db.session.scalars(query.order_by(*sort_columns[sort]).limit(100)).all()
    subjects = db.session.scalars(db.select(Task.subject).where(Task.user_id == current_user.id, Task.subject != "").distinct().order_by(Task.subject)).all()
    return render_template("tasks/list.html", tasks=tasks, filters={"q": search, "status": status, "priority": priority, "subject": subject, "sort": sort}, subjects=subjects)


@tasks_bp.route("/new", methods=["GET", "POST"])
@login_required
def create_task():
    errors, values = {}, {}
    if request.method == "POST":
        values, errors = task_values(request.form)
        if not errors:
            task = Task(user_id=current_user.id, **values)
            if task.status == "Completed":
                task.completed_at = utcnow()
            db.session.add(task)
            db.session.commit()
            flash("Task created.", "success")
            return redirect(url_for("tasks.list_tasks"))
    return render_template("tasks/form.html", task=None, values=values, errors=errors, heading="Add a task")


@tasks_bp.get("/<int:task_id>")
@login_required
def detail(task_id):
    return render_template("tasks/detail.html", task=owned_task(task_id))


@tasks_bp.route("/<int:task_id>/edit", methods=["GET", "POST"])
@login_required
def edit_task(task_id):
    task = owned_task(task_id)
    values, errors = {}, {}
    if request.method == "POST":
        values, errors = task_values(request.form)
        if not errors:
            previous_status = task.status
            for key, value in values.items():
                setattr(task, key, value)
            if task.status == "Completed" and previous_status != "Completed":
                task.completed_at = utcnow()
            elif task.status != "Completed":
                task.completed_at = None
            db.session.commit()
            flash("Task updated.", "success")
            return redirect(url_for("tasks.detail", task_id=task.id))
    return render_template("tasks/form.html", task=task, values=values, errors=errors, heading="Edit task")


@tasks_bp.post("/<int:task_id>/toggle")
@login_required
def toggle_task(task_id):
    task = owned_task(task_id)
    if task.status == "Completed":
        task.status = "Pending"
        task.completed_at = None
    else:
        task.status = "Completed"
        task.completed_at = utcnow()
    db.session.commit()
    flash("Task marked " + task.status.lower() + ".", "success")
    referrer = request.referrer or ""
    return redirect(referrer if referrer.startswith("/") and not referrer.startswith("//") else url_for("tasks.list_tasks"))


@tasks_bp.post("/<int:task_id>/delete")
@login_required
def delete_task(task_id):
    task = owned_task(task_id)
    db.session.delete(task)
    db.session.commit()
    flash("Task deleted.", "success")
    return redirect(url_for("tasks.list_tasks"))
