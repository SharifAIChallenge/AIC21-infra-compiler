from minio_cli import MinioClient, BucketName
import subprocess
from event import Event, Event_Status


def download_code(code_id, dest) -> bool:
    zip_file = MinioClient.get_file(code_id, BucketName.Code.value)
    if zip_file == None:
        return False

    with open(dest, 'wb') as f:
        f.write(zip_file)

    return True


def __compile(source_file, language) -> int:
    cmd = subprocess.Popen(["./compile.sh", source_file,
                            f"{language}"], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
    cmd.communicate()
    return cmd.returncode


def compile(code_id, language) -> Event:
    print(f'receive message with code_id: {code_id}, language: {language}')

    source_file = 'code.zip'
    if download_code(code_id, source_file) == False:
        return Event(token_id=code_id, status_code=Event_Status.FILE_NOT_FOUND, title='failed to fetch the raw code!')

    if __compile(source_file, language) != 0:
        with open('compile.log', 'r') as logfile:
            return Event(token_id=code_id, status_code=Event_Status.COMPILE_FAILED,
                         title='failed to compile code!', message_body=logfile.read())

    with open('bin.zip', 'r') as compiled:
        bin_zip = compiled.read()

    if MinioClient.upload(code_id, bin_zip, BucketName.Code.value) == False:
        return Event(token_id=code_id, status_code=Event_Status.UPLOAD_FAILED, title='failed to upload the code!')

    return Event(token_id=code_id, status_code=Event_Status.COMPILE_SUCCESS,
                 title='code successfully compiled!')
