from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Equipment(models.Model):

    STATUS_CHOICES = [
        ('available', 'Available'),
        ('borrowed', 'Borrowed'),
        ('damaged', 'Damaged'),
    ]

    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=1)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='available'
    )

    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # --------------------------
    # AUTO SYNC STATUS
    # --------------------------
    def update_status(self):
        if self.status != 'damaged':
            self.status = 'borrowed' if self.quantity <= 0 else 'available'

    def save(self, *args, **kwargs):
        # SAVE FIRST
        super().save(*args, **kwargs)

        # THEN SYNC STATUS
        self.update_status()

        # SAVE UPDATED STATUS ONLY IF NEEDED
        super().save(update_fields=['status'])

    def __str__(self):
        return self.name