class Student:
    def __init__(self,name,gender,rank):
        self.name=name
        self.gender=gender
        if self.gender not in ['male','female']:
            raise ValueError('An invalid gender!')
        self.rank=rank
        if not isinstance(self.rank,int) or self.rank<0:
            raise ValueError('An invalid rank!')

    def get_name(self):
        return self.name

    def get_gender(self):
        return self.gender

    def get_rank(self):
        return self.rank

    def introduce(self):
        print('Name: %s, gender: %s, rank: %i'%(self.name,self.gender,int(self.rank)))
        return

Emily=Student('Emily','armed helicopter',6)
Emily.introduce()