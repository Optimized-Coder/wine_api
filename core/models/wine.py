from ..extensions import db

class Wine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    color = db.Column(db.String(24))
    notes = db.Column(db.String(255))
    country = db.Column(db.String(52))
    region = db.Column(db.String(52))
    grape = db.Column(db.String(52))
    abv = db.Column(db.Float())  
    vintage = db.Column(db.Integer)  
    
    @property
    def new_or_old_world(self):
        old_world = [
            'france',
            'italy',
            'portugal',
            'spain',
            'germany',
            'greece',
            'hungary',
            'romania',
            'bulgaria'
        ]

        new_world = [
            'chile',
            'new zealand',
            'south africa',
            'china',
            'australia',
            'usa',
            'argentina',
            'canada',
            'brazil',
            'china',
            'uruguay'
        ]

        if self.country.lower() in old_world:
            return 'old world'
        elif self.country.lower() in new_world:
            return 'new world'
        else:
            return None
        
    @property
    def generate_description(self):
        return f"This {self.color} wine from {self.country.title()} is a lovely {self.grape.title()}. Its notes include {self.notes}. Its abv is {self.abv}%."
    
    @property
    def notes_list(self):
        notes = self.notes.split(', ')
        return notes
    
    def __repr__(self):
        return f'{self.name}, {self.grape}'
    
    def calculate_similarity_score(self, wine):
        similarity_score = 0
        for note in wine.notes_list:
            if note in self.notes_list:
                similarity_score += 2

        if wine.country.lower() == self.country.lower():
            similarity_score += 4

        if wine.color.lower() == self.color.lower():
            similarity_score += 6

        if wine.grape.lower() == self.grape.lower():
            similarity_score += 5
        
        if wine.region.lower() == self.region.lower():
            similarity_score += 6

        return similarity_score
    
    @property
    def similar_wines(self):
        wines = Wine.query.all()
        scores = []
        for wine in wines:
            if wine.id == self.id:
                continue

            score = self.calculate_similarity_score(wine)
            scores.append({f'{wine.name.title()}, {wine.grape.title()}': score})
        return scores
    
    
    @property
    def sorted_similar_wines(self):
        sorted_data = sorted(self.similar_wines, key=lambda x: list(x.values())[0], reverse=True)
        return sorted_data[:4]

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "notes": self.notes,
            "notes_list": self.notes_list,
            "region": self.region,
            "country": self.country,
            "abv": f"{float(self.abv)}%",
            "color": self.color,
            "grape": self.grape,
            "new_or_old_world": self.new_or_old_world,
            "similar_wines": self.sorted_similar_wines,
            "vintage": self.vintage
            # "description": self.generate_description
        }
    

            
class Notes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
