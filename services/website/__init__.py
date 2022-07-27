from flask import Blueprint, render_template

from .utils import render_markdown

bp = Blueprint("website", __name__)


@bp.get("/")
def home():
    """Is the home page of the app showing what YouHedge is about"""
    return render_template("home.html")


@bp.get("/privacy-policy")
def privacy_policy():
    """Returns the privacy policy"""
    return render_markdown("PRIVACY_POLICY.md")


@bp.get("/terms-of-service")
def terms_of_service():
    """Returns the terms of service"""
    return render_markdown("TERMS_OF_SERVICE.md")
