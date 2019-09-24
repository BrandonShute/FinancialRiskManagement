import datetime

DAY_STRINGS = ['d', 'day', 'days']
WEEK_STRINGS = ['w', 'week', 'weeks']
MONTH_STRINGS = ['m', 'month', 'months']
YEAR_STRINGS = ['y', 'year', 'years']
TENOR_START_CHARS = ['d', 'w', 'm', 'y']


class Tenor(object):
    """Tenors class for Financial Data."""

    def __init__(self, tenor_string):
        self.tenor_string = tenor_string
        self.reference_date = datetime.date.today()
        self.offset = self.get_offset_from_tenor_string()
        self.offset_type = self.get_offset_type_from_tenor_string()
        self.associated_date = self.get_associated_date()

    def __init__(self, tenor_string, reference_date):
        self.tenor_string = tenor_string
        self.reference_date = reference_date
        self.offset = self.get_offset_from_tenor_string()
        self.offset_type = self.get_offset_type_from_tenor_string()
        self.associated_date = self.get_associated_date()

    def __init__(self, offset, offset_type):
        self.offset = offset
        self.offset_type = offset_type
        self.reference_date = datetime.date.today()
        self.tenor_string = self.get_tenor_string_from_offset()
        self.associated_date = self.get_associated_date()

    def __init__(self, offset, offset_type, reference_date):
        self.offset = offset
        self.offset_type = offset_type
        self.reference_date = reference_date
        self.tenor_string = self.get_tenor_string_from_offset()
        self.associated_date = self.get_associated_date()

    def get_tenor_string_from_offset(self):
        return str(self.offset) + self.offset_type

    # TODO: Clearly needs to be fixed with validation
    def get_offset_from_tenor_string(self):
        for char in TENOR_START_CHARS:
            if char in self.tenor_string:
                offset_type_index = self.tenor_string.find(char)
                return self.tenor_string[:offset_type_index]

    # TODO: Clearly needs to be fixed with validation
    def get_offset_type_from_tenor_string(self):
        for char in TENOR_START_CHARS:
            if char in self.tenor_string:
                offset_type_index = self.tenor_string.find(char)
                return self.tenor_string[offset_type_index:offset_type_index + 1]


    # TODO: Add validation to final else
    def get_associated_date(self):
        if DAY_STRINGS.contains(self.offset_type):
            associated_date = self.reference_date + datetime.timedelta(
                days=self.offset)
        elif WEEK_STRINGS.contains(self.ofset_type):
            associated_date = self.reference_date + datetime.timedelta(
                weeks=self.offset)
        elif MONTH_STRINGS.contains(self.ofset_type):
            associated_date = self.reference_date + datetime.timedelta(
                months=self.offset)
        elif YEAR_STRINGS.contains(self.ofset_type):
            associated_date = self.reference_date + datetime.timedelta(
                years=self.offset)

        return associated_date

    # TODO Consider moving validation to a MarketData Validation class??
    @staticmethod
    def validate_tenor_string(tenor_string):
        if any(char in tenor_string for char in TENOR_START_CHARS):
            return True
        else:
            return False
