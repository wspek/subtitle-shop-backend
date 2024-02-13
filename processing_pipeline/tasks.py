import uuid

import utils.aws as aws
from celery import shared_task
from celery.utils.log import get_task_logger
from download import download_audio
from subtitle import Language, write_transcript_to_srt_file
from transcribe import transcribe

from .models import GeneratedSubtitle

logger = get_task_logger(__name__)


@shared_task
def generate_subtitle_task(youtube_url, output_folder):
    logger.info(f"Generating subtitles for {youtube_url}")

    audio_path = download_audio(url=youtube_url, folder=output_folder)

    transcript_file = transcribe(file_path=audio_path, language=aws.Language.ENGLISH_US, out_folder=output_folder)

    srt_file = write_transcript_to_srt_file(
        transcript_file=transcript_file,
        src_language=Language.ENGLISH,
        out_folder=output_folder,
    )

    with open(srt_file) as f:
        subtitles = f.read()

    # Generate a unique task ID
    task_id = str(uuid.uuid4())

    # Save the subtitles with the task_id
    GeneratedSubtitle.objects.create(task_id=task_id, subtitles=subtitles)

    logger.info("Subtitles generated successfully")

    return task_id
