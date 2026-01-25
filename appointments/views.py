from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required  
from django.contrib import messages
from .models import Patient, Appointment, Doctor
from .forms import PatientForm
from .utils import get_available_slots

@login_required
def dashboard(request):
    # 1. Role
    is_doctor = request.user.is_staff

    # 2. Defaults (VERY IMPORTANT)
    patients = Patient.objects.all()
    appointments = Appointment.objects.none()
    query = request.GET.get('q')

    # 3. Role-based data
    if is_doctor:
        if query:
            patients = Patient.objects.filter(
                name__icontains=query
            ) | Patient.objects.filter(
                phone__icontains=query
            )
        else:
            patients = Patient.objects.all()

        appointments = Appointment.objects.select_related(
            'patient', 'doctor'
        ).order_by('date', 'time')

    else:
        patients = Patient.objects.filter(user=request.user)

        appointments = Appointment.objects.filter(
            patient__user=request.user
        ).select_related('doctor').order_by('date', 'time')

        if query:
            patients = patients.filter(
                name__icontains=query
            ) | patients.filter(
                phone__icontains=query
            )

    # 4. Slot availability
    selected_doctor_id = request.GET.get('doctor_id')
    selected_date = request.GET.get('date')
    slots = []

    if selected_doctor_id and selected_date:
        doctor = get_object_or_404(Doctor, id=selected_doctor_id)
        slots = get_available_slots(doctor, selected_date)

    # 5. Forms
    pform = PatientForm()

    if request.method == 'POST':

        # Add Patient
        if 'add_patient' in request.POST and is_doctor:
            pform = PatientForm(request.POST)
            if pform.is_valid():
                pform.save()
                messages.success(request, "New patient added successfully.")
                return redirect('dashboard')

        # Book Appointment
        elif 'add_appointment' in request.POST:
            p_id = request.POST.get('patient')
            d_id = request.POST.get('doctor')
            date = request.POST.get('date')
            time = request.POST.get('time')

            if p_id and d_id and date and time:
                if Appointment.objects.filter(
                    doctor_id=d_id,
                    date=date,
                    time=time
                ).exists():
                    messages.error(request, "This slot was just taken.")
                else:
                    Appointment.objects.create(
                        patient_id=p_id,
                        doctor_id=d_id,
                        date=date,
                        time=time
                    )
                    messages.success(request, "Appointment confirmed!")
                    return redirect('dashboard')
            else:
                messages.error(request, "Please fill all booking fields.")

    # 6. Context
    context = {
        'is_doctor': is_doctor,
        'patients': patients,
        'doctors': Doctor.objects.all(),
        'appointments': appointments,
        'slots': slots,
        'pform': pform,
        'selected_doctor_id': selected_doctor_id,
        'selected_date': selected_date,
        'query': query,
    }

    return render(request, 'appointments/dashboard.html', context)


@login_required
def appointment_list(request):
    # This view satisfies the redirect in book_appointment
    appointments = Appointment.objects.all()
    return render(request, 'appointment.html', {'appointments': appointments})

@login_required
def edit_patient(request, id):
    # Fetch the patient or return 404 error if not found
    patient = get_object_or_404(Patient, id=id)
    
    if request.method == "POST":
        # Fill the form with new POST data but link it to the existing patient instance
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            messages.success(request, f"Details for {patient.name} updated!")
            return redirect('dashboard')
    else:
        # GET request: Show the form with current patient data
        form = PatientForm(instance=patient)
        
    return render(request, 'appointments/edit.html', {'form': form, 'patient': patient})

@login_required
def delete_patient(request, id):
    patient = get_object_or_404(Patient, id=id)
    patient.delete()
    messages.success(request, "Patient record deleted successfully.")
    return redirect('dashboard')

def home(request):
    """
    Public landing page for the hospital.
    Accessible to all visitors.
    """
    return render(request, 'appointments/home.html')

def about(request):
    """
    Renders the About Us page.
    """
    return render(request, 'appointments/about.html')