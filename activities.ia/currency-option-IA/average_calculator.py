def mediaMovel(serie):
    medias = []
    for i, v in enumerate(serie):
        if i == 0:
            m = v
            medias.append(m)
        else:
            m = m + (v - m)/ (i + 1)
            medias.append(m)
    return medias

def funcaoAgenteCompraDolar(media, valor):
    if valor >= media:
        return False, valor, media
    else:
        return True, valor, media