def diamond_layout():
    """
    Returns normalized coordinates (0.0 to 100.0) for the North Indian Diamond Chart.
    """
    return {
        "style": "north_indian_diamond",
        "houses": {
            1:  {"x": 50, "y": 20, "label": "Top"},
            2:  {"x": 20, "y": 10, "label": "Top-Left"},
            3:  {"x": 10, "y": 20, "label": "Left-Top"},
            4:  {"x": 20, "y": 50, "label": "Left"},
            5:  {"x": 10, "y": 80, "label": "Left-Bottom"},
            6:  {"x": 20, "y": 90, "label": "Bottom-Left"},
            7:  {"x": 50, "y": 80, "label": "Bottom"},
            8:  {"x": 80, "y": 90, "label": "Bottom-Right"},
            9:  {"x": 90, "y": 80, "label": "Right-Bottom"},
            10: {"x": 80, "y": 50, "label": "Right"},
            11: {"x": 90, "y": 20, "label": "Right-Top"},
            12: {"x": 80, "y": 10, "label": "Top-Right"},
        }
    }