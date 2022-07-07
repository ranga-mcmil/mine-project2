from django.db import models
from django.conf import settings
from django.utils import timezone
from accounts.models import User


class ForfeitedManager(models.Manager):
    def get_queryset(self):
        return super(ForfeitedManager,
                     self).get_queryset() \
            .filter(status='forfeit')


class PendingApprovalManager(models.Manager):
    def get_queryset(self):
        return super(PendingApprovalManager,
                     self).get_queryset() \
            .filter(status='pending_approval')


class ActiveManager(models.Manager):
    def get_queryset(self):
        return super(ActiveManager,
                     self).get_queryset() \
            .filter(status='active')


# # Create your models here.
# class Mine(models.Model):
#     user = models.OneToOneField(User, related_name='mine', on_delete=models.CASCADE)
#     name = models.CharField(max_length=250)
#     created = models.DateTimeField(default=timezone.now)
#     balance = models.CharField(max_length=250)
#
#     class Meta:
#         ordering = ('-name',)
#
#     def __str__(self):
#         return self.name


class Claim(models.Model):
    STATUS_CHOICES = (
        ('pending_approval', 'Pending Approval'),
        ('forfeit', 'Forfeited'),
        ('active', 'Active')
    )
    applicant = models.ForeignKey(User, related_name='claims', on_delete=models.CASCADE)
    location = models.CharField(max_length=250)
    address = models.CharField(max_length=250)
    size_approximation = models.CharField(max_length=250)
    date_applied = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=30,
                              choices=STATUS_CHOICES,
                              default='pending_approval')
    created = models.DateTimeField(default=timezone.now)
    objects = models.Manager()  # The default manager.
    forfeited = ForfeitedManager()  # Our custom manager.
    pending_approval = PendingApprovalManager()  # Our custom manager.
    active = ActiveManager()  # Our custom manager.

    class Meta:
        ordering = ('-created',)


class Proof(models.Model):
    image = models.ImageField(upload_to='images', blank=True)
    uploaded_by = models.ForeignKey(User, related_name='proof_of_payment', on_delete=models.CASCADE)
    is_processeed = models.BooleanField(default=False)
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ('-created',)


class Payment(models.Model):
    amount = models.CharField(max_length=250)
    reason = models.CharField(max_length=250)
    user = models.ForeignKey(User, related_name='payments', on_delete=models.CASCADE, null=True)
    proof = models.ForeignKey(Proof, related_name='payment', on_delete=models.CASCADE, null=True)
    is_processeed = models.BooleanField(default=False)
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ('-created',)