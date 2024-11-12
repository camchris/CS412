from django.db import models

# Create your models here.
class Voter(models.Model):
    '''Image class for mini_fb.'''
    last_name = models.TextField(blank=False)
    first_name = models.TextField(blank=False)
    address_streetnum = models.TextField(blank=False)
    address_streetname = models.TextField(blank=False)
    address_aptnum = models.TextField(blank=False)
    address_zip = models.TextField(blank=False)
    birth_date = models.TextField(blank=False)
    registration_date = models.TextField(blank=False)
    party = models.CharField(max_length=6)
    precinct_num = models.TextField(blank=False)

    v20state = models.TextField(blank=False)
    v21town = models.TextField(blank=False)
    v21primary = models.TextField(blank=False)
    v22general = models.TextField(blank=False)
    v23town = models.TextField(blank=False)
    voter_score = models.TextField(blank=False)


    def __str__(self):
        '''Return a string representation of this StatusMessage object.'''
        return f'{self.last_name}, {self.first_name}: {self.party}'
    
def load_data():
    '''Function to load data records from CSV file into Django model instances.'''
    Voter.objects.all().delete()
    filename = '/Users/camillechristie/Desktop/CS412/newton_voters.csv'
    f = open(filename)
    f.readline() # discard headers
    for row in f:
        line = f.readline().strip()
        fields = line.split(',')
        # show which value in each field
                
        # create a new instance of Voter object with this record from CSV
        try:
            voter = Voter(
                            last_name=fields[1].strip(),
                            first_name=fields[2].strip(),
                            address_streetnum = fields[3].strip(),
                            address_streetname = fields[4].strip(),
                            address_aptnum = fields[5].strip(),
                            address_zip = fields[6].strip(),

                            birth_date = fields[7].strip(),
                            registration_date = fields[8].strip(),
                            party = fields[9].strip(),
                            precinct_num = fields[10].strip(),
                        
                            v20state = fields[11].strip(),
                            v21town = fields[12].strip(),
                            v21primary = fields[13].strip(),
                            v22general = fields[14].strip(),
                            v23town = fields[15].strip(),
                            voter_score = fields[16].strip()
                        )
            voter.save()
            print(f'Created voter: {voter}')
        except:
            print(f"Skipped: {fields}")