from Interpolators.BilinearInterpolation import BilinearInterpolation


# TODO: This method should be added to the BlackVolatilitySurface when it's created
def volatility_surface_interpolation(volatility_surface, target_maturity,
                                     target_strike, interp_method):
    # Convert row and column headers to floats (if they are string or unicode)
    maturities = [float(i) for i in list(volatility_surface.index)]
    strike_as_percentages = [float(i) for i in list(volatility_surface)]
    volatility_surface = volatility_surface.as_matrix()

    # TODO: Add other types of interpolation methods
    if interp_method.lower() == 'bilinearinterpolation':
        interpolator = BilinearInterpolation(maturities, strike_as_percentages,
                                             volatility_surface)

    return interpolator(target_maturity, target_strike)
