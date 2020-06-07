class HomDict(dict):
    
    def __init__(self, *args, **kwargs):
        self.aux_dict = {}
        self.update(*args, **kwargs)

    def __setitem__(self, item, value):
        if item not in self:
            # We are adding a new key to the dictionary
            super().__setitem__(item, value)

            if value not in self.aux_dict:
                # We are setting a new value
                self.aux_dict[value] = [item]

            else:
                # There already exist keys with this value
                self.aux_dict[value] += [item]

        else:
            # The key was already in the dictionary
            old_value = self[item]

            if value not in self.aux_dict:
                # We are setting a new value
                self.aux_dict[value] = []

            # Update all the other keys that contained the old value
            for key in self.aux_dict[old_value]:
                self.aux_dict[value].append(key)
                super().__setitem__(key, value)

            del self.aux_dict[old_value]

    def update(self, *args, **kwargs):
        for k , v in dict(*args, **kwargs).items():
            self[k] = v
