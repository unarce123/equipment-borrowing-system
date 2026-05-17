from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


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

    def update_status(self):
        if self.status != 'damaged':
            self.status = 'borrowed' if self.quantity <= 0 else 'available'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.update_status()
        super().save(update_fields=['status'])

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Equipment"
        verbose_name_plural = "Equipment Items"