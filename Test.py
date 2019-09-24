import QuantLib as ql

start_date = ql.Date(1, 1, 2015)
end_date = ql.Date(1, 1, 2016)
tenor = ql.Period(ql.Monthly)
calendar = ql.UnitedStates()
schedule = ql.Schedule(start_date, end_date, tenor, calendar, ql.Following,
                           ql.Following, ql.DateGeneration.Forward, False)
print(list(schedule))


annualRate = 0.05
dayCount = ql.ActualActual()
compoundType = ql.Compounded
frequency = ql.Annual
interestRate = ql.InterestRate(annualRate, dayCount, compoundType, frequency)

print(interestRate)

