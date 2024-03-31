# 1. Zaprojektuj i zaimplementuj prosty własny sposób przechowywania haseł w bazie sqlite: 
# użytkownik podaje hasło dwa razy, losujesz sól, hashujesz wszystko 
# zapisujesz hash oraz sól do bazy. Dodaj funkcję weryfikującą hasło.

import user_interface as ui


if __name__ == "__main__":
    ui.sign_up()
