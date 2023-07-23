from ..extensions import db

class Wine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    notes = db.Column(db.String(100))
    country = db.Column(db.String(52))
    region = db.Column(db.String(52))
    grape = db.Column(db.String(52))
    abv = db.Column(db.Float())    
    
    @property
    def new_or_old_world(self):
        old_world = [
            'france',
            'italy',
            'portugal',
            'spain',
            'germany'
        ]

        new_world = [
            'chile',
            'new zealand',
            'south africa',
            'china',
        ]

        if self.country.lower() in old_world:
            return 'old world'
        elif self.country.lower() in new_world:
            return 'new world'
        else:
            return None
    
    def __repr__(self):
        return f'{self.name}, {self.grape}'

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "notes": self.notes,
            "region": self.region,
            "country": self.country,
            "abv": f"{float(self.abv)}%",
        }
    
        
