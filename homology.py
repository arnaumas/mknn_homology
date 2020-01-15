
class HomologyClass():
    def __init__(self, dimension, generators = [], representatives = []):
        self.dimension = dimension
        self.generators = set(generators)
        self.representatives = set(representatives)

    def __repr__(self):
        if len(self.generators) is 0:
            return "H[]"
        else:
            return "H[" + ", ".join([repr(c) for c in self.generators])

    def __str__(self):
        return (f"{self.dimension}-dimensional homology class consisting of the chains: " 
            + repr(self.representatives))
    
    


