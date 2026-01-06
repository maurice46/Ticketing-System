from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ticket_service import (
    create_ticket,
    list_tickets,
    get_ticket_by_id,
    update_ticket,
    delete_ticket
)

ticket_bp = Blueprint("tickets", __name__)


@ticket_bp.route("/", methods=["POST"])
@jwt_required()
def create():
    if not request.is_json:
        return {"error": "Request must be JSON"}, 415
    
    creator_id = int(get_jwt_identity())
    data = request.get_json()
    return create_ticket(data, creator_id)


@ticket_bp.route("/all", methods=["GET"])
@jwt_required()
def list_all():
    return list_tickets()


@ticket_bp.route("/<int:ticket_id>", methods=["GET"])
@jwt_required()
def get_one(ticket_id):
    return get_ticket_by_id(ticket_id)


@ticket_bp.route("/<int:ticket_id>", methods=["PATCH"])
@jwt_required()
def update(ticket_id):
    return update_ticket(ticket_id, request.get_json())


@ticket_bp.route("/<int:ticket_id>", methods=["DELETE"])
@jwt_required()
def delete_(ticket_id):
    return delete_ticket(ticket_id)

