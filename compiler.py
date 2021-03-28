from minio_cli import MinioClient, BucketName
import subprocess

COMPILE_SUCCESS=100
COMPILE_FAILURE=101
class Compiler:

    @staticmethod
    def compile(code_id, language) -> bool:
        print(f'receive message with code_id: {code_id}, language: {language}')

        """ read file from minio """
        zip_file = MinioClient.get_file(code_id, BucketName.Code.value)
        with open('code.zip', 'wb') as f:
            f.write(zip_file)

        cmd = subprocess.Popen(["./compile.sh",f"{language}"],stderr=subprocess.DEVNULL,stdout=subprocess.DEVNULL)
        cmd.communicate()
        if cmd.returncode == 0:
            push_event(code_id,COMPILE_SUCCESS,title='code successfully compiled!')
        else
            with open('compile.log', 'r') as logfile:
                push_event(code_id,COMPILE_FAILURE,title='failed to compile code!',logfile.read())
                return False
        f = open('compiled.zip', 'r')
        file = f.read()
        f.close()

        ''' write in minio '''
        MinioClient.upload(code_id, file, BucketName.Code.value)
        return True
