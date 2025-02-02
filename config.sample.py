import os

CSV_FIELDS = [
    'folder',
    'favorite',
    'type',
    'name',
    'notes',
    'fields',
    'reprompt',
    'login_uri',
    'login_username',
    'login_password',
    'login_totp',
]

FIELD_DEFAULTS = {
    'type': 'login'
}

FIELD_FUNCTIONS = {
    'name': lambda base, path, data: os.path.basename(path),
    'folder': lambda base, path, data: os.path.dirname(path).replace(base, '').lstrip('/'),
    'login_password': lambda base, path, data: data.split("\n")[0],
}

FIELD_PATTERNS = {
    'login_uri': '^url ?: ?(.*)$',
    'login_username': '^(?:user|login|username).* ?: ?(.*)$',
    'login_totp': r'otpauth://totp/[^?]+\?secret=([^&]+)',
}
