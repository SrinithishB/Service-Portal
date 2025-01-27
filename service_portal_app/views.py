from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.timezone import now
from .models import ServiceRequest, ServiceRequestImage, Quote
from users.models import Location


# Create your views here.
def index(request):
    return render(request, 'service_portal_app/index.html')


@login_required
def cust_dash(request):
    locations = Location.objects.all()
    service_requests = ServiceRequest.objects.filter(
        customer=request.user.profile,  # Fetch requests specific to the logged-in customer
        status__in=['Pending', 'Accepted']
    )
    if request.method == 'POST':
        description = request.POST.get('description')
        location_id = request.POST.get('location')
        location = Location.objects.filter(location_id=location_id).first()
        images = request.FILES.getlist('images')  # List of uploaded images

        if not description:
            messages.error(request, "Description is required.")
            return render(request, 'service_portal_app/cust_dashboard.html', {'locations': locations})

        # Create the service request
        service_request = ServiceRequest.objects.create(
            customer=request.user.profile,
            description=description,
            location=location,
            status='Pending'
        )

        # Save the uploaded images
        for image in images:
            ServiceRequestImage.objects.create(service_request=service_request, image=image)

        messages.success(request, 'Your service request has been created successfully!')
        return redirect('Service Portal:customer')

    return render(request, 'service_portal_app/cust_dashboard.html', {
        'locations': locations,
        'service_requests': service_requests
    })


@login_required
def serv_dash(request):
    service_requests = ServiceRequest.objects.filter(
        location=request.user.profile.location,
        status='Pending'
    ).exclude(
        quotes__provider=request.user  # Exclude requests with quotes from the current user
    )
    bids = Quote.objects.filter(provider=request.user).select_related('service_request').order_by('-created_at')
    return render(request, 'service_portal_app/service_provider_dashboard.html', {
        'service_requests': service_requests,'bids': bids
    })


@login_required
def request_details(request, pk):
    service_request = get_object_or_404(ServiceRequest, request_id=pk)

    # Check if the user is authorized to view the request
    if request.user.profile != service_request.customer:
        messages.error(request, "You are not authorized to view this request.")
        return redirect('Service Portal:index')

    quotes = service_request.quotes.all()
    return render(request, 'service_portal_app/request_details.html', {
        'service_request': service_request,
        'quotes': quotes
    })


@login_required
def cancel_request(request, request_id):
    service_request = get_object_or_404(ServiceRequest, request_id=request_id)

    # Check if the logged-in user is the owner of the request
    if request.user.profile != service_request.customer:
        messages.error(request, "You are not authorized to cancel this request.")
        return redirect('Service Portal:cust_dash')

    # Mark the request as canceled
    if service_request.status == 'Pending':
        service_request.status = 'Canceled'
        service_request.save()
        messages.success(request, "Request has been canceled successfully.")
    else:
        messages.error(request, "You can only cancel pending requests.")

    return redirect('Service Portal:customer')


@login_required
def accept_quote(request, quote_id):
    quote = get_object_or_404(Quote, quote_id=quote_id)
    service_request = quote.service_request

    # Ensure the user is the owner of the service request
    if request.user.profile != service_request.customer:
        messages.error(request, "You are not authorized to accept quotes for this request.")
        return redirect('service_portal_app:request_details', pk=service_request.request_id)

    # Ensure the service request is still pending
    if service_request.status != 'Pending':
        messages.error(request, "You can only accept quotes for pending requests.")
        return redirect('service_portal_app:request_details', pk=service_request.request_id)

    # Mark the service request as accepted and link the accepted quote
    service_request.status = 'Accepted'
    service_request.accepted_quote = quote
    service_request.save()

    # Cancel all other quotes related to the service request
    service_request.quotes.exclude(quote_id=quote_id).update(status='Canceled')

    messages.success(request, "Quote has been accepted successfully, and all other quotes have been canceled.")
    return redirect('Service Portal:request_details', pk=service_request.request_id)


@login_required
def quote_submission(request, pk):
    service_request = get_object_or_404(ServiceRequest, request_id=pk)
    existing_quote = Quote.objects.filter(service_request=service_request, provider=request.user).first()

    # if existing_quote:
    #     messages.error(request, "You have already submitted a quote for this request.")
    #     return redirect('Service Portal:request_details', pk=pk)
    # Ensure the user is a service provider and not the owner of the request
    if request.user.profile == service_request.customer:
        messages.error(request, "You cannot submit a quote for your own request.")
        return redirect('Service Portal:service')

    if request.method == "POST":
        price = request.POST.get('price')
        comments = request.POST.get('comments', '')
        availability_date = request.POST.get('availability_date')

        # Create a new quote
        Quote.objects.create(
            service_request=service_request,
            provider=request.user,
            price=price,
            comment=comments,
            availability_date=availability_date,
            created_at=now(),
        )
        messages.success(request, "Your quote has been submitted successfully.")
        return redirect('Service Portal:provider')
    has_submitted_quote = service_request.quotes.filter(provider=request.user).exists()

    context = {
        "service_request": service_request,
        "has_submitted_quote": has_submitted_quote,
    }
    return render(request, "service_portal_app/quote_submission.html", context)


@login_required
def my_requests(request):
    # Fetch service requests for the logged-in user
    service_requests = ServiceRequest.objects.filter(customer=request.user.profile).order_by('-created_at')

    # Render the template with the service requests
    return render(request, 'service_portal_app/my_request.html', {
        'service_requests': service_requests
    })

@login_required
def my_bids(request):
    # Fetch quotes submitted by the logged-in user
    bids = Quote.objects.filter(provider=request.user).select_related('service_request').order_by('-created_at')

    # Render the template with the quotes
    return render(request, 'service_portal_app/my_bids.html', {
        'bids': bids
    })

def mark_completed(request, request_id):
    # Fetch the service request
    service_request = get_object_or_404(ServiceRequest, request_id=request_id)

    # Ensure the request status is 'Accepted' before completing
    if service_request.status == 'Accepted':
        service_request.status = 'Completed'
        service_request.save()
        
        # Redirect to the quote_submission page
    return redirect(reverse('Service Portal:quote_submission', kwargs={'pk': request_id}))

    return HttpResponse("Service request cannot be marked as completed.", status=400)