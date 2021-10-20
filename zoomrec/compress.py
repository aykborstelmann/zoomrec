import atexit
import logging
import os.path
import signal
import subprocess


def compress(input_filename):
    output_filename = f"{os.path.splitext(input_filename)[0]}.mp4"
    command = f"ffmpeg -i {input_filename} -nostats -vcodec libx265 -crf 28 {output_filename}"
    ffmpeg = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
    atexit.register(os.killpg, os.getpgid(ffmpeg.pid), signal.SIGINT)
    return_code = ffmpeg.wait()
    logging.info(f"ffmpeg finished with return code {return_code}")

    if not return_code:
        return output_filename