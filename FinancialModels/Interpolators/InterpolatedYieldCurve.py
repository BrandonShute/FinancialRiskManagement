# TODO: This method should be added to the BlackVolatilitySurface when it's created
def interpolated_yield_curve(input_yield_curve, payment_timing):
    # The inputted yield curve will be a pandas dataframe with row of terms and corresponding row of rates.
    # We assume the yield curve will be generic, i.e. the key rates for certain curves will be different from others.
    # "Payment Timing" is a list of times (in years) representing timing of payments.
    valuation__curve = []

    key_rate_list = list(input_yield_curve)

    # Convert the key rates to floats (if they are string or unicode)
    key_rates = []
    for k in range(len(key_rate_list)):
        key_rates.append(float(key_rate_list[k]))

    input_yield_curve = [k for k in input_yield_curve.iloc[0,
                                    :]]  # change pandas DataFrame to list

    for ii in range(len(payment_timing)):

        if payment_timing[ii] <= key_rates[0]:
            valuation__curve.append(input_yield_curve[0])

        if (payment_timing[ii] > key_rates[0]) & (
                payment_timing[ii] < key_rates[-1]):
            jj = 0
            while payment_timing[ii] > key_rates[jj]:
                jj = jj + 1
            valuation__curve.append(input_yield_curve[jj - 1] + (
                    input_yield_curve[jj] - input_yield_curve[jj - 1]) / (
                                            key_rates[jj] - key_rates[
                                        jj - 1]) * (
                                            payment_timing[ii] - key_rates[
                                        jj - 1]))

        # if payment date exceeds last key rate, then set yield to last key rate yield
        if payment_timing[ii] >= key_rates[-1]:

            valuation__curve.append(input_yield_curve[-1])

    return valuation__curve
