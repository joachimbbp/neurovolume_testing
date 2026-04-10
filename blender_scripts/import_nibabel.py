import bpy
import logging
import subprocess
import sys
import numpy as np
from pathlib import Path
import openvdb as vdb


print("hello from openVDB_builder.py")


# from util import display_message
def display_message(message, title="Notification", icon="INFO"):
    """Show a popup message in Blender."""

    def draw(self, context):
        self.layout.label(text=message)

    def show_popup():
        bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)
        return None  # Stops timer

    bpy.app.timers.register(show_popup)


# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def get_modules_path():
    """Return a writable directory for installing Python packages."""
    return bpy.utils.user_resource("SCRIPTS", path="modules", create=True)


def install_package(package, modules_path):
    """Install a single package using Blender's Python."""
    try:
        logger.info(f"Installing {package}...")
        subprocess.check_call(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "--upgrade",
                "--target",
                modules_path,
                package,
            ]
        )
        logger.info(f"{package} installed successfully.")
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to install {package}. Error: {e}")
        display_message(
            f"Failed to install {package}. Check console for details.", icon="ERROR"
        )


install_package("nibabel>=5.4.2", get_modules_path())
import nibabel as nib
# BOOKMARK: MRI stuff not implemented yet!


