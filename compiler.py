from minio_cli import MinioClient, BucketName
import subprocess
from event import Event, Event_Status
import logging

logging.basicConfig(filename='app.log', filemode='w', format='%(asctime)s - %(levelname)s:%(message)s')


def download_code(code_id, dest) -> bool:
    zip_file = MinioClient.get_file(code_id, BucketName.Code.value)
    if zip_file is None:
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
    logging.info(f'1.receive message with code_id: {code_id}, language: {language}')

    source_file = 'code.zip'
    if not download_code(code_id, source_file):
        return Event(token=code_id, status_code=Event_Status.FILE_NOT_FOUND.value,
                     title='failed to fetch the raw code!')

    logging.info(f'2.download code with code_id: {code_id}, language: {language}')

    if __compile(source_file, language) != 0:
        with open('compile.log', 'r') as logfile:
            return Event(token=code_id, status_code=Event_Status.COMPILE_FAILED.value,
                         title='failed to compile code!', message_body=logfile.read())

    logging.info(f'3.compile code with code_id: {code_id}, language: {language}')

    with open('bin.tgz', 'rb') as compiled:
        if not MinioClient.upload(code_id, compiled, BucketName.Code.value):
            return Event(token=code_id, status_code=Event_Status.UPLOAD_FAILED.value,
                         title='failed to upload the code!')

    return Event(token=code_id, status_code=Event_Status.COMPILE_SUCCESS.value,
                 title='code successfully compiled!')
