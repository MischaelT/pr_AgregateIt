TYPE_USD = 'USD'
TYPE_EUR = 'EUR'
TYPE_HRN = 'HRN'

TYPE_GET = 'GET'
TYPE_POST = 'POST'

TYPE_PRIVAT = 'privat_bank'
TYPE_MONO = 'mono_bank'
TYPE_OSCHAD = 'oschad_bank'
TYPE_PUMB = 'pumb_bank'
TYPE_VKURSE = 'vkurse_site'
TYPE_MINFIN = 'minfin_site'


RATE_TYPES = (
    (TYPE_USD, 'Dollar'),
    (TYPE_EUR, 'Euro'),
)

RESPONCE_LOG_TYPES = (
    (TYPE_GET, 'Get'),
    (TYPE_POST, 'Post'),
)

SOURCE_TYPES = (
    (TYPE_PRIVAT, 'Privat bank'),
    (TYPE_OSCHAD, 'Oschad bank'),
    (TYPE_PUMB, 'Pumb'),
    (TYPE_MONO, 'Mono bank'),
    (TYPE_VKURSE, 'vkurse.ua'),
    (TYPE_MINFIN, 'minfin.ua'),
)
