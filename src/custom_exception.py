import traceback
import sys

class CustomException(Exception): # Need the predefined exception also
    
    def __init__(self,error_message,error_detail:sys):
        super().__init__(error_message)
        self.error_message = self.add_n
        
    @staticmethod      # makes this function independent of the class, no need to define class object for use of this function
    def get_detailed_error_message(error_message,error_detail:sys):
        
    