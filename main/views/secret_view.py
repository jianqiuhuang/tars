"""Secret view: executes backend code and displays results"""
import io
import sys
from django.shortcuts import render
from ..utils.mta_bus import run_all_bus_checks


def secret_view(request):
    """Page that executes backend code and displays results"""
    # Capture stdout
    output = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = output
    
    try:
        # Run the MTA bus checks
        run_all_bus_checks(output_func=print)
    finally:
        # Restore stdout and get the output
        sys.stdout = old_stdout
        result = output.getvalue()
    
    context = {
        'result': result,
    }
    return render(request, 'main/secret.html', context)

