from dateutil.relativedelta import relativedelta
import numpy as np


def callable_bond_pricing_function(initial_short_rate, mu, vol, first_coupon_date, coupon_frequency, coupon_rate, face,
                                   call_schedule, call_schedule_exercise_type, val_date, maturity_date):
    num_months = 12. / coupon_frequency

    initial_pmt__after__val_date = first_coupon_date
    while initial_pmt__after__val_date < val_date:
        initial_pmt__after__val_date = initial_pmt__after__val_date + relativedelta(months=int(num_months))

    delta_t_1 = (initial_pmt__after__val_date - val_date).days / 365.
    delta_t_1plus = 1. / coupon_frequency

    # initial_short_rate=0.02
    # mu=0.1
    # vol=0.05
    # CouponRate=10
    # Face=100
    # callSchedule=np.matrix([[datetime.datetime(2016,12,1,0,0),102],[datetime.datetime(2017,12,6,0,0),104]])
    # CallScheduleExerciseType='Bermudan' # Bermudan or American call schedule exercise
    # MaturityDate=dt.datetime(2018,12,1,0,0)
    # ValDate=dt.datetime(2017,6,1,0,0)

    coupon_rate = 1.0 * coupon_rate / coupon_frequency
    coupon_amount = coupon_rate / 100. * face

    n = (maturity_date - val_date).days / 365.  # number of years between valdate and bond maturity
    n = round(n * 2) / 2  # round to nearest 0.5
    num_steps = n / 0.5  # number of steps in interest rate tree
    num_steps = int(num_steps)  # change to integer

    ho__lee__tree = np.zeros(shape=(num_steps, num_steps))
    ho__lee__tree[0, 0] = initial_short_rate

    row_count_1 = 0
    for ii in range(1, num_steps - 1 + 1):
        row_count_1 = row_count_1 + 1
        for jj in range(0, row_count_1 - 1 + 1):
            if (ii == 0) & (jj == 0):
                delta_t = delta_t_1
            else:
                delta_t = delta_t_1plus
            ho__lee__tree[jj, ii] = max(0, ho__lee__tree[jj, ii - 1] + mu * delta_t + vol * pow(delta_t, 0.5))
        ho__lee__tree[ii, ii] = max(0, ho__lee__tree[ii - 1, ii - 1] + mu * delta_t - vol * pow(delta_t, 0.5))
    bond__price__tree = np.zeros(shape=(num_steps + 1, num_steps + 1))
    bond__price__tree[:, -1] = face + coupon_amount

    ###############################################################################
    # Incorporating Call Schedule
    call_schedule_2 = {}
    for ii in range(0, len(call_schedule) - 1 + 1):
        call_schedule_2[int(round((call_schedule[ii, 0] - val_date).days / 365 * 2))] = call_schedule[ii, 1]
    call_schedule_times = set()
    for key in call_schedule_2:
        call_schedule_times.add(key)

    if call_schedule_exercise_type == 'Bermudan':
        # Creating Strike Tree (BERMUDAN)
        strike__tree = np.zeros(shape=(num_steps + 1, num_steps + 1))
        strike__tree[:] = 1e500
        for ii in range(1, len(bond__price__tree) + 1):
            if ii in call_schedule_times:
                strike__tree[:, ii] = call_schedule_2[ii]

    if call_schedule_exercise_type == 'American':
        # Creating Strike Tree (AMERICAN)
        strike__tree = np.zeros(shape=(num_steps + 1, num_steps + 1))
        strike__tree[:] = 1e500
        for ii in range(1, len(bond__price__tree) + 1):
            if ii in call_schedule_times:
                strike__tree[:, ii:] = call_schedule_2[ii]
    ###############################################################################

    row_count_2 = num_steps + 1
    for ii in range(num_steps - 1, -1, -1):  # cycle through columns
        row_count_2 = row_count_2 - 1
        for jj in range(0, row_count_2):  # cycle through rows
            if (ii == 0) & (jj == 0):
                delta_t = delta_t_1
                coupon_amount = 0  # no coupon payment at time 0
            else:
                delta_t = delta_t_1plus
            bond__price__tree[jj, ii] = min(coupon_amount + (
                    (0.5 * bond__price__tree[jj, ii + 1] + 0.5 * bond__price__tree[jj + 1, ii + 1]) / (
                pow((1 + ho__lee__tree[jj, ii]), delta_t))), strike__tree[
                                                jj, ii])  # reflects coupon payment at each node in adddition to discounted bond value at subsequent nodes   # (each node wit prob=0.5)  # this value is compared against  # set-up assumes call will be activated just prior to coupon payment
    bond__price = bond__price__tree[0, 0]

    return bond__price
