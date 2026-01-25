from datetime import datetime, timedelta
from .models import Appointment

def get_available_slots(doctor, date):
    # Define hospital hours: 9:00 AM to 5:00 PM
    start_time = datetime.strptime("09:00", "%H:%M")
    end_time = datetime.strptime("17:00", "%H:%M")
    slot_duration = timedelta(minutes=30)

    slots = []
    current_time = start_time

    # Fetch all booked times for this doctor on this day
    booked_times = Appointment.objects.filter(doctor=doctor, date=date).values_list('time', flat=True)

    while current_time < end_time:
        time_str = current_time.strftime("%H:%M")
        # Check if the time slot exists in booked_times
        is_booked = any(bt.strftime("%H:%M") == time_str for bt in booked_times)
        
        slots.append({
            'time': time_str,
            'available': not is_booked
        })
        current_time += slot_duration
        
    return slots