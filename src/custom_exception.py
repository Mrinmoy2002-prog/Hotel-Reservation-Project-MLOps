import traceback
import sys

class CustomException(Exception): # Need the predefined exception also
    
    def __init__(self,error_message,error_detail:sys):
        super().__init__(error_message)
        self.error_message = self.get_detailed_error_message(error_message,error_detail=error_detail)
        
    @staticmethod      # makes this function independent of the class, no need to define class object for use of this function
    def get_detailed_error_message(error_message,error_detail:sys):
        _,_,exc_tb = error_detail.exc_info() # gives the tuple of error type, error message and stack trace
        file_name = exc_tb.tb_frame.f_code.co_filename # gives the file name where the error occurred
        line_number = exc_tb.tb_lineno # gives the line number where the error occurred
        error_message = f"Error occurred in : [{file_name}] at line number: [{line_number}] with error message: [{error_message}]"
        return error_message
    
    def __str__(self):
        return self.error_message