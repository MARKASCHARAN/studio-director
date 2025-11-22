def auto_fix_json(json_data):
    # Fix exposure
    if json_data.get("lighting", {}).get("exposure", 1) > 1.3:
        json_data["lighting"]["exposure"] = 1.0

    # Fix palette warmth
    if json_data.get("color_palette", {}).get("warmth", 0.5) < 0.2:
        json_data["color_palette"]["warmth"] = 0.5

    return json_data
