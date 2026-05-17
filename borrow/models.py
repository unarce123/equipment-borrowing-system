from django.db import models
from django.contrib.auth.models import User
from equipment.models import Equipment


class BorrowRequest(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('returned', 'Returned'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    borrow_date = models.DateField()
    return_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    date_requested = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.equipment.name}"

    class Meta:
        verbose_name = "Borrow Request"
        verbose_name_plural = "Borrow Requests"