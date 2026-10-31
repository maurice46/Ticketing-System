from models import db, Ticket, User

"""
CRUD Logic for tickets
Ticket ownership checks: ticket creator or admin user 
"""

def is_owner_or_admin(ticket, user_id): # authorization
    user = User.query.get(user_id)

    if not user: return False

    return ticket.creator_id == user_id or user.role == "admin"

def create_ticket(data, creator_id): # create a ticket 
    if not data or "title" not in data:
        return {"error": "title required"}, 400
    
    ticket = Ticket(
        title=data["title"],
        description=data.get("description"),
        creator_id=creator_id
    )

    db.session.add(ticket)
    db.session.commit()

    return {"id": ticket.id, "title": ticket.title, "creator id": ticket.creator_id}, 201 # 201 = created

def list_tickets(): # read tickets 
    tickets = Ticket.query.all()

    return [{"id": t.id, "title": t.title, "status": t.status, "description" : t.description} 
            for t in tickets]

def get_ticket_by_id(ticket_id, user_id): # read a certain ticket 
    ticket = Ticket.query.get(ticket_id)

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
    ticket = Ticket.query.get(ticket_id)

    if not ticket:
        return {"error": "not found"}, 404
    
    if not is_owner_or_admin(ticket, user_id):
        return {"error": "forbidden"}, 403
    
    ticket.title = data.get("title", ticket.title)
    ticket.description = data.get("description", ticket.description)
    ticket.status = data.get("status", ticket.status)

    db.session.commit()
    return {"message": "updated"}

def delete_ticket(ticket_id, user_id): # delete a certain ticket 
    ticket = Ticket.query.get(ticket_id)

    if not ticket:
        return {"error": "not found"}, 404
    
    if not is_owner_or_admin(ticket, user_id):
        return {"error": "forbidden"}, 403

    db.session.delete(ticket)
    db.session.commit()
    return "", 204 




