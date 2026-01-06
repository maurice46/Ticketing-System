from models import db, Ticket

# create 
def create_ticket(data):
    ticket = Ticket(
        title=data["title"],
        description=data.get("description")
    )
    db.session.add(ticket)
    db.session.commit()
    return {"id": ticket.id, "title": ticket.title}, 201 # 201 -> created

# read 
def list_tickets():
    tickets = Ticket.query.all()
    return [{"id": t.id, "title": t.title, "status": t.status} for t in tickets]

def get_ticket_by_id(ticket_id):
    ticket = Ticket.query.get(ticket_id)
    if not ticket:
        return {"error": "not found"}, 404
    return {"id": ticket.id, "title": ticket.title}

# update 
def update_ticket(ticket_id, data):
    ticket = Ticket()

# delete
def delete_ticket(ticket_id):
    pass


