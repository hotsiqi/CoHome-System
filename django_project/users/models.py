from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    bank_account_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'


class PaymentProof(models.Model):
    house_unit = models.ForeignKey('HouseUnit', related_name='payments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    proof = models.FileField(upload_to='payment_proofs/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment Proof for {self.house_unit} by {self.user.username}"


HOUSE_TYPE_CHOICES = (
    ('duplex', 'Duplex'),
    ('condominium', 'Condominium'),
    ('bungalow', 'Bungalow'),
    ('apartment', 'Apartment'),
    ('semi_d', 'Semi-D'), 
)


BEDROOM_CHOICES = (
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5+'), 
)


MALAYSIA_STATE_CHOICES = (
    ('JHR', 'Johor'),
    ('KDH', 'Kedah'),
    ('KTN', 'Kelantan'),
    ('MLK', 'Malacca'),
    ('NSN', 'Negeri Sembilan'),
    ('PHG', 'Pahang'),
    ('PRK', 'Perak'),
    ('PLS', 'Perlis'),
    ('PNG', 'Penang'),
    ('SBH', 'Sabah'),
    ('SWK', 'Sarawak'),
    ('SGR', 'Selangor'),
    ('TRG', 'Terengganu'),
    ('KUL', 'Kuala Lumpur'),
    ('LBN', 'Labuan'),
    ('PJY', 'Putrajaya'),
)


class HouseUnit(models.Model):
    STATUS_CHOICES = (
        ('available', 'Available'),
        ('rented', 'Rented Out'),
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    location = models.CharField(max_length=255, choices=MALAYSIA_STATE_CHOICES, default='KUL')
    house_type = models.CharField(max_length=50, choices=HOUSE_TYPE_CHOICES, default='apartment')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    bedrooms = models.IntegerField(choices=BEDROOM_CHOICES, default=1)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available')

    def __str__(self):
        return f"{self.house_type} in {self.location} with {self.bedrooms} bedroom(s)"

class HouseImage(models.Model):
    house = models.ForeignKey(HouseUnit, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='house_images/')

    def __str__(self):
        return f"Image for house {self.house.id} at {self.house.location}"
    

class Contract(models.Model):
    house_unit = models.ForeignKey(HouseUnit, related_name='contracts', on_delete=models.CASCADE)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    contract_file = models.FileField(upload_to='contracts/')
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Contract for {self.house_unit.location} uploaded by {self.uploaded_by.username}"

class TechnicianReport(models.Model):
    technician = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    photo = models.ImageField(upload_to='technician_reports/')
    created_at = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(default=False)

    def str(self):
        return self.title
    
    
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    house_unit = models.ForeignKey(HouseUnit, on_delete=models.CASCADE, related_name='favorited_by')
    added_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'house_unit')  # Prevents duplicate favorites for the same house

    def __str__(self):
        return f"{self.user.username} favorited {self.house_unit.description}"

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    house_unit = models.ForeignKey(HouseUnit, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_date = models.DateTimeField(auto_now_add=True)
    verified_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='verified_transactions')
    verified_at = models.DateTimeField(null=True, blank=True)
    processed = models.BooleanField(default=False)

    def __str__(self):
        return f"Transaction by {self.user.username} for {self.house_unit.description}"


class PaymentProof(models.Model):
    transaction = models.ForeignKey('Transaction', related_name='payment_proofs', on_delete=models.CASCADE, null=True, blank=True)
    proof = models.FileField(upload_to='payment_proofs/')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Payment Proof for {self.transaction.house_unit} by {self.user.username}"



class Notification(models.Model):
    recipient = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f'Notification for {self.recipient.username} - Read: {"Yes" if self.read else "No"}'