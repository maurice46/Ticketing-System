from models import db, Ticket, User

"""
CRUD Logic for tickets
Ticket ownership checks: ticket creator or admin user 
"""

VALID_STATUSES = {"open", "in_progress", "closed"}
MAX_TITLE_LEN = 120

def _is_admin(user):
    return user is not None and user.role == "admin"


def is_owner_or_admin(ticket, user_id): # authorization
    user = db.session.get(User, user_id) # dont do "User.query.get(user_id)""

    if not user: return False

    return ticket.creator_id == user_id or _is_admin(user)


def _validate_title(title): # return (clean_title, error_message)
    if not isinstance(title, str):
        return None, "title must be a string"
    
    title = title.strip()

    if not title:
        return None, "title required"

    if len(title) > MAX_TITLE_LEN:
        return None, f"title must be at most {MAX_TITLE_LEN} characters"

    return title, None


def _validate_description(description):
    if description is not None and not isinstance(description, str):
        return "description must be a string"
    return None



def create_ticket(data, creator_id): # create a ticket 
    if not isinstance(data, dict) or "title" not in data:
        return {"error": "title required"}, 400

    title, error = _validate_title(data['title'])

    if error:
        return {"error": error}, 400

    description = data.get("description")
    error = _validate_description(description)

    if error:
        return {"error": error}, 400
    
    ticket = Ticket(title=title, description=description, creator_id=creator_id)

    db.session.add(ticket)
    db.session.commit()

    return {"id": ticket.id, "title": ticket.title, "creator id": ticket.creator_id}, 201 # 201 = created



def list_tickets(user_id): # read tickets 
    user = db.session.get(User, user_id)

    if _is_admin(user):
        tickets = Ticket.query.all()
    else:
        tickets = Ticket.query.filter_by(creator_id=user_id).all()

    return [{"id": t.id, "title": t.title, "status": t.status, 
             "description" : t.description, "creator_id": t.creator_id} 
            for t in tickets], 200



def get_ticket_by_id(ticket_id, user_id): # read a certain ticket 
    ticket = db.session.get(Ticket, ticket_id)

    if not ticket:
        return {"error": "not found"}, 404

    if not is_owner_or_admin(ticket, user_id):
        return {"error": "forbidden"}, 403

    return {"id": ticket.id, 
            "title": ticket.title, 
            "description": ticket.description,
            "status": ticket.status, 
            "creator_id": ticket.creator_id}



def update_ticket(ticket_id, data, user_id): # update a certain ticket 
    ticket = db.session.get(Ticket, ticket_id)

    if not ticket:
        return {"error": "not found"}, 404
    
    if not is_owner_or_admin(ticket, user_id):
        return {"error": "forbidden"}, 403

    if not isinstance(data, dict):
        return {"error": "JSON object body required"}, 400

    # update title 
    if "title" in data:
        title, error = _validate_title(data['title'])
        if error: return {"error": error}, 400
        ticket.title = title

    # update description
    if "description" in data:
        error = _validate_description(data['description'])
        if error: return {"error": error}, 400
        ticket.description = data['description']
    
    # update status
    if "status" in data:
        if data['status'] not in VALID_STATUSES:
            return {"error": f"status must be one of: {', '.join(sorted(VALID_STATUSES))}"}, 400
        ticket.status = data['status']

    db.session.commit()
    return {"message": "updated"}



def delete_ticket(ticket_id, user_id): # delete a certain ticket 
    ticket = db.session.get(Ticket, ticket_id)

    if not ticket:
        return {"error": "not found"}, 404
    
    if not is_owner_or_admin(ticket, user_id):
        return {"error": "forbidden"}, 403

    db.session.delete(ticket)
    db.session.commit()
    return "", 204 




