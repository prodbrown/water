from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
import uuid

User = get_user_model()


class Bill(models.Model):
    MONTHS = [
        ('January', 'January'), ('February', 'February'), ('March', 'March'),
        ('April', 'April'), ('May', 'May'), ('June', 'June'),
        ('July', 'July'), ('August', 'August'), ('September', 'September'),
        ('October', 'October'), ('November', 'November'), ('December', 'December')
    ]
    STATUS_CHOICES = [
        ('NOT PAID', 'Not Paid'),
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('REJECTED', 'Rejected')  
    ]

    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'is_customer': True},
        related_name='bills_as_customer'
    )
    service_provider = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'is_serviceprovider': True},
        related_name='bills_as_service_provider'
    )
    month = models.CharField(choices=MONTHS, max_length=20)
    year = models.IntegerField(default=timezone.now().year)
    units_used = models.PositiveIntegerField()
    unit_price = models.PositiveIntegerField(default=1500)
    total_amount = models.PositiveIntegerField(editable=False)
    control_number = models.PositiveIntegerField(default='0620709539')
    status = models.CharField(choices=STATUS_CHOICES, max_length=10, default='NOT PAID')
    payment_verification_message = models.TextField(blank=True, null=True)
    payment_verification_screenshot = models.ImageField(upload_to='payment_screenshots/', blank=True, null=True)

    def save(self, *args, **kwargs):
        self.total_amount = self.units_used * self.unit_price
        super().save(*args, **kwargs)

    def generate_control_number(self):
        return str(uuid.uuid4().int)[:12]

    def __str__(self):
        return f'Bill for {self.customer.email} - {self.month} {self.year}'


class Payment(models.Model):
    bill = models.OneToOneField(Bill, on_delete=models.CASCADE)
    payment_date = models.DateTimeField(auto_now_add=True)
    paid_amount = models.PositiveIntegerField()
    verified = models.BooleanField(default=False)  

    def __str__(self):
        return f'Payment for {self.bill}'
