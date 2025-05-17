import logging
from datetime import datetime

logger = logging.getLogger(__name__)


def clean(raw_data):
    aide_data = []
    seen_aides = set()
    shift_data = []
    for data in raw_data:
        # aide data gets separated
        pa_name = data.pop("pa_name")
        pa_ppl_id = data.pop("pa_ppl_id")
        if pa_ppl_id not in seen_aides:
            aide_data.append((pa_ppl_id, pa_name))
        seen_aides.add(pa_ppl_id)

        # shift data logic
        service_date = data.pop("service_date")
        time_in = data.pop("time_in")
        time_out = data.pop("time_out")
        # payroll_st_date = data.pop("payroll_start_date")
        # payroll_end_date = data.pop("payroll_end_date")
        status = data.pop("status")

        # time in
        combined_str = f"{service_date} {time_in}"
        time_in_dt = datetime.strptime(combined_str, "%m/%d/%Y %I:%M %p")

        # time out
        combined_str = f"{service_date} {time_out}"
        time_out_dt = datetime.strptime(combined_str, "%m/%d/%Y %I:%M %p")

        # payroll period
        # payroll_period = payroll_st_date + " - " + payroll_end_date

        # in database entry order
        shift_data.append((pa_ppl_id, time_in_dt, time_out_dt, status))

    return aide_data, shift_data
