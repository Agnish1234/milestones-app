from app import app, Milestone

with app.app_context():
    items = Milestone.query.all()
    print(type(items).__name__, len(items))
    if items:
        print(repr(items[0]))
