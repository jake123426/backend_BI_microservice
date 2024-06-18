from datetime import datetime, date

class DateFormat():   

    date_format = "%d/%m/%Y"
    date_format2 = "%Y-%m-%d"
    
    @classmethod
    def convert_date(self, date):        
        # return datetime.strftime(date, '%d/%m/%Y')
        return datetime.strftime(date, self.date_format2)
        # return datetime.date(2024, 5, 25) # año/mes/dia (genera objeto date con la fecha especificada)
    
    @classmethod
    def stringDate_to_fomattedDate(self, date):        
        return datetime.strptime(date, self.date_format2)
    
    @classmethod
    def generate_date(self):
        # current_date = date.today()
        current_date = datetime.now()        
        return  current_date.strftime(self.date_format2)