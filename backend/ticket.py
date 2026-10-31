from flask import Blueprint, request # groups routes, holds incoming HTTP data
from flask_jwt_extended import jwt_required, get_jwt_identity # login check, who is logged in 
from ticket_service import (
    create_ticket,
    list_tickets,
    get_ticket_by_id,
    update_ticket,
    delete_ticket
)

""" Defines ticket API routes and enforces JWT authentication """

# main.py mounts this blueprint at /api/v1/tickets
ticket_bp = Blueprint("tickets", __name__)

# POST /api/v1/tickets/  -> create a ticket 
@ticket_bp.route("/", methods=["POST"])
@jwt_required() # require valid JWT in Authorization header
def create():
    if not request.is_json:
        return {"error": "Request must be JSON"}, 415
    
    creator_id = int(get_jwt_identity()) # extract user ID from token
    data = request.get_json(silent=True)
    return create_ticket(data, creator_id)


# GET /api/v1/tickets/all  -> your tickets (admin gets everyones)
@ticket_bp.route("/all", methods=["GET"])
@jwt_required()
def list_all():
    user_id = int(get_jwt_identity())
    return list_tickets(user_id) # the service decides what this user may see 


# GET /api/v1/tickets/5  -> one ticket; <int::ticket_id> turns the 5 into an integer argument 
@ticket_bp.route("/<int:ticket_id>", methods=["GET"])
@jwt_required()
def get_one(ticket_id):
    user_id = int(get_jwt_identity())
    return get_ticket_by_id(ticket_id, user_id)


# PATCH /api/v1/tickets/5  -> change only the fields you send (title, description, status)
@ticket_bp.route("/<int:ticket_id>", methods=["PATCH"])
@jwt_required()
def update(ticket_id):
    if not request.is_json:
        return {"error": "Request must be JSON"}, 415
    
    user_id = int(get_jwt_identity())
    data = request.get_json(silent=True)
    return update_ticket(ticket_id, data, user_id)


# DELETE /api/v1/tickets/5  -> remove a ticket
@ticket_bp.route("/<int:ticket_id>", methods=["DELETE"])
@jwt_required()
def delete_(ticket_id): # route function; the logic is in delete_ticket (ticket_service.py)
    user_id = int(get_jwt_identity())
    return delete_ticket(ticket_id, user_id)

