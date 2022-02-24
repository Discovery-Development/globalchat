def calc_level(xp: float) -> dict:
    """
    Calculate the level using the XP as parameter.
    """
    if xp >= 0:
        lvl = 1
        text = "Absoluter Neuling"
    if xp > 20:
        lvl = 2
        text = "Beginner"
    if xp > 50:
        lvl = 3
        text = "Unglaublich"
    return {"lvl": lvl, "text": text}


def embed_colors(color: int) -> list:
    """
    Returns the embed color and URL.
    """
    # blue:
    if color == 1:
        col = 0x3535c9
        url = "https://cdn.discordapp.com/attachments/943563001183752282/946042352575873064/hr_NIGHT.png"
    
    # red:
    elif color == 2:
        col = 0xf1284c
        url = "https://cdn.discordapp.com/attachments/943563001183752282/946042687134519306/hr_RED.png"
    
    # green:
    elif color == 3:
        col = 0x44ba38
        url = "https://cdn.discordapp.com/attachments/943563001183752282/946043007310893076/hr_GREEN.png"
    
    # pink:
    elif color == 4:
        col = 0xe34ccd
        url = "https://cdn.discordapp.com/attachments/943563001183752282/946043509037752410/hr_PINK.png"
    
    # orange:
    elif color == 5:
        col = 0xff953f
        url = "https://cdn.discordapp.com/attachments/943563001183752282/946043509297791066/hr_ORANGE.png"
    
    # yellow:
    elif color == 6:
        col = 0xd3c349
        url = "https://cdn.discordapp.com/attachments/943563001183752282/946043509499101234/hr_YELLOW.png"
    
    # white
    elif color == 7:
        col = 0xebebeb
        url = "https://cdn.discordapp.com/attachments/943563001183752282/946045014419599431/hr_WHITE.png"

    # rainbow (lgbtq lol):
    else:
        col =   0xff7182
        url = "https://cdn.discordapp.com/attachments/943563001183752282/946044665172484096/HR.gif"
    
    return [col, url]