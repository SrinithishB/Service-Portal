# from django.db import models
# from users.models import Profile,Location  # Replace profile_app with the actual app name
# from django.contrib.auth.models import User


# class ServiceRequest(models.Model):
#     STATUS_CHOICES = [
#         ('Pending', 'Pending'),
#         ('Canceled', 'Canceled'),
#         ('Accepted', 'Accepted'),
#     ]

#     request_id = models.AutoField(primary_key=True)
#     customer = models.ForeignKey(
#         Profile, 
#         on_delete=models.CASCADE, 
#         related_name='service_requests',
#         limit_choices_to={'user_type': 'Customer'}
#     )
#     description = models.TextField()
#     location = models.ForeignKey(
#         Location, 
#         on_delete=models.SET_NULL, 
#         null=True, 
#         related_name='service_requests'
#     )
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Request {self.request_id} by {self.customer.name} - {self.status}"

#     class Meta:
#         verbose_name = "Service Request"
#         verbose_name_plural = "Service Requests"
#         ordering = ['-created_at']


# class ServiceRequestImage(models.Model):
#     service_request = models.ForeignKey(
#         ServiceRequest, 
#         on_delete=models.CASCADE, 
#         related_name='images'
#     )
#     image = models.ImageField(upload_to='service_requests/images/')
#     uploaded_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Image for Request {self.service_request.request_id}"


# class Quote(models.Model):
#     quote_id = models.AutoField(primary_key=True)
#     service_request = models.ForeignKey(
#         ServiceRequest, on_delete=models.CASCADE, related_name="quotes"
#     )
#     provider = models.ForeignKey(
#         User, on_delete=models.CASCADE, related_name="submitted_quotes"
#     )
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     comment = models.TextField(blank=True, null=True)
#     availability_date = models.DateField(null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Quote {self.quote_id} by {self.provider.username} for Request {self.service_request.request_id}"

#     class Meta:
#         verbose_name = "Quote"
#         verbose_name_plural = "Quotes"
#         ordering = ['-created_at']

from django.db import models
from users.models import Profile, Location  # Replace with the actual app name
from django.contrib.auth.models import User


class ServiceRequest(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Canceled', 'Canceled'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
    ]

    request_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='service_requests',
        limit_choices_to={'user_type': 'Customer'}
    )
    description = models.TextField()
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        related_name='service_requests'
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    accepted_quote = models.OneToOneField(
        'Quote',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='accepted_request'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.accepted_quote:
            return f"Request {self.request_id} (Accepted Quote: {self.accepted_quote.quote_id})"
        return f"Request {self.request_id} by {self.customer.name} - {self.status}"

    class Meta:
        verbose_name = "Service Request"
        verbose_name_plural = "Service Requests"
        ordering = ['-created_at']


class ServiceRequestImage(models.Model):
    service_request = models.ForeignKey(
        ServiceRequest,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to='service_requests/images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for Request {self.service_request.request_id}"


class Quote(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Canceled', 'Canceled'),
        ('Completed', 'Completed'),
    ]
    quote_id = models.AutoField(primary_key=True)
    service_request = models.ForeignKey(
        ServiceRequest,
        on_delete=models.CASCADE,
        related_name="quotes"
    )
    provider = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="submitted_quotes"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    comment = models.TextField(blank=True, null=True)
    availability_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"Quote {self.quote_id} by {self.provider.username} for Request {self.service_request.request_id}"

    class Meta:
        verbose_name = "Quote"
        verbose_name_plural = "Quotes"
        ordering = ['-created_at']
