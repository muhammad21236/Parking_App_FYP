"""This module is the main module of the PerfectParkingClient package."""
import argparse
import logging
import yaml
from perfectparking import create_image_from_video, ParkingMonitorData
from colors import COLOR_RED
from coordinates_generator import CoordinatesGenerator
from motion_detector import MotionDetector


def main():
    """Main method of the PerfectParkingClient package."""
    logging.basicConfig(level=logging.INFO)

    args = parse_args()

    image_file = args.image_file
    data_file = args.data_file
    start_frame = args.start_frame

    # Generate image and coordinates if image_file is provided
    if image_file is not None:
        create_image_from_video(image_file, args.video_file)
        with open(data_file, "w+") as points:
            generator = CoordinatesGenerator(image_file, points, COLOR_RED)
            generator.generate()

    # Load parking spaces data from the YAML file
    try:
        with open(data_file, "r") as data:
            parking_spaces: list = yaml.full_load(data)
    except FileNotFoundError:
        logging.error(f"The data file '{data_file}' was not found.")
        return
    except yaml.YAMLError as e:
        logging.error(f"Error parsing the data file '{data_file}': {e}")
        return

    # Validate parking_spaces
    if not parking_spaces or not isinstance(parking_spaces, list):
        logging.error("Invalid parking spaces data. Ensure it is a non-empty list.")
        return

    # Initialize ParkingMonitorData and MotionDetector
    parking_monitor_data = ParkingMonitorData()
    detector = MotionDetector(args.video_file, parking_spaces, int(start_frame), parking_monitor_data)

    # Start motion detection
    while True:
        was_stopped = detector.detect_motion()
        if was_stopped:
            break


def parse_args():
    """Parses the command line arguments."""
    parser = argparse.ArgumentParser(description='Generates Coordinates File')

    parser.add_argument("--image",
                        dest="image_file",
                        required=False,
                        help="Image file to generate coordinates on")

    parser.add_argument("--video",
                        dest="video_file",
                        required=True,
                        help="Video file to detect motion on")

    parser.add_argument("--data",
                        dest="data_file",
                        required=True,
                        help="Data file to be used with OpenCV")

    parser.add_argument("--start-frame",
                        dest="start_frame",
                        required=False,
                        default=1,
                        help="Starting frame on the video")

    return parser.parse_args()


if __name__ == '__main__':
    main()