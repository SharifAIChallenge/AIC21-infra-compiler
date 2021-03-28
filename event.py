import enum

class Status_Code(enum.Enum):
    # compile status codes
    COMPILE_SUCCESS=100
    COMPILE_FAILED=102
    
    # file transfer status codes
    UPLOAD_FAILED=402
    FILE_NOT_FOUND=404
    
class Event:
    def __init__(self,title,token_id,status_code,message_body=""):
        self.title=title
        self.status_code=status_code
        self.message_body=message_body
        self.token_id=token_id
    