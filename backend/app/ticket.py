from flask import Blueprint, request
from .ticket_service import (
    create_ticket,
    list_tickets,
    get_ticket_by_id,
    update_ticket,
    delete_ticket
)

ticket_bp = Blueprint("tickets", __name__)

@ticket_bp.route("/", methods=["POST"])
def create():
    return create_ticket(request.get_json())

@ticket_bp.route("/all", methods=["GET"])
def list_all():
    return list_tickets()

@ticket_bp.route("/<int:ticket_id>", methods=["GET"])
def get_one(ticket_id):
    return get_ticket_by_id(ticket_id)

@ticket_bp.route("/<int:ticket_id>", methods=["PATCH"])
def update(ticket_id):
    return update_ticket(ticket_id, request.get_json())

@ticket_bp.route("/<int:ticket_id>", methods=["DELETE"])
def delete_(ticket_id):
    return delete_ticket(ticket_id)

