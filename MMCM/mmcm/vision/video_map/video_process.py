import numpy as np
import cv2

import logging

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


class VideoClipOperator(object):
    def __init__(self) -> None:
        pass

    def __call__(self, *args, **kwds):
        pass


class VSELength(VideoClipOperator):
    def __init__(self, time_start, duration, target, change_length_func) -> None:
        self.time_start = time_start
        self.duration = duration
        self.target = target
        self.change_length_func = change_length_func

    def __call__(self, *args, **kwds):
        return super().__call__(*args, **kwds)


class EditedVideoWriter(object):
    """do operators to videoclip

    Args:
        operators ([[VideoClipOperator,VideoClipOperator], [VideoClipOperator]]):
    """

    def __init__(self, operators):
        self.operators = operators

    def __call__(self, video, out):
        """
        1. open out path
        2. do operator to video, return edited video clip
        3. save

        Args:
            video (_type_): _description_
            out (_type_): _description_
        """
        cap = cv2.VideoCapture(video)
        # Check if camera opened successfully
        if cap.isOpened() == False:
            logger.error("Error opening video stream or file")

        out = cv2.VideoWriter(
            out,
            cv2.VideoWriter_fourcc("M", "J", "P", "G"),
            10,
            (self.width, self.height),
        )
        # float `width`
        for clip_operator in self.operators:
            frames = clip_operator(
                width=cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH),
                height=cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT),
                frame_count=cap.get(cv2.CAP_PROP_FRAME_COUNT),
                fps=cap.get(cv2.cv.CV_CAP_PROP_FPS),
            )
            for frame in frames:
                out.write(frame)
        out.release()
