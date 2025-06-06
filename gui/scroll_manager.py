CURRENT_SCROLL_TARGET = None

def set_scroll_target(widget):
    global CURRENT_SCROLL_TARGET
    CURRENT_SCROLL_TARGET = widget

def unset_scroll_target(widget):
    global CURRENT_SCROLL_TARGET
    if CURRENT_SCROLL_TARGET == widget:
        CURRENT_SCROLL_TARGET = None

def handle_mousewheel(event):
    if CURRENT_SCROLL_TARGET is not None:
        delta = -1 if event.delta > 0 else 1
        CURRENT_SCROLL_TARGET.yview_scroll(delta, "units")