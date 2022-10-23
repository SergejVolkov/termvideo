import os
import screeninfo


def get_optimal_size(src_w, src_h, chr_aspect = (1, 2)):
    # Screen size
    try:
        monitor_info = screeninfo.get_monitors()[0]
        screen_w, screen_h = monitor_info.width, monitor_info.height
        work_w = screen_w - 4   # Approximate working area width
        work_h = screen_h - 60  # Approximate working area height
    except screeninfo.common.ScreenInfoError:
        work_w, work_h = 16, 9  # Ugly aspect ratio guess here

    # Terminal size
    term_size = os.get_terminal_size()
    term_w, term_h = term_size.columns, term_size.lines

    if work_w / work_h > src_w / src_h:
        return term_h * src_w * chr_aspect[1] // (src_h * chr_aspect[0]), term_h
    return term_w, term_w * src_h * chr_aspect[0] // (src_w * chr_aspect[1])
