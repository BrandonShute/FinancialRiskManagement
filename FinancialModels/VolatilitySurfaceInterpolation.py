def volatility_surface_interpolation(volatility_surface, target_maturity, target_strike):
    # volSurface is pandas DataFrame matrix with column labels as percentage of stock prices & row labels as time in years

    # Volatility_Surface_Interpolation(volSurface,1.5,0.015)

    num_rows = volatility_surface.shape[0]
    num_columns = volatility_surface.shape[1]

    row_headers_list = list(volatility_surface.index)
    column_headers_list = list(volatility_surface)

    # Convert row and column headers to floats (if they are string or unicode)
    row_headers = []
    for r in range(len(row_headers_list)):
        row_headers.append(float(row_headers_list[r]))
    column_headers = []
    for c in range(len(column_headers_list)):
        column_headers.append(float(column_headers_list[c]))

    volatility_surface = volatility_surface.as_matrix()

    ###################### Time to Maturity (Row) ############################
    row_id = -1
    for ii in range(0, num_rows - 1):
        if (row_headers[ii] <= target_maturity) & (target_maturity < row_headers[ii + 1]):
            row_id = ii

    if row_id == -1:  # row_id did not change
        if target_maturity == row_headers[-1]:
            row_id = num_rows - 1

    if row_id == -1:  # row_id has not yet changed
        if target_maturity > row_headers[-1]:
            row_id = num_rows - 1

    if row_id == -1:  # row_id has not yet changed
        if target_maturity < row_headers[0]:
            row_id = 0

    ############################ Strike (Column) #############################
    column_id = -1
    for jj in range(0, num_columns - 1):
        if (column_headers[jj] <= target_strike) & (target_strike < column_headers[jj + 1]):
            column_id = jj

    if column_id == -1:  # column_id did not change
        if target_strike == column_headers[-1]:
            column_id = num_columns - 1
            return volatility_surface[
                row_id, column_id]  # simplying assumption if trying to interpolate outside of range of volatility surface

    if column_id == -1:  # column_id did not change
        if target_strike > column_headers[-1]:
            column_id = num_columns - 1
            return volatility_surface[
                row_id, column_id]  # simplying assumption if trying to interpolate outside of range of volatility surface

    if column_id == -1:  # column_id did not change
        if target_strike < column_headers[0]:
            column_id = 0
            return volatility_surface[
                row_id, column_id]  # simplying assumption if trying to interpolate outside of range of volatility surface

    ########################### Bilinear Interpolation #######################

    x1 = volatility_surface[row_id, column_id] + (
            (volatility_surface[row_id, column_id + 1] - volatility_surface[row_id, column_id]) / float(
        (column_headers[column_id + 1] - column_headers[column_id])) * (target_strike - column_headers[column_id]))
    x2 = volatility_surface[row_id + 1, column_id] + (
            (volatility_surface[row_id + 1, column_id + 1] - volatility_surface[row_id + 1, column_id]) / float(
        (column_headers[column_id + 1] - column_headers[column_id])) * (target_strike - column_headers[column_id]))
    x3 = x1 + ((float((x2 - x1))) / (row_headers[row_id + 1] - row_headers[row_id]) * (
            target_maturity - row_headers[row_id]))

    return x3
